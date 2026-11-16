---
title: GoHighLevel 家庭服务自动化（三）：FF-02 Lead Follow-up —— 带条件判断的客户跟进自动化
description: 用 If/Else 条件分支做客户跟进：负责人分配、两次电话任务、等待与自动停止的完整配置。
summary: 线索进来之后怎么跟进，又不会骚扰已经回复的客户？用一条 FF-02 工作流串起负责人分配、两次电话任务、等待和 If/Else 判断，实现两次跟进后自动停止。
date: 2026-11-16
lastmod: 2026-11-16
draft: false
slug: ghl-ff-02-lead-follow-up
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

![GoHighLevel 客户跟进 FF-02：带条件判断的自动化 封面](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-cover-zh-03.webp)

> 这是「FlowFix Plumbing Demo」系列的第三篇。前两篇完成了账户配置和第一条「表单 → 商机 → 通知」的线索获取闭环。
>
> 本篇解决更核心的业务问题：**线索进来之后如何跟进，以及如何避免「客户已经回复/预约了，还在被催促」**。
>
> 我们用一条 `FF-02 | Lead Follow-up` 工作流，通过负责人分配、任务创建、等待和 **If/Else 条件分支**，实现「两次电话跟进 + 自动停止」。

## 一、业务场景与目标

原客户需求里有「两次电话跟进」「客户回复后转 Hot Lead」等功能。如果跟进流程设计得不好，会出现这样的尴尬：客户已经回复或已经预约了，系统还在按时间表继续发送催促信息。

因此，跟进的**核心不是「按时间发消息」，而是「有明确的停止条件」**。

`FF-02` 的最终业务目标：

1. 当负责人把商机从 `New Lead` 移到 `Follow-up` 时，自动启动跟进（保留人工审核权，不让所有新线索立即被自动化骚扰）；
2. 自动把商机分配给负责人，并创建第一次电话联系任务；
3. 等待一段时间后，**重新检查商机是否仍处于 Follow-up**：
   - 仍是 Follow-up → 创建第二次联系任务；
   - 已进入 Hot Lead / Booked 等其他阶段 → 直接结束，不再催促。

> 说明：MVP 阶段通过「手动移动 Pipeline 阶段」模拟「客户已回复/已预约」。真正识别客户回复并自动转 Hot Lead，属于后续扩展，本流程先用阶段状态作为停止条件。

## 二、最终工作流架构

![FF-02 跟进流程图](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-diagram-zh-03-ff02-branch.webp)

## 三、准备工作

| 项目 | 说明 |
|---|---|
| 前置资产 | 复用 FF-01 的 `FF | Service Sales Pipeline` 和 Emma Carter 的商机，无需新建表单 |
| 内部用户 | 需要一名可接收商机分配的负责人（本篇创建 `Alex Morgan`） |
| 测试联系人 | Emma Carter（已存在于 CRM） |

> 提示：FF-02 不再发送邮件。它创建的是 GHL 内部的 **Task（待办任务）**，分配给负责人并关联到联系人，查看位置在 `CRM → Contacts → 联系人详情 → Tasks`，而不是收件箱。

## 四、分步骤搭建

### 步骤 1：创建内部用户（负责人）

FF-02 需要把商机分配给负责人，但 FlowFix 子账户的用户列表是空的（这也是 FF-01 里 `Particular user` 显示 No Data 的根因）。先进入 `Settings → Users → Add User` 添加一名测试销售负责人：

| 字段 | 内容 |
|---|---|
| First / Last Name | Alex / Morgan |
| Email | 你能接收邀请的真实邮箱（如 support@xdstudiolab.com） |
| Role | 普通 User / Standard User（不赋予 Agency 管理权限） |

> 注意：GHL **User 是拥有账户权限的内部员工，不是 CRM Contact**。添加用户可能发送邀请邮件、占用账户席位。创建前确认不会产生额外费用，不要用 `example.com` 模拟邮箱。

![FF-02 跟进 操作截图 1](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113194318.webp)
*图：Alex Morgan 创建成功，User Type 为 Account - user，归属于 FlowFix Plumbing Demo 子账户，用户数量 1。*

### 步骤 2：创建 FF-02 并配置 Trigger

`Automations → Workflows → Create Workflow → Start from Scratch`，命名 `FF-02 | Lead Follow-up`。

添加 Trigger：

| 设置 | 内容 |
|---|---|
| Trigger | Pipeline Stage Changed |
| In Pipeline | FF \| Service Sales Pipeline |
| Pipeline Stage / Moved To Stage | 02 Follow-up |

