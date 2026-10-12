#!/usr/bin/env python3
"""封面尺寸体检：检查图片是否符合 1200x900（4:3，即 1.333）。

用法：
    python3 scripts/check-covers.py            # 检查 assets/img/covers/ 目录
    python3 scripts/check-covers.py 图.png     # 检查指定文件

判定（距 1.333 的相对偏差）：
    < 2%  OK      直接用，几乎零裁切
    < 12% 偏差    能用，cover 会裁掉一部分
    更大  严重    建议重做或裁剪

需要 pillow：pip install pillow
"""
import glob
import os
import sys

try:
    from PIL import Image
except ImportError:
    print('缺少 pillow：请先 pip install pillow')
    sys.exit(1)

TARGET = 1.3333333


def check(path):
    im = Image.open(path)
    w, h = im.size
    r = w / h
    d = abs(r - TARGET) / TARGET * 100
    if d < 2:
        flag = 'OK'
    elif d < 12:
        flag = '偏差'
    else:
        flag = '严重'
    print('%-52s %-12s %-7.3f %5.1f%%  %s' % (
        os.path.basename(path), '%dx%d' % (w, h), r, d, flag))
    return flag


def main():
    args = sys.argv[1:]
    files = args or sorted(glob.glob('assets/img/covers/*.jpg')) \
        + sorted(glob.glob('assets/img/covers/*.webp'))
    if not files:
        print('未找到图片')
        sys.exit(1)

    bad = 0
    for f in files:
        if check(f) != 'OK':
            bad += 1
    print()
    print('标准尺寸 1200x900，比例 4:3 = 1.333；等比例可用 1600x1200 / 800x600')
    print('结果：%d 张中 %d 张需注意' % (len(files), bad))


if __name__ == '__main__':
    main()
