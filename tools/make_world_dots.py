#!/usr/bin/env python3
"""生成点阵世界地图底纹（首页业务领域板块背景）。

数据源：world-atlas 的 land-110m.json（TopoJSON，Natural Earth 1:110m）。
不依赖任何第三方库，只用标准库 + 一次下载；生成结果提交进仓库，构建时不再联网。

两张图，因为同一点径在手机和桌面上的视觉差别极大：
  world-dots.svg     pattern 4.4 / r .75  → 桌面宽 1720px 时点距 7.6、点径 2.6
  world-dots-sm.svg  pattern 7.6 / r 1.7  → 手机宽 600px 时点距 4.6、点径 2.0

用法：python3 tools/make_world_dots.py [--cache /tmp/land110.json]
"""
import json
import os
import sys
import urllib.request

SRC_URL = "https://cdn.jsdelivr.net/npm/world-atlas@2/land-110m.json"
CACHE = "/tmp/land110.json"

# 画布：等距圆柱投影，纬度裁到 86..-8（南极洲不要，北极点在 110m 数据里本就到 83.6）
# 这两张图从 V176 起是「贴在板块底部」的带状底纹，底边与板块底边齐平，
# 所以下界取 -8：让赤道一带（刚果、亚马逊、印尼）压住底线，
# 底线才不会落在南大洋的空海面上（原来是 -58，底部整条没有点）。
W = 1000.0
LAT_TOP, LAT_BOT = 86.0, -8.0
H = (LAT_TOP - LAT_BOT) / 360.0 * W

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets/img/deco")


def load():
    if not os.path.exists(CACHE):
        print("downloading", SRC_URL)
        urllib.request.urlretrieve(SRC_URL, CACHE)
    return json.load(open(CACHE))


def rings_of(d):
    """TopoJSON → 经纬度环列表。弧段是 delta 编码，负索引表示反向。"""
    sx, sy = d["transform"]["scale"]
    tx, ty = d["transform"]["translate"]
    arcs = []
    for arc in d["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)

    out = []
    for g in d["objects"]["land"]["geometries"]:
        for poly in g["arcs"]:
            for ring in poly:
                pts = []
                for i in ring:
                    a = arcs[~i][::-1] if i < 0 else arcs[i]
                    pts.extend(a[1:] if pts else a)
                out.append(pts)
    return out


def unwrap(pts):
    """消除跨 180 经线的跳变，让相邻点经度连续。"""
    out = [list(pts[0])]
    for lon, lat in pts[1:]:
        prev = out[-1][0]
        while lon - prev > 180:
            lon -= 360
        while lon - prev < -180:
            lon += 360
        out.append([lon, lat])
    return out


def _clip(pts, inside, isect):
    out = []
    n = len(pts)
    for i in range(n):
        cur, prev = pts[i], pts[i - 1]
        ci, pi = inside(cur), inside(prev)
        if ci:
            if not pi:
                out.append(isect(prev, cur))
            out.append(cur)
        elif pi:
            out.append(isect(prev, cur))
    return out


def clip_lon(pts, lo=-180.0, hi=180.0):
    r = _clip(pts, lambda p: p[0] >= lo,
              lambda a, b: (lo, a[1] + (b[1] - a[1]) * (lo - a[0]) / (b[0] - a[0])))
    if not r:
        return []
    return _clip(r, lambda p: p[0] <= hi,
                 lambda a, b: (hi, a[1] + (b[1] - a[1]) * (hi - a[0]) / (b[0] - a[0])))


def clip_lat(pts, lo=LAT_BOT, hi=LAT_TOP):
    r = _clip(pts, lambda p: p[1] >= lo,
              lambda a, b: (a[0] + (b[0] - a[0]) * (lo - a[1]) / (b[1] - a[1]), lo))
    if not r:
        return []
    return _clip(r, lambda p: p[1] <= hi,
                 lambda a, b: (a[0] + (b[0] - a[0]) * (hi - a[1]) / (b[1] - a[1]), hi))


def project(lon, lat):
    return (lon + 180.0) / 360.0 * W, (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * H


def build_path(rings):
    kept = []
    for r in rings:
        if len(r) < 4:
            continue
        u = unwrap(r)
        lons = [p[0] for p in u]
        # 跨日期变更线的碎片（弗兰格尔岛、斐济）在数据里带 ±180 端点，
        # 一 unwrap 就变成一条横穿整幅的细线；体量只有几像素，直接丢
        if max(lons) - min(lons) > 300 and len(u) < 20:
            continue
        # 被简化成又长又薄一条的碎片（阿留申等），点阵化后只是一根线
        lats = [p[1] for p in u]
        if max(lons) - min(lons) > 18 and max(lats) - min(lats) < 0.7:
            continue
        shifts = [-360.0, 0.0, 360.0] if (min(lons) < -180 or max(lons) > 180) else [0.0]
        for s in shifts:
            c = clip_lon([[p[0] + s, p[1]] for p in u])
            if len(c) >= 3:
                c = clip_lat(c)
                if len(c) >= 3:
                    kept.append(c)

    d = []
    for pts in kept:
        d.append("".join(
            ("M" if i == 0 else "L") + "%.1f %.1f" % project(lon, lat)
            for i, (lon, lat) in enumerate(pts)) + "Z")
    return "".join(d), len(kept)


def svg(d, step, radius, color):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %.0f" width="%.0f" height="%.0f" '
        'role="img" aria-hidden="true">\n<defs>\n<path id="ld" fill="#fff" fill-rule="evenodd" d="%s"/>\n'
        '<pattern id="wd" width="%s" height="%s" patternUnits="userSpaceOnUse">\n'
        '<circle cx="%s" cy="%s" r="%s" fill="%s"/>\n</pattern>\n'
        '<mask id="wl" maskUnits="userSpaceOnUse" x="0" y="0" width="%.0f" height="%.0f">\n'
        '<use href="#ld"/>\n</mask>\n</defs>\n'
        '<rect width="%.0f" height="%.0f" fill="url(#wd)" mask="url(#wl)"/>\n</svg>\n'
    ) % (W, H, W, H, d, step, step, step / 2, step / 2, radius, color, W, H, W, H)


def main():
    d, n = build_path(rings_of(load()))
    print("rings kept:", n, " path KB:", round(len(d) / 1024, 1))
    os.makedirs(OUT_DIR, exist_ok=True)

    specs = [
        ("world-dots.svg", 4.4, 0.75, "#95a2b4"),
        ("world-dots-sm.svg", 7.6, 1.70, "#95a2b4"),
    ]
    for name, step, r, color in specs:
        out = svg(d, step, r, color)
        with open(os.path.join(OUT_DIR, name), "w", encoding="utf-8") as f:
            f.write(out)
        print(name, round(len(out) / 1024, 1), "KB")


if __name__ == "__main__":
    sys.exit(main())
