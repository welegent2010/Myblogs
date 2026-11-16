---
title: GoHighLevel 家庭服务自动化（二）：第一条自动化流程 FF-01 —— 表单到商机的端到端闭环
description: 用 GHL 原生节点完成表单到商机的闭环：建 Pipeline、询盘表单与 FF-01 工作流，并真实提交验证。
summary: 从六阶段 Pipeline、七字段询盘表单，到 FF-01 工作流的三步动作（打标签、建商机、内部通知），再用模拟客户通过公开表单真实提交一次，验证整条链路确实跑通。
date: 2026-11-16
lastmod: 2026-11-16
draft: false
slug: ghl-ff-01-form-to-opportunity
channels:
- notes-methods
topics:
- workflow
content_type: method
featured: false
categories:
- 业务自动化
tags:
- gohighlevel
series:
- GoHighLevel 家庭服务自动化
showTableOfContents: true
showComments: true
---

![GoHighLevel 自动化流程 FF-01：表单到商机闭环 封面](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-cover-zh-02.webp)

> 这是「FlowFix Plumbing Demo」系列的第二篇。上一篇搭好了账户结构，本篇将完成**第一个真正跑通的业务闭环**：
>
> 客户在网站表单提交维修询盘 → GHL 自动创建 Contact 和 Opportunity → 负责人收到内部通知。
>
> 全程只用 GHL 原生功能，不借助 Make / n8n。用模拟客户 Emma Carter 通过公开表单真实提交一次，即可验证整条链路。

## 一、业务场景与目标

家庭服务公司（水管、HVAC、电工）最常见的获客动作就是「客户提交维修询盘」。传统做法是客服手动把询盘录入表格、再分配销售跟进，既慢又容易漏单。

我们要用一条工作流 `FF-01 | New Lead Intake` 把它自动化。当客户提交 `FF | Service Request` 表单时，系统自动完成三件事：

1. 给联系人打上 `FF-New-Lead` 标签（标记线索来源）；
2. 在 `FF | Service Sales Pipeline` 中创建一条阶段为 `01 New Lead` 的商机；
3. 向负责人发送一封内部通知，带上客户姓名、服务类型、紧急程度和需求描述。

**验收标准**：Emma 通过公开表单提交数据后，Contacts 中出现 Emma、Opportunities 中出现她的 `New Lead` 商机、内部通知包含正确的服务需求。

## 二、最终工作流架构

![FF-01 工作流流程图](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-diagram-zh-02-ff01-workflow.webp)

> 注意：表单提交本身就会创建/更新联系人，所以**不需要**再加一个 `Create Contact` 节点。三个 Action 已足够，保持最小可用。

## 三、准备工作

在搭工作流之前，先建立三个前置资产：

| 资产 | 名称 | 用途 |
|---|---|---|
| Pipeline | `FF | Service Sales Pipeline` | 六个销售阶段，商机的落点 |
| Form | `FF | Service Request` | 公开询盘表单，触发表单提交事件 |
| 通知邮箱 | 负责人可接收的邮箱 | Internal Notification 的收件地址 |

模拟测试客户数据（Emma Carter）：

| 字段 | 值 |
|---|---|
| First / Last Name | Emma / Carter |
| Phone | +1 312-555-0101 |
| Email | emma.carter@example.com |
| Service Type | Leak Repair |
| Service Urgency | Within 48 Hours |
| Project Description | Water is leaking beneath the kitchen sink. I need someone to inspect and repair it within the next two days. |

## 四、分步骤搭建

### 步骤 1：创建销售管道 Pipeline

进入 `CRM → Opportunities → Pipeline`。首次进入显示 `No pipelines yet`。

![FF-01 工作流 操作截图 1](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113155107.webp)
*图：Pipeline 管理页显示 No pipelines yet，正适合从零搭建。*

点击右上角 `Create pipeline`，名称填 `FF | Service Sales Pipeline`，配置六个阶段：

| 顺序 | Stage Name | 业务含义 | Probability | 配色 |
|---|---|---|---|---|
| 01 | New Lead | 新询盘，尚未联系 | 10% | 灰蓝 #64748B |
| 02 | Follow-up | 已开始联系，等待回复 | 25% | 蓝 #3B82F6 |
| 03 | Hot Lead | 客户回复，有明确需求 | 50% | 橙 #F59E0B |
| 04 | Booked | 已安排预约 | 75% | 紫 #8B5CF6 |
| 05 | No-show | 客户未按时赴约（异常） | 20% | 红 #EF4444 |
| 06 | Completed | 服务已完成 | 100% | 绿 #22C55E |

