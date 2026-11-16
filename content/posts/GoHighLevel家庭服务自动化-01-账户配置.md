---
title: GoHighLevel 家庭服务自动化（一）：账户配置——从 Agency 到 FlowFix 子账户
description: 在 GoHighLevel 里把账户结构搭对：Agency 层与子账户各放什么，以及新建 FlowFix 子账户的完整步骤。
summary: 自动化能否复用，取决于账户分层是否正确。本篇说明 Agency 层与 Sub-account 层各自承载什么，并逐步新建 FlowFix Plumbing Demo 子账户、确认业务菜单可进入，为后续 Pipeline、表单与工作流打地基。
date: 2026-11-16
lastmod: 2026-11-16
draft: false
slug: ghl-account-setup-agency-to-subaccount
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

![GoHighLevel 账户配置：从 Agency 到 FlowFix 子账户 封面](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-cover-zh-01.webp)

> 系列定位：这是「FlowFix Plumbing Demo」家庭服务自动化教程的第一篇。整个系列用 GoHighLevel（GHL）原生功能，从零搭建一套可复用的线索获取与跟进自动化系统，最终封装成 Snapshot 交付给营销代理机构复用。
>
> 本篇只解决一件事：**把 GHL 的账户结构搭对**——在 Agency（代理机构层）下新建一个独立的业务子账户 `FlowFix Plumbing Demo`，为后续 Pipeline、表单和 Workflow 的搭建打地基。

## 一、业务场景与目标

营销代理机构（Agency）需要同时服务多个客户，每个客户在 GHL 里对应一个独立的 **Sub-account / Location（子账户）**。子账户之间数据隔离，各自拥有自己的 Contacts、Opportunities、Workflows 和 Sites。

本系列以一个虚构的芝加哥家庭水管维修公司 **FlowFix Plumbing** 为模拟客户，验证 GHL 最有价值的几个原生能力：CRM、销售管道、工作流、预约与 Snapshot 模板化部署。

因为最后要产出可复制的 **Snapshot**，所以账户结构必须从第一天就区分清楚两层：

- **Agency 层**：你的 GHL 主账户，负责管理所有客户子账户、创建 Snapshot；
- **Sub-account 层**：具体的业务工作账户，Form、CRM、Pipeline、Calendar、Workflow 都在这一层搭建。

如果把工作流建错了账户层级，后续会出现在错误的账户里、无法复制等问题。

> ⚠️ 说明：本系列所有企业资料均为**模拟数据**（虚构公司、保留域名 `example.com`、`555-01xx` 预留号码），仅用于教程与作品集演示，不对应真实企业、不用于真实联系。

## 二、最终账户架构

![账户配置流程图](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-diagram-zh-01-account-layers.webp)

本篇完成后，账户应处于上图右侧「FlowFix Plumbing Demo」子账户已就绪、可进入业务菜单的状态。

## 三、准备工作

| 项目 | 说明 |
|---|---|
| GHL 账号 | 已订阅的 30 天试用或正式账户，能登录 Agency View |
| 通知邮箱 | 一个你能实际接收测试邮件的邮箱（本系列后续内部通知使用 QQ 邮箱） |
| 浏览器 | Chrome（后续排查加载慢时，可用无痕窗口/Safari 对照） |
| 不需要 | 邮件发件域名、LC Phone、SMS、Stripe/PayPal、WhatsApp、AI Agent —— 这些本阶段一律不配置 |

## 四、分步骤搭建

### 步骤 1：确认 Agency View 与现有子账户