不需要限定特定联系人——未来所有进入 Follow-up 阶段的客户都应启动这条自动化。

![FF-02 跟进 操作截图 2](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113190353.webp)
*图：FF-02 的 Trigger 已配置为 Pipeline Stage Changed → 02 Follow-up。*

### 步骤 3：Action 1 —— Assign User 分配负责人

在 Trigger 下点击 `+`，搜索 `Assign User`：

| 字段 | 内容 |
|---|---|
| Action Name | Assign Follow-up Owner |
| Users | Alex Morgan |
| Only Apply to Unassigned Contacts | ON |

![FF-02 跟进 操作截图 3](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113195152.webp)
*图：Assign User 节点，选择 Alex Morgan 作为跟进负责人。*

### 步骤 4：Action 2 —— Add Task 创建第一次联系任务

在 Assign User 下点击 `+`，搜索 `Add Task`：

| 字段 | 内容 |
|---|---|
| Action Name | #1 Create First Contact Task |
| Title | `First Call - ` + Contact Full Name（动态字段） |
| Assign To | Alex Morgan |
| Due Date — Value / Unit | 1 / Days |
| Due Date — Time | 11:59 PM |
| Description | Contact the customer, confirm their service needs and update the opportunity stage. |

![FF-02 跟进 操作截图 4](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113212644.webp)
*图：Add Task 节点。Due Date 只支持 Days/Weeks/Months/Years，不支持 Hours；这里的 Select time 是任务截止钟点，不是工作流等待时间。*

> 注意区分 **Task Due Date**（告诉负责人最晚何时完成联系）与 **Workflow Wait**（控制自动化何时执行下一步）——两者是两回事。

### 步骤 5：Action 3 —— Wait 等待

在 Task 下点击 `+`，搜索 `Wait`，选择 **For a set period of time**：

| 设置 | Demo 测试值 | 正式业务值 |
|---|---|---|
| Action Name | Wait - Before Second Follow-up | 保持 |
| Time Period | 2 | 1 |
| Unit | Minutes | Days |

![FF-02 跟进 操作截图 5](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113213254.webp)
*图：Wait 节点选择「For a set period of time」。GHL 的 Wait 支持 Seconds/Minutes/Hours/Days。*

> 不要选 `Until the contact replies`——Emma 是模拟邮箱和电话，无法真正回复，会一直卡在 Wait 节点。测试用 2 分钟即可，跑通后再改回 1 天。

### 步骤 6：Action 4 —— If/Else 条件分支

在 Wait 下点击 `+`，搜索 `If/Else`。GHL 会自动提供一个 **None branch**（条件不成立时走的分支），无需额外创建第二个分支。

| 设置 | 内容 |
|---|---|
| Action Name | Check Follow-up Status |
| Branch Name | Still Follow-up |
| Select | Opportunity → Pipeline Stage |
| Operator | Is / Equals |
| Value | 02 Follow-up（Pipeline: FF \| Service Sales Pipeline） |

![FF-02 跟进 操作截图 6](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113214442.webp)
*图：If/Else 条件已设置为「Opportunity 的 Pipeline Stage 是否等于 02 Follow-up」，None branch 保持为空（条件不成立直接结束）。*

> 关键：必须选 **Opportunity 的 Pipeline Stage**，而不是 Contact 的自定义字段。我们判断的是实时商机状态，不是客户最初填写的表单信息。`Pipeline Stage Changed` 属于 Opportunity 类触发器，If/Else 才能读取商机字段。

### 步骤 7：Yes 分支 —— 第二次联系任务

在 `Still Follow-up` 分支下点击 `+`，添加 `Add Task`：

| 字段 | 内容 |
|---|---|
| Action Name | #2 Create Second Contact Task |
| Title | `Second Call - ` + Contact Full Name（动态字段） |
| Assign To | Alex Morgan |
| Due Date — Value / Unit / Time | 1 / Days / 11:59 PM |
| Description | Attempt a second follow-up call with the customer. Review the first contact attempt, confirm whether the customer still needs service, and update the opportunity stage. |

![FF-02 跟进 操作截图 7](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113214704.webp)
*图：第二次联系任务的 Add Task 节点，负责人仍为 Alex Morgan。*

完成后发布 FF-02。None branch 保持空，条件不成立时直接结束。

## 五、测试与结果验证

