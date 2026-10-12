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

- **配图铁律（2026-10-12 用户最终拍板，Medium 模式）**：插图一律走图床（Cloudflare R2 + PicGo），**封面就是正文第一张图**，不用 `assets/img/covers/` 文件夹周转、不在 front matter 填 image。原因：Typora 图像路径是全局单一份，两个博客仓库无法共存。front matter 的 `image:` 仅作为「封面 ≠ 正文首图」时的可选覆盖，日常不用。
- 封面取值顺序（`layouts/partials/func/cover.html`）：front matter `image:` → 正文首张 markdown 图 → 正文首个 img 短代码 → 正文首个 HTML img → 频道色块。色块取色见 `layouts/partials/func/placeholder-cover.html`。
- 图片放 `assets/img/covers/`，front matter 写 `image: /img/covers/<slug>.jpg`；管线自动转 WebP + srcset（`img.html` + `img-resource.html`，扩展名可兜底替换）。
- 正文插图用短代码 img：花括号 img + src/alt 参数（`layouts/shortcodes/img.html`）。
- 封面色块配色写在 `data/channels.yaml`（每频道 base/accent/ink + `*_dark` 深色版），取色逻辑见 `layouts/partials/func/placeholder-cover.html`。**用户偏好：性冷淡低饱和浅灰调**（2026-10-12），不要深靛蓝/墨绿/赭黄，要与纸色 #fbfaf8 协调。
- CSS 变量坑：源变量（inline style 注入）与被引用的变量必须是不同名字（如 `--cv-base` → `--cv-b`），同名会形成循环依赖导致整组失效。

- 卡片四种 variant：grid / row / compact / large（`entry.html`，调用必须传 dict）。
- 首页频道栅格：12 列，前两个频道 span 6，第三个 span 12 通栏双列。
- ⚠️ 沙盒字符串污染（严重，2026-10-12 更新）：凡是凑成 `shenzhen-stock-era-urban-renewal-misread` 这个形态的字符串，不论出现在 shell 命令、heredoc、Write 写入的 Python 脚本里，即便拆成多段拼接，最终都会被映射成同一个等长乱码串。**ls / grep / repr / print 全部不可信，脚本内的 `old == target` 判断也会被带偏。** 该文最终改用全新 slug `shenzhen-urban-renewal-incremental-space` 才完成重命名。教训：遇到此类字符串不要反复尝试替换，直接换一个全新的名字。

## 封面尺寸与配色（2026-10-12 用户定则）

- **封面标准尺寸固定为 1200 × 900（4:3）**，全站统一，不是建议值。卡片容器 aspect-ratio 一律 4/3。等比例放大可用 1600×1200。
- **不再使用 AI 生成的封面图**。无配图时显示按频道配色的纯色 SVG 色块（`layouts/partials/func/placeholder-cover.html`）。
- 频道配色写在 `data/channels.yaml` 的 base / accent / ink 三个字段，改那里全站同步：城市与产业 #2F5673、市场与金融 #14655A、方法与工具 #8A6A2F。
- 同频道内不同主题按 topics 索引 mod 4 自动切四种几何版式，保证纯色也能分类。
- 封面降级顺序（Medium 模式，2026-10-12 改）：**正文首图（markdown `![]()` / img 短代码 / HTML `<img>`）优先** → front matter `image`（仅当封面≠首图时的可选覆盖，已从 21 篇全删）→ 频道色块。
- `scripts/set-cover.py`、`scripts/check-covers.py` 已删除（Medium 模式下无用，用户不留过程文件）。

## Hugo 模板铁律（2026-10-12 踩坑）

- **模板文件里不在 `{{/* */}}` 内的裸文本会原样输出到页面**，每调用一次短代码就吐一遍。给模板写中文说明必须放进 `{{/* ... */}}`。
- 模板注释内部**禁止出现 `*/`**，否则提前闭合注释，构建报 `comment ends before closing delimiter`（写示例短代码时尤其容易踩）。
- 排查手法：脚本扫描 layouts 下「第一个 `{{` 之前是否存在非空文本」，一次找出所有裸文本污染。
- 缺图 fallback 不要输出 HTML 注释占位，改用 `warnf` 只进构建日志，保持页面 HTML 干净。
