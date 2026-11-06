#!/usr/bin/env python3
"""把 css/*.css 生成为同名 *.min.css —— 去注释 + 折叠多余空白。

为什么需要：线上静态托管没有开 gzip，CSS 是原字节数传输。三份 CSS 原始
145.6KB，压缩后 86.6KB（-40%），这是目前唯一实打实的传输优化。

安全边界（改这个脚本前先读）：
- 只折叠「连续空格/制表符」为单个空格，不删单个空格 —— `calc(100vh - var(--footh))`
  这类表达式靠空格分隔，删了就失效。
- 只删 `/* ... */` 注释，不碰 `content:"..."` 里的内容（实测三份 CSS 里没有
  含多个空格的 content 字符串，也没有带空格的 url()）。
- 源文件保持可读，页面引用 .min；改完源文件务必重新跑本脚本，否则线上是旧样式。
  `tools/check_min.py` 会比对 mtime 并列出不同步的文件。

用法：python3 tools/build_min.py
"""
import glob
import os
import re


def minify_css(s):
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r'\s*\n\s*', '\n', s)
    s = re.sub(r'\n+', '\n', s)
    s = re.sub(r'\s*([{};,])\s*', r'\1', s)
    return s.strip() + '\n'


def main():
    total0 = total1 = 0
    for src in sorted(glob.glob('css/*.css')):
        if src.endswith('.min.css'):
            continue
        s = open(src, encoding='utf-8').read()
        out = minify_css(s)
        dst = src[:-4] + '.min.css'
        open(dst, 'w', encoding='utf-8').write(out)
        b0, b1 = len(s.encode()), len(out.encode())
        total0 += b0
        total1 += b1
        print('%-18s %7d -> %7d B  (-%d%%)  -> %s'
              % (src, b0, b1, round((1 - b1 / b0) * 100), dst))
    if total0:
        print('合计 %d -> %d B，省 %.1f KB' % (total0, total1, (total0 - total1) / 1024))


if __name__ == '__main__':
    main()
