#!/usr/bin/env python3
"""从彩色 logo 位图生成纯白反白 SVG（党建模块页头用）。

用法：python3 tools/make_logo_white.py
输出：assets/img/logo-white.svg

做法：alpha 通道高斯平滑去阶梯 → 阈值取不透明区域 → cv2 找轮廓（含孔洞）
→ approxPolyDP 抽稀成多边形 → 合成单条 fill-rule=evenodd 的白色 path。
单一形状 + 单一填充色，所以不会出现两层之间的缝隙；镂空部分直接透明，
露出页面底色（深红 banner），这才是反白 logo 该有的样子。

如果日后拿到 Figma 源 SVG，直接覆盖 assets/img/logo-white.svg 即可，
页面用的是 <img src>，不依赖本脚本产物的任何内部结构。
"""
import os
import numpy as np
import cv2
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'assets/img/_img_index_bbw-logo.png')
OUT = os.path.join(ROOT, 'assets/img/logo-white.svg')

S = 1600          # 矢量图坐标系边长（与显示尺寸无关，靠 CSS 缩放）
ALPHA_SIGMA = 2.0
EDGE_SIGMA = 1.5
EPS = 1.0         # approxPolyDP 容差，越小越贴合、文件越大
MIN_AREA = 30


def contours_to_path(mask):
    segs = []
    cnts, _ = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    for c in cnts:
        if cv2.contourArea(c) < MIN_AREA:
            continue
        ap = cv2.approxPolyDP(c, EPS, True).reshape(-1, 2)
        if len(ap) < 3:
            continue
        segs.append('M' + 'L'.join('%g %g' % (x, y) for x, y in ap) + 'Z')
    return ' '.join(segs)


def main():
    im = Image.open(SRC).convert('RGBA').resize((S, S), Image.LANCZOS)
    alpha = cv2.GaussianBlur(np.array(im)[..., 3].astype(np.float32), (0, 0), ALPHA_SIGMA)
    m = np.where(alpha > 127.5, 255, 0).astype(np.uint8)
    m = cv2.GaussianBlur(m, (0, 0), EDGE_SIGMA)
    m = (m > 127).astype(np.uint8) * 255

    d = contours_to_path(m)
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
           'role="img" aria-label="广西计算机有限责任公司">'
           '<path fill="#fff" fill-rule="evenodd" d="%s"/></svg>') % (S, S, d)
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(svg)
    print('wrote %s  (%d bytes)' % (OUT, len(svg)))


if __name__ == '__main__':
    main()
