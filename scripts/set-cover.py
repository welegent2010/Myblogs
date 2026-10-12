#!/usr/bin/env python3
"""封面管理：查看或切换文章的封面来源。

封面取值顺序（layouts/partials/func/cover.html）：
    1. front matter 的 image 字段
    2. 正文第一张 markdown 图
    3. 正文第一个 img 短代码
    4. 正文第一个 <img>

用法：
    python3 scripts/set-cover.py                      列出所有文章的封面来源
    python3 scripts/set-cover.py 文旅                 只看标题含关键字的文章
    python3 scripts/set-cover.py 文旅 --first-image   删掉 image 字段，改用正文第一张图
    python3 scripts/set-cover.py 文旅 --url https://img.87188202.xyz/a.png
    python3 scripts/set-cover.py 文旅 --color         删掉 image 字段，改用频道配色块
    python3 scripts/set-cover.py --all --color        所有文章改用频道配色块
"""
import glob
import io
import os
import re
import sys

POSTS = 'content/posts/*.md'


def split_front_matter(text):
    if not text.startswith('---'):
        return text, ''
    parts = text.split('---', 2)
    return parts[2], parts[1]


def get_field(fm, name):
    m = re.search(r'^%s:\s*(.*)$' % name, fm, re.M)
    return m.group(1).strip().strip('"\'') if m else None


def set_field(fm, name, value):
    line = '%s: "%s"\n' % (name, value)
    m = re.search(r'^%s:\s*.*$\n?' % name, fm, re.M)
    if m:
        return fm[:m.start()] + line + fm[m.end():]
    return fm.rstrip('\n') + '\n' + line


def drop_field(fm, name):
    m = re.search(r'^%s:\s*.*$\n?' % name, fm, re.M)
    return fm[:m.start()] + fm[m.end():] if m else fm


def find_first_body_image(body):
    m = re.search(r'!\[[^\]]*\]\(([^)\s]+)', body)
    if m:
        return m.group(1), '正文 markdown 图'
    m = re.search(r'\{\{<\s*img[^>]+src="([^"]+)"', body)
    if m:
        return m.group(1), '正文 img 短代码'
    m = re.search(r'<img[^>]+src="([^"]+)"', body)
    if m:
        return m.group(1), '正文 HTML img'
    return None, '无'


def scan():
    rows = []
    for path in sorted(glob.glob(POSTS)):
        text = io.open(path, encoding='utf-8').read()
        body, fm = split_front_matter(text)
        if not fm:
            continue
        slug = get_field(fm, 'slug') or os.path.basename(path)[:-3]
        fm_img = get_field(fm, 'image')
        body_img, kind = find_first_body_image(body)
        rows.append((slug, fm_img, body_img, kind, path))
    return rows


def show(rows, keyword=None):
    print('%-44s %s' % ('文章 slug', '封面来源'))
    print('-' * 96)
    for slug, fm_img, body_img, kind, path in rows:
        if keyword and keyword not in slug and keyword not in path:
            continue
        if fm_img:
            src = fm_img
            origin = 'front matter image'
        elif body_img:
            src = body_img
            origin = kind
        else:
            src = '（占位块）'
            origin = '无图'
        print('%-44s %s' % (slug[:44], origin))
        print('%-44s   %s' % ('', src[:78]))


def apply_change(rows, keyword, mode, value=None):
    changed = 0
    for slug, fm_img, body_img, kind, path in rows:
        if keyword and keyword not in slug and keyword not in path:
            continue
        text = io.open(path, encoding='utf-8').read()
        body, fm = split_front_matter(text)
        if not fm:
            continue
        if mode in ('first-image', 'color'):
            fm = drop_field(fm, 'image')
        elif mode == 'url':
            fm = set_field(fm, 'image', value)
        new_text = '---' + fm + '---' + body
        io.open(path, 'w', encoding='utf-8').write(new_text)
        changed += 1
        print('已更新:', os.path.basename(path))
    print('\n共修改 %d 篇' % changed)


def main():
    args = sys.argv[1:]
    mode = None
    value = None
    if '--first-image' in args:
        mode = 'first-image'
        args.remove('--first-image')
    if '--url' in args:
        mode = 'url'
        i = args.index('--url')
        value = args[i + 1]
        del args[i:i + 2]
    all_posts = '--all' in args
    if all_posts:
        args.remove('--all')
    keyword = args[0] if args else None

    rows = scan()

    if mode:
        if not (keyword or all_posts):
            print('请指定文章关键字，或加 --all')
            sys.exit(1)
        apply_change(rows, keyword, mode, value)
    else:
        show(rows, keyword)
        print()
        print('切换方式：')
        print('  改用正文第一张图    python3 scripts/set-cover.py 关键字 --first-image')
        print('  改成图床链接        python3 scripts/set-cover.py 关键字 --url https://...')
        print('  改用频道配色块      python3 scripts/set-cover.py 关键字 --color')


if __name__ == '__main__':
    main()