![FF-01 工作流 操作截图 2](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113160820.webp)
*图：Pipeline 编辑器。可设置阶段名称、成交概率（Probability）与报表开关（Funnel / Distribution 两个图标）。*

![FF-01 工作流 操作截图 3](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113163724.webp)
*图：最终 Pipeline 看板，六个阶段用不同颜色区分，橙=Hot Lead、红=No-show、绿=Completed。*

**两点关键配置**：

- **Probability（成交概率）不是进度百分比**。它表示「商机处于当前阶段时最终成交的估计可能性」，六个数之间不累加、也不要求加起来等于 100%。No-show 从 75% 降到 20% 是「成交预期恶化」，不是「进度倒退」。这些是教程演示值，正式项目应基于历史胜率调整。
- **Use opportunity-level probability 保持 OFF**；`Show in reports` 的漏斗图标（Funnel）与饼图图标（Distribution）是两个独立开关——No-show 属于异常阶段，建议关掉 Funnel、保留 Distribution，避免污染销售漏斗数据。

### 步骤 2：创建客户询盘表单

进入 `Sites → Forms → Builder`，选择 `Create New Form`（模板选 Blank Form），表单命名 `FF | Service Request`。

![FF-01 工作流 操作截图 4](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113164507.webp)
*图：Form Builder 中的字段编辑界面。*

表单包含 7 个**必填**字段：

| 字段 | 类型 | 必填 |
|---|---|---|
| First Name / Last Name | Text | 是 |
| Phone | Phone | 是 |
| Email | Email | 是 |
| Service Type | Single Dropdown（单选） | 是 |
| Service Urgency | Single Dropdown（单选） | 是 |
| Project Description | Multi Line（多行文本） | 是 |

Service Type 六个选项：Leak Repair、Drain Cleaning、Water Heater Repair、Pipe Inspection、Emergency Plumbing、Faucet Replacement。
Service Urgency 四个选项：Urgent、Within 48 Hours、This Week、Flexible。

![FF-01 工作流 操作截图 5](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113170447.webp)
*图：把 Service Type / Service Urgency 从 Multi Dropdown 改为 Single Dropdown，保证每条询盘只有一个主要服务/紧急程度，后续 Workflow 便于直接判断。*

**关键：确认三个业务字段已保存为 Contact Custom Field**。这是本表单最重要的一点——我们不只是收集表单数据，而是要让 Workflow 能读取 `Service Type`、`Service Urgency`、`Project Description` 用于线索分类和内部通知。验证方法：在 Form Builder 中点击 `Add Object Fields`，选择 Contact，确认这三个字段出现在可用字段列表中。

![FF-01 工作流 操作截图 6](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113170828.webp)
*图：表单保存完成，右侧显示 Your form is ready，七个字段均已设为 Required。*

> 提示：底部 SMS Consent 保留着默认占位符。本阶段只做内部测试、不发送短信，可暂不配置，但不要把这份表单直接作为对外收集信息的正式页面使用。

### 步骤 3：新建工作流并配置 Trigger

进入 `Automations → Workflows`，点击 `Create workflow`，选择 `Start from Scratch`（从空白开始），命名 `FF-01 | New Lead Intake`。

![FF-01 工作流 操作截图 7](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113171432.webp)
*图：Workflows 列表页，本教程选择手动创建（Start from Scratch），不使用 AI 生成。*

进入编辑器后，建议点击 **Enable auto save now**（草稿阶段自动保存，发布后不再适用）。然后在画布上点击 **Add new trigger**，搜索并选择 `Form Submitted`，配置过滤条件：

| 设置 | 内容 |
|---|---|
| Trigger | Form Submitted |
| Filter | Form is |
| Form | FF \| Service Request |

这个 Filter 很重要：**不限定表单**，将来同账户下其他表单也会误触发这条 New Lead 工作流。

![FF-01 工作流 操作截图 8](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113174959.webp)
*图：已配置 Form Submitted Trigger（关联 FF | Service Request），并添加了第一个 Action「Add Contact Tag」。*