登录 [GoHighLevel](https://app.gohighlevel.com/)，确认左上角当前处于 **Agency View**，然后进入 `Sub-Accounts → Accounts`。

![账户配置 操作截图 1](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113152308.webp)
*图：Agency View 下的 Sub-accounts 列表。Agency 名称为 `crc`，已有一个系统预建子账户 `crc`（创建于 2026-11-12），右上角有 `Create Sub-Account` 按钮。*

**这一步确认什么**：你的账户结构已经初始化，无需重新注册 Agency。若已有可用的空白子账户，优先复用；本教程保留原 `crc` 子账户不动，单独新建 FlowFix，便于后续区分 Snapshot 来源账户。

### 步骤 2：创建 FlowFix Plumbing Demo 子账户

点击右上角蓝色 `Create Sub-Account` 按钮，进入创建流程。系统会先让你搜索企业地址。

![账户配置 操作截图 2](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113152827.webp)
*图：创建子账户的地址选择页，右侧搜索框旁有 `Add Manually` 入口。因为 FlowFix 是虚构企业，不在地图上选取真实营业地址。*

由于模拟企业没有真实地址，点击搜索框右侧的 **Add Manually**，手动填写企业信息，而不是从 Google 地图中选一家现有企业。

![账户配置 操作截图 3](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113152943.webp)
*图：Add Manually 的手动填写表单，用于录入模拟企业资料（截图显示部分字段）。*

按下面的模拟资料填写（能留空的非必填项就留空，不编造真实美国企业地址）：

| 字段 | 设置值 |
|---|---|
| First Name | Alex |
| Last Name | Morgan |
| Email | `flowfix.demo@example.com` |
| Business Name | FlowFix Plumbing Demo |
| Business Niche | Plumbing / Home Services |
| Business Phone | `+1 312-555-0148` |
| Address | 100 Demo Plaza |
| City / State / Country | Chicago / Illinois / United States |
| Zip | 60601 |
| Time Zone | America/Chicago（如界面显示城市时区，选 Central Time (US & Canada)） |

> 说明：`+1 312-555-0148` 属于北美预留的虚构号码段（555-0100 ~ 555-0199）；`example.com` 是保留示例域名。如果 GHL 要用该邮箱发送登录邀请或验证，需换成你能真实接收邮件的邮箱。页面底部的 `Include sample data` 保持 OFF，并选中 `This is my client's account`。

### 步骤 3：检查并修正 Business Profile

子账户创建成功后进入账户详情页 `Basic Details`。

![账户配置 操作截图 4](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113154535.webp)
*图：FlowFix Plumbing Demo 子账户创建成功后的 Basic Details 页面，说明账户结构已建立。*

这里是**最终确定**的几个关键项（也是本教程实际验证过的最终状态）：

| 配置项 | 最终状态 |
|---|---|
| Sub-account 名称 | FlowFix Plumbing Demo（保留） |
| Time Zone | `GMT+08:00 Asia/Shanghai (CST)` —— 已确认可用，保留 |
| Website | 建议清空（不要挂与模拟企业无关的真实网址） |
| 地址 / 邮编 | 建议保持主体一致（外观项，不影响自动化） |

时区这里有一个已确认的结论：香港与上海目前同为 UTC+8 且都不实行夏令时，所以 `Asia/Shanghai` 对联系人记录、工作流等待时间没有实际影响。后续模拟芝加哥客户预约时，再在 Calendar 里单独检查时区（芝加哥有夏令时）。

### 步骤 4：切换到子账户，进入业务界面

在账户详情页点击右上角 **Switch to Sub-Account**（`Actions` 左侧的浅蓝色按钮），进入子账户的业务功能区。

![账户配置 操作截图 5](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113152531.webp)
*图：Sub-accounts 列表中的 `Switch to Sub-Account` 入口，用于进入子账户业务界面。*

![账户配置 操作截图 6](https://ele-image.oss-cn-guangzhou.aliyuncs.com/img/gohighlevel/ghl-20261113154757.webp)
*图：进入 FlowFix Plumbing Demo 后的 Dashboard，左侧菜单可见 CRM、Automations、Sites 等功能区。*

进入后应能看到左侧的业务菜单：**Contacts、Opportunities、Calendars、Automation、Sites、Settings**。这些是后续搭建 Pipeline、表单和工作流的入口。

## 五、测试与结果验证

本篇没有「运行」类测试，验收点是**账户就绪度**：

| 检查项 | 预期结果 | 实际结果 |
|---|---|---|
| 子账户创建 | FlowFix Plumbing Demo 出现在 Sub-accounts 列表 | ✅ 成功 |
| 进入业务界面 | 左侧可见 CRM / Automations / Sites | ✅ 成功 |
| 时区 | Asia/Shanghai（GMT+8），UTC+8 与 HK 一致 | ✅ 确认可用 |
| Pipeline 状态 | 尚未创建，显示 No pipeline available | ✅ 符合预期 |

> 备注：Dashboard 中若出现 Google Analytics / Ads / Meta Ads 的 `Connection expired`，以及 Email Health Report 提示，**都不是报错**，与 CRM / Workflow 无关，本阶段无需处理。

## 六、关键实施经验

1. **Agency 与 Sub-account 必须一开始就分清**。所有业务资产（Form / CRM / Pipeline / Calendar / Workflow）都建在子账户层；Snapshot 在 Agency 层创建。层错则复制失败。
2. **模拟企业信息要守规矩**：虚构电话用 `555-01xx` 段、邮箱用 `example.com` 保留域、地址明确标注虚构；一旦系统要求真实验证（电话/地址/邮箱），不要用虚构资料绕过。
3. **时区别纠结**：本 Demo 最终用 `Asia/Shanghai`（GMT+8）即可，对流程无影响；芝加哥客户的预约时区留到 Calendar 阶段再处理。
4. **Snapshot 权限需提前核实**：不是所有试用账户都有 `Account Snapshots` 或创建第二个子账户的权限。先在 Agency View 左侧确认该功能存在即可，**现在不创建**；若无权限，Snapshot 环节标记「待验证」，不影响先完成核心业务 Demo。
5. **不配置用不到的功能**：邮件发件域名、短信、支付、AI Agent 全部跳过，先在系统内部完成「联系人 → 管道 → 工作流」闭环。

## 七、总结

账户配置是整套自动化最不起眼、却最容易埋雷的一步。本篇用最简结构完成了「Agency → Sub-account」的清晰分层，并确认了子账户可正常进入业务界面。

下一篇将正式进入第一个业务对象：先建 **Pipeline（销售管道）** 和 **询盘表单**，再用一条 `FF-01 | New Lead Intake` 工作流把「表单提交 → 联系人 → 商机 → 内部通知」整条链路跑通。

> 下一篇：[GoHighLevel 家庭服务自动化（二）：第一条自动化流程 FF-01](02-第一条自动化流程FF-01：表单到商机的端到端闭环.md)
