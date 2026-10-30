#!/usr/bin/env python3
"""把 banners/*.webp 统一染成标准色系深蓝双色调。
用法：
  python3 tint_banners.py preview   # 只处理 3 张样张到 /tmp/tint-preview
  python3 tint_banners.py apply     # 全量覆盖 assets/img/banners/*.webp
  python3 tint_banners.py stats     # 输出各图平均色/亮度（数字校验，不读图）
"""
import os, sys, glob
from PIL import Image, ImageOps, ImageEnhance

SRC = 'assets/img/banners'
# 深蓝 duotone：暗部 → 深群青夜色，中调 → 标准色，亮部 → 冷蓝白
DARK  = (26, 40, 106)     # #1a286a 深群青（不再接近黑）
MID   = (54, 76, 172)     # #364cac 标准色提亮一档
LIGHT = (171, 189, 228)   # #abbde4 冷蓝（压住亮部，避免发灰发紫）

def lut():
    r, g, b = [], [], []
    for i in range(256):
        t = i / 255.0
        if t < 0.5:
            k = t / 0.5
            c = (DARK[k2] * (1 - k) + MID[k2] * k for k2 in range(3))
        else:
            k = (t - 0.5) / 0.5
            c = (MID[k2] * (1 - k) + LIGHT[k2] * k for k2 in range(3))
        cr, cg, cb = list(c)
        r.append(int(cr)); g.append(int(cg)); b.append(int(cb))
    return (r, g, b)

LUT = lut()

def tint(im, mix=0.88):
    """保留原图明暗层次，只把色相统一压到标准蓝并适度提亮。
    比 duotone 更能留住建筑结构／玻璃反光／城市灯点，不会糊成一片。"""
    src = im.convert('RGB')
    g0 = src.convert('L')
    l0 = sum(g0.resize((48, 30)).getdata()) / (48 * 30)
    lift = 1.52 if l0 < 40 else (1.34 if l0 < 60 else (1.10 if l0 < 90 else 0.96))
    gamma = 0.62 if l0 < 40 else (0.72 if l0 < 60 else (0.86 if l0 < 90 else 0.95))

    hsv = src.convert('HSV')
    _, sat, val = hsv.split()
    hue = Image.new('L', src.size, 164)                     # 164/255≈232°，标准色相
    sat = sat.point(lambda x: min(255, int(x * 0.42 + 92)))   # 饱和下限：标准群青，不发荧光
    vmin = 104 if l0 < 26 else (82 if l0 < 42 else 62)
    val = val.point(lambda x: min(255, max(vmin, int(255 * (((x / 255.0) ** gamma) * lift)))))
    blue = Image.merge('HSV', (hue, sat, val)).convert('RGB')
    return Image.blend(blue, src, 1 - mix)

def stat(im):
    small = im.resize((64, 40))
    px = list(small.getdata())
    n = len(px)
    avg = tuple(round(sum(p[i] for p in px) / n) for i in range(3))
    lum = round(0.2126 * avg[0] + 0.7152 * avg[1] + 0.0722 * avg[2])
    return avg, lum

def run(apply_):
    files = sorted(glob.glob(os.path.join(SRC, '*.webp')))
    for f in files:
        im = Image.open(f).convert('RGB')
        out = tint(im)
        avg0, lum0 = stat(im)
        avg1, lum1 = stat(out)
        name = os.path.basename(f)
        if apply_:
            out.save(f, 'WEBP', quality=86, method=6)
        print(f'{name:26s} 原 rgb{avg0} L{lum0} → 蓝 rgb{avg1} L{lum1}')

def preview():
    os.makedirs('/tmp/tint-preview', exist_ok=True)
    picks = ['biz.webp', 'scene-etrade.webp', 'product-ca.webp']
    for p in picks:
        im = Image.open(os.path.join(SRC, p)).convert('RGB')
        tint(im).resize((640, 400)).save('/tmp/tint-preview/' + p.replace('.webp', '.jpg'), quality=88)
    # 拼一张总览：上排原 3 张，下排染色 3 张
    tiles = []
    for p in picks:
        tiles.append(Image.open(os.path.join(SRC, p)).convert('RGB').resize((430, 269)))
        tiles.append(Image.open('/tmp/tint-preview/' + p.replace('.webp', '.jpg')).resize((430, 269)))
    sheet = Image.new('RGB', (430 * 3 + 16, 269 * 2 + 8), (255, 255, 255))
    for i, t in enumerate(tiles[:3]):
        sheet.paste(t, (i * 436, 0))
    for i, t in enumerate(tiles[3:]):
        sheet.paste(t, (i * 436, 277))
    sheet.save('/tmp/tint-preview/sheet.jpg', quality=88)
    print('sheet -> /tmp/tint-preview/sheet.jpg')

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stats'
    {'preview': preview, 'apply': lambda: run(True), 'stats': lambda: run(False)}[cmd]()