用已有的 Emma Carter 测试（不需要再填表单）：在 `CRM → Opportunities` 把 Emma 从 `01 New Lead` 拖到 `02 Follow-up`，然后观察 2 分钟后的结果。

![FF-02 跟进 操作截图 8](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113220839.webp)
*图：Emma 的联系人详情右侧 Tasks 面板，已出现 First Call 与 Second Call 两条任务，负责人 Alex Morgan，截止日期为次日 11:59 PM。*

![FF-02 跟进 操作截图 9](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113221824.webp)
*图：FF-02 的 Execution Logs，完整记录 Assign → First Task → Wait → If/Else（Still Follow-up 成立）→ Second Task → End 的执行时间线。*

**FF-02 执行结果（主分支已通过）**：

| 执行时间 | Action | 状态 |
|---|---|---|
| 21:55:20 | Add to Workflow | 成功 |
| 21:55:20 | Assign Follow-up Owner | 已执行 |
| 21:55:22 | Create First Contact Task | 成功 |
| 21:55:22 | Wait | 进入等待 |
| 21:57:22 | Wait Finished | 2 分钟结束 |
| 21:57:23 | Still Follow-up | 条件成立 |
| 21:57:23 | Create Second Contact Task | 成功 |
| 21:57:24 | End of Workflow | 正常结束 |

**已验证**：GHL 不只是按时间执行固定动作，还能在等待结束后根据商机当前所处阶段决定走哪个分支。第一次任务正确显示 `First Call - Emma Carter`。

**三项待收尾/待核实（如实标注）**：

1. **第二次任务标题未映射（Bug，需修正）**：显示为 `Second Call - Contact Full Name` 而非 `Second Call - Emma Carter`。原因是 Title 里用了普通文字，需改用标签图标插入 `Contact → Full Name` 动态字段。修正后新任务才正确，不影响已生成的旧任务。
2. **Contact Owner 仍显示 Unassigned（待核实）**：Assign User 节点虽显示 Executed，但联系人详情仍显示 `Owner: Unassigned`。需打开 Owner 下拉框确认是否真的分配给了 Alex Morgan——「任务能分配给 Alex」不代表「Contact/Opportunity Owner 已同步更新」，二者可能不同步。
3. **None 分支尚未测试（待验证）**：目前日志只证明了「Still Follow-up」分支。还需做一次负向测试——让一条新商机进入 Follow-up 后，在 2 分钟内移到 Booked，确认走 None branch 且不创建第二次任务。

> 建议：负向测试完成后，把 Wait 从测试用的 `2 Minutes` 改回正式的 `1 Day` 再发布，否则 Snapshot 复制给客户后会在两分钟后就创建第二次联系任务。

## 六、关键实施经验

1. **跟进必须有停止条件**。用「If/Else 检查商机当前阶段」比「按时间固定发消息」更符合真实销售场景，能避免已回复/已预约客户继续收到催促。
2. **「Executed」不等于「生效」**。Assign User 显示 Executed 但 Owner 仍是 Unassigned，说明要打开实际数据核实，不能只凭绿色日志判断成功。
3. **User 与 Contact 是两回事**。User 是有权限的内部员工（`Settings → Users`），Contact 是客户；「创建跟进任务」在 `Workflow → Add Action → Add Task`，不是在 Users 设置里找 Task。
4. **动态字段必须用标签选择器插入**。手写 `Contact Full Name` 只是普通文字，所有任务标题都会变成字面上的「Contact Full Name」。
5. **Wait 与 Task Due Date 是两个概念**，别混用：Wait 控制流程何时继续，Due Date 只是给负责人看的任务截止时间。
6. **测试分支要分次进行**，别在 T03（第二次任务）还没跑完时就移动商机，否则两个测试互相干扰；再次触发工作流还要确认 Workflow 的 Re-entry 设置。

## 七、总结

`FF-02` 是整套自动化里业务价值最高的一条：它把「负责人分配 + 两次电话跟进 + 条件停止」串成一个闭环，验证了 GHL 原生 CRM 与 Workflow 的无缝衔接——这是它相比 Make/n8n 方案最明显的优势。

当前主分支已跑通，剩余的是三件收尾工作：修正第二次任务标题的动态字段、核实 Owner 是否真正同步、做一次「已预约即停止」的负向测试。完成后即可进入 `FF-03 | Appointment Management`（预约确认与提醒），并把整套配置封装成可复用的 Snapshot。

> 系列导读与总结：[GoHighLevel 家庭服务自动化 · 系列导读与总结](00-系列导读与总结.md)
