---
title: "在这里填写文章标题"
date: {{ .Date }}
lastmod: {{ .Date }}
draft: false

description: "用一句话概括这篇文章的核心内容（用于 SEO 描述）。"
summary: "列表页摘要，建议 40~90 字。"

# 研究频道：cities-industries / markets-finance / notes-methods
# 注意：Hugo 只认复数键 channels，写成单数 channel 不会注册词条
channels:
  - cities-industries

# 研究主题：见 data/topics.yaml，必须是里面已有的 key
topics:
  - urban-regeneration

# 内容类型：essay / note / method / tool / experiment
content_type: "essay"

# 是否进入首页「重点研究」
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
2. channels 只能是 cities-industries / markets-finance / notes-methods 三选一
3. topics 只能用 data/topics.yaml 里已定义的 key，新增主题先改 data 文件
4. 标题、description、summary 保留双引号
5. 列表项每一项前面保留 "- "
-->

# 在这里填写正文标题

<!--more-->

## 引言

在这里继续正文内容。