### 步骤 4：Action 1 —— Add Contact Tag

在 Trigger 下方点击 `+`，搜索 `Add Contact Tag`，配置：

| 设置 | 内容 |
|---|---|
| Action Name | Add Tag - New Lead |
| Tags | FF-New-Lead |

添加 Tag 时确认下拉框里确实选中了 `FF-New-Lead`（必要时先 `Create new tag`），不要只输入文字就保存。

### 步骤 5：Action 2 —— Create Opportunity（用新版节点）

在 Add Tag 下方点击 `+`，搜索 Opportunity。

> ⚠️ **版本差异（重要）**：GHL 会把 `Create or Update Opportunity` 标记为 **Deprecated（即将弃用）**，官方建议新工作流改用独立的 `Create Opportunity`。从零搭建时不要选旧版组合节点。

![FF-01 工作流 操作截图 9](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113180906.webp)
*图：新版 `Create Opportunity` 节点的配置面板。新节点不提供 Status 选项，不指定时会默认创建为 Open。*

按下面配置：

| 字段 | 内容 |
|---|---|
| Action Name | Create New Service Opportunity |
| Pipeline | FF \| Service Sales Pipeline |
| Stage | 01 New Lead |
| Opportunity Name | `Contact Full Name` + `-` + `Service Type`（动态字段，例：Emma Carter - Leak Repair） |
| Opportunity Source | `FF Service Request Form`（固定文字，表示商机来源） |
| Opportunity Value | 0 |
| Duplicate Opportunities | Disabled（避免同一联系人反复测试产生重复商机） |

字段映射要点：

- **Opportunity Source 不要填 Service Type**。Source 是「商机从哪来」，Service Type 是「客户需要什么服务」，二者语义不同。以后增加电话、Google Ads 等渠道时可分别统计。
- 新版 `Create Opportunity` **没有 Status 选项**，不指定时默认创建为 `Open`，无需额外加 `Update Opportunity` 节点。
- 动态字段通过右侧标签图标插入（`Contact → Custom Fields → Service Type`），而不是手写变量名。

### 步骤 6：Action 3 —— Send Internal Notification

在 Create Opportunity 下方点击 `+`，搜索 `Send internal notification`（新版名称，绿色铃铛图标）。

![FF-01 工作流 操作截图 10](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113182751.webp)
*图：在通知 Message 编辑器里，通过标签图标（Custom Values）把 `Contact → Custom Fields` 下的 Service Type / Service Urgency / Project Description 插入正文。*

通知配置：

| 字段 | 内容 |
|---|---|
| Action Name | Notify Owner - New Lead |
| Type of Notification | Email |
| From Name / From Email | 都**留空**（使用 GHL 默认发件设置） |
| To User Type | Custom email |
| Recipient Email | 你的负责人收件邮箱（本教程用 QQ 邮箱） |
| Subject | New Service Request - FlowFix Plumbing |

Message 正文示例（方括号内用动态字段插入）：

```text
NEW SERVICE REQUEST — FLOWFIX PLUMBING

A new customer inquiry has been received.

Customer: [Contact Full Name]
Email: [Contact Email]
Phone: [Contact Phone]

Service Type: [Service Type]
Urgency: [Service Urgency]

Project Description:
[Project Description]

Pipeline: FF | Service Sales Pipeline
Stage: 01 New Lead

Next Action: Review the customer inquiry and arrange the first contact attempt.
```

**两个必须避开的坑**：

1. **收件人用 Custom email，而不是 Particular user**。当前 FlowFix 子账户的用户列表为空（`Select Users` 显示 No Data），选择 `Particular user` 会找不到收件人。先填一个固定的 `Custom email` 把 Demo 跑通，正式项目再配置负责人分配。
2. **From Name 和 From Email 必须成对**。只要填了 `From Name` 却没填 `From Email`，会报 `From email is mandatory when From Name is entered`。Demo 阶段两个都清空，用默认发件设置即可。

![FF-01 工作流 操作截图 11](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113183426.webp)
*图：FF-01 保存并发布成功，右上角显示 Workflow is now published and live，Form Submitted Trigger + 三个 Action 全部就绪。*

### 步骤 7：发布

确认三个 Action 配置齐全后，把右上角 `Draft` 切换为 `Publish`。发布后公开表单提交就会自动触发工作流，无需手动执行。

## 五、测试与结果验证

