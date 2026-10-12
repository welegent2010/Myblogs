---
title: "在这里填写文章标题"
date: {{ .Date }}
lastmod: {{ .Date }}
draft: false

description: "用一句话概括这篇文章的核心内容（用于 SEO 描述）。"
summary: "列表页摘要，建议 40~90 字。"

# 一级频道，三选一，不能用别的词
#   cities-industries -> /urban/ 城市与产业
#   markets-finance   -> /markets/ 市场与金融
#   notes-methods     -> /notes/ 方法与工具
# 必须写成复数 channels，单数 channel 不会注册词条
channels:
  - cities-industries

# 二级主题，必须属于上面这个频道，来源 data/topics.yaml
#   cities-industries: urban-regeneration(城市更新)、tourism(文旅)、regional-development(区域发展)、
#                      industry-research(产业研究)、development-economics(投资运营)、
#                      gis-data(GIS与数据)、planning-practice(规划实践)
#   markets-finance:   us-equities(美股)、company-research(公司研究)、industry-chain(产业链研究)、
#                      ai-infrastructure(AI基础设施)、semiconductors(半导体)、
#                      market-structure(市场结构)、trading(交易方法)、portfolio(投资组合)
#   notes-methods:     ai-research(AI与研究)、gis-data-methods(GIS与数据)、knowledge-systems(知识系统)、
#                      web-software(软件与工具)、workflow(工作流)、ux-design(体验设计)
# 写错 key 不报错，只会生成孤儿聚合页，文章不会进任何栏目，落笔前务必核对
topics:
  - urban-regeneration

# URL 片段，英文小写加连字符
slug: ""

# 内容类型：essay / note / method / tool / experiment
content_type: "essay"

# 是否进入频道页顶部「重点推荐」
featured: false

# 旧分类，保留即可，不影响新的频道体系
categories:
  - 工作记录

tags:
  - 标签一
  - 标签二

series:
  - 工作笔记

showTableOfContents: true
showComments: true
---

<!--
填写提醒：
1. 日期必须是 YYYY-MM-DD，例如 2026-04-02
2. slug 用英文小写加连字符，改过的旧地址补到 aliases
3. channels 三选一，topics 只能用上面注释里列出的 key，不能自己造词
4. 要新建二级主题：先在 data/topics.yaml 加词条（写明 en / zh / channel），
   再把 key 挂到 data/channels.yaml 对应频道的 topics 列表，两处都改才会出现在频道页导航栏和侧栏
5. 完整规则见项目根目录的 发文模板.md
6. 标题、description、summary 保留双引号，列表项每项前面保留 "- "
-->

# 在这里填写正文标题

<!--more-->

## 引言

在这里继续正文内容。
