# -*- coding: utf-8 -*-
"""
banner 替换工具：把生成/外包的 banner 源图按站点规范处理成 1920x1200 webp。

用法：
  1. 把新源图放进 SRC_DIR（默认 .workbuddy/gen-banners/）；
  2. 按需修改下面的 MAPPING（目标名 -> 源文件名）；
  3. python3 tools/process_banners.py
  4. 结果直接覆盖 assets/img/banners/<目标名>.webp，HTML 零改动。

规范：
  - 目标尺寸 1920x1200（8:5），文件名与页面引用同名，webp 质量 82；
  - 自动裁掉源图底部 WATERMARK_CROP_PX 高度（生成模型右下角「AI生成」合规水印带，
    实测水印位于输出 y>=1165，裁掉源图底部 69px 即可全部去除）；
  - 高度不足 1200 时，用图片自身顶边平均色在顶部补齐（页头图顶部均为深色天空，
    补边无缝；页头 dhero 只显示中段横带，补边不可见）。
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT, ".workbuddy", "gen-banners")
OUT_DIR = os.path.join(ROOT, "assets", "img", "banners")

TARGET_W, TARGET_H = 1920, 1200
WATERMARK_CROP_PX = 69          # 源图底部裁掉的高度（去「AI生成」水印）
QUALITY = 82

# 目标文件名 -> 源文件名（本批 2026-10-26 生成的 20 张；换新图时改这里即可）
MAPPING = {
    "biz":                "Aerial_fine_art_photograph_of__2026-10-26T00-30-44.png",
    "products":           "Fine_art_architectural_photogr_2026-10-26T00-30-43.png",
    "scene":              "Long_exposure_fine_art_photogr_2026-10-26T00-30-44.png",
    "about":              "Fine_art_photograph_of_a_long__2026-10-26T00-30-43.png",
    "news":               "Minimalist_fine_art_photograph_2026-10-26T00-30-43.png",
    "area-enterprise":    "Fine_art_photograph_of_a_moder_2026-10-26T00-31-21.png",
    "area-agri":          "Aerial_fine_art_photograph_of__2026-10-26T00-31-20.png",
    "area-asset":         "Fine_art_architectural_photogr_2026-10-26T00-31-19.png",
    "area-procure":       "Fine_art_still_life_photograph_2026-10-26T00-31-21.png",
    "product-etrade":     "A_brass_auction_gavel_resting__2026-10-26T00-31-20.png",
    "product-rural":      "A_small_rural_village_surround_2026-10-26T00-32-12.png",
    "product-software":   "A_single_minimal_software_pack_2026-10-26T00-32-09.png",
    "product-data":       "Glowing_blue_data_light_stream_2026-10-26T00-32-12.png",
    "product-ca":         "A_translucent_glass_sphere_wit_2026-10-26T00-32-12.png",
    "product-blockchain": "Illuminated_glass_cubes_linked_2026-10-26T00-32-12.png",
    "scene-etrade":       "An_empty_modern_auction_hall_w_2026-10-26T00-32-11.png",
    "scene-rural":        "Terraced_rice_fields_at_dusk_w_2026-10-26T00-32-15.png",
    "scene-software":     "A_minimalist_glass_pavilion_in_2026-10-26T00-32-12.png",
    "scene-digital":      "A_futuristic_curved_bridge_wit_2026-10-26T00-32-13.png",
    "scene-data":         "A_fiber_optic_bundle_emitting__2026-10-26T00-32-12.png",
}


def top_avg_color(im, rows=5):
    """取图片顶部 rows 行的平均色，用于补边。"""
    px = im.load()
    w, h = im.size
    r = g = b = 0
    n = 0
    for y in range(min(rows, h)):
        for x in range(w):
            pr, pg, pb = px[x, y]
            r += pr; g += pg; b += pb; n += 1
    return (r // n, g // n, b // n)


def process(name, src_name):
    src = os.path.join(SRC_DIR, src_name)
    im = Image.open(src).convert("RGB")
    w, h = im.size
    # 1) 裁掉底部水印带
    keep_h = h - WATERMARK_CROP_PX
    if keep_h < h:
        im = im.crop((0, 0, w, keep_h))
    # 2) 等比缩放到目标宽
    nw = TARGET_W
    nh = round(im.size[1] * nw / im.size[0])
    im = im.resize((nw, nh), Image.LANCZOS)
    # 3) 高度不足则用顶边色补齐；超出则居中裁到目标高
    if nh < TARGET_H:
        canvas = Image.new("RGB", (nw, TARGET_H), top_avg_color(im))
        canvas.paste(im, (0, TARGET_H - nh))
        im = canvas
    elif nh > TARGET_H:
        top = (nh - TARGET_H) // 2
        im = im.crop((0, top, nw, top + TARGET_H))
    out = os.path.join(OUT_DIR, name + ".webp")
    im.save(out, "WEBP", quality=QUALITY, method=6)
    print("OK %-18s %s  <-  %s" % (name, im.size, src_name))


def main():
    srcs = list(MAPPING.values())
    assert len(srcs) == len(set(srcs)), "MAPPING 源文件名重复"
    for name, src in MAPPING.items():
        path = os.path.join(SRC_DIR, src)
        if not os.path.exists(path):
            raise SystemExit("缺源图: " + path)
    for name, src in MAPPING.items():
        process(name, src)
    print("done: %d banners -> %s" % (len(MAPPING), OUT_DIR))


if __name__ == "__main__":
    main()