进入 `Sites → Forms`，找到 `FF | Service Request`，点击 Share 打开公开表单，填写 Emma Carter 的资料并点击 Submit（**不是**点 Workflow 里的 Test workflow——我们要验证的是完整端到端链路）。

提交后依次检查四个位置：

![FF-01 工作流 操作截图 12](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113185002.webp)
*图：一次表单提交产生五条 Execution Logs：Add to workflow → Add Tag → Create Opportunity → Notify Owner → Removed by End Of Workflow。三个 Action 均显示绿色 Executed。*

![FF-01 工作流 操作截图 13](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113185020.webp)
*图：手机/邮箱实际收到内部通知，说明通知邮件已送达（而不仅是节点显示 Executed）。*

![FF-01 工作流 操作截图 14](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113185031.webp)
*图：通知邮件正文，Service Type / Urgency / Project Description 三个自定义字段正确填充。*

![FF-01 工作流 操作截图 15](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113185052.webp)
*图：CRM → Contacts 中出现 Emma Carter，三个业务字段保存完整。*

![FF-01 工作流 操作截图 16](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113185103.webp)
*图：CRM → Opportunities 的 Pipeline 看板，Emma 的商机 `Emma Carter - Leak Repair` 进入 01 New Lead，六个阶段配色清晰可见。*

**FF-01 最终验收结果**：

| 检查位置 | 预期结果 | 实际结果 |
|---|---|---|
| 表单提交 | Emma 的询盘成功提交 | ✅ 成功 |
| Contacts | 自动创建 Emma Carter | ✅ 成功 |
| 客户标签 | ff-new-lead 已添加 | ✅ 成功 |
| Opportunity | Emma Carter - Leak Repair，01 New Lead，Status Open | ✅ 成功（并验证了新版节点默认 Open） |
| 字段映射 | 服务类型 / 紧急程度 / 描述正确 | ✅ 成功 |
| 内部邮件 | QQ 邮箱实际收到通知 | ✅ 送达 |
| 执行日志 | 三个 Action 均 Executed | ✅ 成功 |

> 补充说明：Contacts 里出现了第二条「QQ 邮箱」联系人，很可能是通知/测试过程中的系统记录，不影响 Emma 的正常商机；如需排查可查看该联系人的 Created By 与 Activity/Audit Logs。当前 Opportunity Owner 仍为 Unassigned，Demo 用 Custom Email 收件不影响运行，但「负责人分配」要留到 FF-02 解决。

## 六、关键实施经验

1. **旧节点要绕开**：`Create or Update Opportunity` 已被弃用，新工作流直接用 `Create Opportunity`；新版无 Status 字段，默认 Open。
2. **字段语义别混淆**：Opportunity Source 是来源、Service Type 是服务需求；表单名在 Trigger 里指定，不要在 Opportunity 节点里再找「Service Request」字段。
3. **内部通知收件人用 Custom email 最省事**：能绕开子账户用户列表为空的问题，快速验证闭环。
4. **发件人字段成对**：From Name 与 From Email 要么都空、要么都填，否则保存报错。
5. **区分三个数据层次**：Contacts（客户是谁/需求是什么）、Opportunities（业务进行到哪一步）、Execution Logs（自动化有没有正常运行）。日常管理只看 Pipeline 看板，Execution Logs 只用于调试排查。
6. **「Executed」≠「送达」**：通知节点显示 Executed 只代表动作执行成功，邮件是否送达要另查收件箱。本教程两者都验证了，才标记「已通过」。

## 七、总结

FF-01 是本系列第一个完整跑通的端到端闭环，验证了 GHL 的原生优势：表单、联系人、商机、通知、执行日志都在一个平台内自动衔接，不需要再像 Make / n8n 那样额外接一个 Google Sheets 才能做客户管理。

但这条流程只解决了「接到线索」，还没解决「跟进线索」。下一篇 `FF-02 | Lead Follow-up` 将加入负责人分配、第一次/第二次电话联系任务，并用 **If/Else 条件分支** 解决最关键的业务问题：**客户已经回复或预约后，自动停止催促，不再发送多余的跟进消息**。

> 下一篇：[GoHighLevel 家庭服务自动化（三）：FF-02 Lead Follow-up 跟进自动化](03-FF-02-Lead-Follow-up：带条件判断的客户跟进自动化.md)
