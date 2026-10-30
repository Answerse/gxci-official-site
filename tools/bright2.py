#!/usr/bin/env python3
"""banner 统一调色：提亮到正常照片亮度 + 轻微品牌蓝调，高光软压缩不截断。

用法:
  python bright2.py preview <out_dir>     # 出 2-3 张样张
  python bright2.py apply                 # 全量重出（从原始未调色源恢复）
  python bright2.py stats                 # 只打印当前亮度统计
"""
import glob
import os
import sys

import numpy as np
from PIL import Image

BK = '.workbuddy/backup/v59-20261022-181419'          # 未调色的原始 webp
BD = 'assets/img/banners'

# 输出名 -> 原始源（备份里的原图 / 新生成未调色的 PNG）
SRC_MAP = {
    'area-enterprise': BK + '/area-data.webp',
    'area-asset':      BK + '/area-trade.webp',
    'area-agri':       BD + '/Fine_art_aerial_photograph_of__2026-10-23T03-44-20.png',
    'area-procure':    BD + '/Bright_daylight_editorial_phot_2026-10-23T04-41-48.png',
}

SRGB_TO_LIN = np.array([0.04045], dtype=np.float32)


def to_linear(a):
    return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)


def to_srgb(a):
    a = np.clip(a, 0.0, 1.0)
    return np.where(a <= 0.0031308, a * 12.92, 1.055 * a ** (1 / 2.4) - 0.055)


def bright(im, target=0.300, shadow_tint=(0.93, 0.975, 1.075), tint_amt=0.34):
    """target 为线性光下的平均相对亮度（0.30 ≈ sRGB L 约 140）。"""
    a = np.asarray(im.convert('RGB')).astype(np.float32) / 255.0
    lin = to_linear(a)
    lum = 0.2126 * lin[:, :, 0] + 0.7152 * lin[:, :, 1] + 0.0722 * lin[:, :, 2]
    gain = target / max(float(lum.mean()), 0.004)

    lin = lin * gain
    # 高光软压缩：接近 1 时平滑收住，不出现硬边裁切
    lin = 1.0 - np.exp(-lin * 1.06)

    # 轻微提饱和，抵消后续 tint 的灰感
    l2 = (0.2126 * lin[:, :, 0] + 0.7152 * lin[:, :, 1] + 0.0722 * lin[:, :, 2])[:, :, None]
    lin = l2 + (lin - l2) * 1.06

    # 暗部蓝调（split-tone），亮部保持中性
    out = to_srgb(lin)
    w = np.clip(1.0 - (0.2126 * out[:, :, 0] + 0.7152 * out[:, :, 1] + 0.0722 * out[:, :, 2]), 0, 1)
    w = (w ** 1.4)[:, :, None] * tint_amt
    tinted = out * np.array(shadow_tint, dtype=np.float32)
    out = out * (1 - w) + tinted * w

    return Image.fromarray(np.clip(out * 255, 0, 255).astype(np.uint8))


def stat(img):
    s = img.convert('RGB').resize((64, 40))
    px = np.asarray(s).astype(np.float32).reshape(-1, 3)
    avg = tuple(round(float(v)) for v in px.mean(axis=0))
    L = round(0.2126 * avg[0] + 0.7152 * avg[1] + 0.0722 * avg[2])
    big = np.asarray(img.convert('RGB').resize((160, 100))).astype(np.float32)
    clip = round(float((big.max(axis=2) >= 252).mean()) * 100, 1)
    return L, avg, clip


def sources():
    m = dict(SRC_MAP)
    for f in sorted(glob.glob(BK + '/*.webp')):
        n = os.path.basename(f)[:-5]
        m.setdefault(n, f)
    return m


TARGET_L = 138


def render(im, target_l=TARGET_L):
    """按目标平均亮度迭代两次，抵消高光软压缩带来的整体变暗。"""
    t = 0.30
    out = bright(im, target=t)
    for _ in range(2):
        cur = stat(out)[0]
        if abs(cur - target_l) <= 3:
            break
        t *= (target_l / max(cur, 20)) ** 1.85
        out = bright(im, target=min(t, 1.4))
    return out


def apply_all(target=TARGET_L):
    rows = []
    for name, src in sources().items():
        im = Image.open(src)
        w, h = im.size
        if im.format == 'PNG':
            im = im.crop((0, 0, w, h - 58))            # 去掉生图右下角「AI生成」水印
        b = render(im, target).resize((1920, 1200), Image.LANCZOS)
        dst = 'assets/img/banner-first.webp' if name == 'banner-first' else f'{BD}/{name}.webp'
        b.save(dst, 'WEBP', quality=86, method=6)
        L, avg, clip = stat(b)
        rows.append((name, L, avg, clip))
        print(f'{name:26s} L{L:3d} rgb{avg} clip{clip}%')
    Ls = [r[1] for r in rows]
    print(f'--- {len(rows)} 张  L {min(Ls)}–{max(Ls)}')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stats'
    if cmd == 'apply':
        apply_all(float(sys.argv[2]) if len(sys.argv) > 2 else TARGET_L)
    elif cmd == 'preview':
        out = sys.argv[2] if len(sys.argv) > 2 else '/tmp/b2'
        os.makedirs(out, exist_ok=True)
        picks = ['biz', 'area-agri', 'area-procure', 'scene-digital']
        tiles = []
        for n in picks:
            im = Image.open(sources()[n])
            b = bright(im)
            b.save(f'{out}/{n}.jpg', quality=88)
            tiles.append(b.resize((520, 325)))
        sheet = Image.new('RGB', (520 * 2 + 12, 325 * 2 + 12), (255, 255, 255))
        for i, t in enumerate(tiles):
            sheet.paste(t, ((i % 2) * 532, (i // 2) * 337))
        sheet.save(f'{out}/sheet.jpg', quality=86)
        print('preview ->', out)
    else:
        for f in sorted(glob.glob(BD + '/*.webp')) + ['assets/img/banner-first.webp']:
            L, avg, clip = stat(Image.open(f))
            print(f'{os.path.basename(f):30s} L{L:3d} rgb{avg} clip{clip}%')
