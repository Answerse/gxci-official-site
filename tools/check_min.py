#!/usr/bin/env python3
"""检查 css/*.css 与对应 *.min.css 是否同步（源文件改过但没重新构建就报警）。

页面引用的是 .min.css，源文件仅供阅读与修改。改完 css 忘了跑
`python3 tools/build_min.py`，线上就会是旧样式 —— 这个脚本就是拦这个坑。

用法：python3 tools/check_min.py   退出码 1 表示有不同步文件
"""
import glob
import os
import sys


def main():
    bad = []
    for src in sorted(glob.glob('css/*.css')):
        if src.endswith('.min.css'):
            continue
        dst = src[:-4] + '.min.css'
        if not os.path.exists(dst):
            bad.append((src, '缺少 min 文件'))
            continue
        if os.path.getmtime(src) > os.path.getmtime(dst) + 1:
            bad.append((src, '源文件比 min 新'))
    if bad:
        print('以下 CSS 需要重新构建（python3 tools/build_min.py）：')
        for f, why in bad:
            print('  %-20s %s' % (f, why))
        return 1
    print('CSS 源文件与 min 产物同步。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
