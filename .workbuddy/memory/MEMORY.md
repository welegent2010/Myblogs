# Myblogs 项目长期约定

## 站点事实

- Hugo 站点，域名 `https://87188202.xyz/`，`hugo.toml` 单文件配置，模板在 `layouts/`，主题 `themes/congo-dev`（只用其 assets/data，页面结构基本被项目 layouts 接管）。
- 部署：Cloudflare Pages 从 Git 源码构建。`public/`、`public-drafts/`、`resources/` 都在 .gitignore 里，**改源码才算生效，构建产物不用提交**。

## 文章归属体系（核心）

- 决定文章出现在哪个栏目的只有 front matter 两个字段，其余字段都不管位置：
  - `channels` → 一级频道，取值来自 `data/channels.yaml`（3 个 key）
  - `topics` → 二级主题，取值来自 `data/topics.yaml`（21 个 key）
- 频道与页面地址映射：`cities-industries → /urban/`、`markets-finance → /markets/`、`notes-methods → /notes/`；地址由 `content/channels/<key>/_index.md` 的 `url:` 覆盖。
- `categories` / `tags` / `series` 是旧字段，中文随意，只影响 SEO、相关阅读、归档。
- `featured: true` 进频道页顶部重点区（按日期倒序）。
- **写错 key 不会报错**，Hugo 会静默生成孤儿聚合页，文章不进任何栏目。新增二级主题必须同时改 `data/topics.yaml`（加词条）和 `data/channels.yaml`（挂进频道 topics 列表）。

## 维护约定

- 改了 `data/channels.yaml` 或 `data/topics.yaml` 之后，必须同步三处文档：`发文模板.md` 的对照表、`archetypes/default.md` 的字段注释、`README.md` 的 Writing Workflow 章节。
- 新增 sitemap 收录范围要看 `layouts/sitemap.xml`：用 URL 白名单放行指定页，`hugo.toml` 的 `params.sitemap.excludedKinds` 负责整类排除（当前排除 taxonomy/term）。目前 28 条 URL；`/search/` 刻意用 `xml: false` + `noindex,follow` 排除，不要改。

## SEO / 统计

- Google Analytics 4：Measurement ID `G-ZRV5DR4HCX`，代码在 `layouts/partials/head.html` 末尾，经 `layouts/_default/baseof.html` 全站生效（含 404）。
- sitemap 与 robots.txt 由 Hugo 自动生成，已在 Search Console 待提交。

## 封面与卡片体系

- 封面取值顺序（`layouts/partials/func/cover.html`）：front matter `image:` → 正文第一张图 → CSS 占位块（频道编号 + 名称，网格纹理）。
- 图片放 `assets/img/covers/`，front matter 写 `image: /img/covers/<slug>.jpg`；管线自动转 WebP + srcset（`img.html` + `img-resource.html`，扩展名可兜底替换）。
- 正文插图用短代码 img：花括号 img + src/alt 参数（`layouts/shortcodes/img.html`）。
- 卡片四种 variant：grid / row / compact / large（`entry.html`，调用必须传 dict）。
- 首页频道栅格：12 列，前两个频道 span 6，第三个 span 12 通栏双列。
- 已知沙盒怪象：含 "shenzhen-stock-era-urban-renewal-misread" 的命令输出会被显示层改写成乱码串，磁盘真实内容以 grep -c 计数验证为准。
