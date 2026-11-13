# -*- coding: utf-8 -*-
"""生成茧易通详情页架构图：桌面横版 jyt-arch.svg / 移动竖版 jyt-arch-m.svg。

V359 清晰版（用户反馈「一点都不清晰」后重画）：
  - 上半区只讲「四个端各自管什么、共同围着平台」：单层椭圆环 + 四端胶囊压环
    + 中心枢纽 + 四个象限内的功能名（图标 + 原文功能名）。
  - 下半区只讲「业务流程」：四步蓝胶囊 + 三个箭头，胶囊上方标原文端名。
  - 两区靠留白分隔，不画装饰线；**没有虚线环、点线、凭证小字、重复端名**。
  - 桌面设计宽度 1040 = 页面实际显示宽度，1:1 不缩放，最小字号 16px。

图内所有文字只来自两处：
  1) /Users/answerose/Downloads/茧易通功能说明.docx —— 8 个功能名、4 个端名；
  2) 页面已有标题「茧易通」。
不写概括性标签、不写装饰序号、不编数据；所有连线都是语义连线。
改坐标请改本脚本重跑，别手改 SVG。
"""
import zipfile
import re
import html
import os
from xml.etree import ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCX = '/Users/answerose/Downloads/茧易通功能说明.docx'
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

BLUE = '#2b3a92'
INK = '#141414'
MUT = '#8a8a8a'
FONT = ("'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Source Han Sans SC',"
        "'Noto Sans CJK SC',system-ui,sans-serif")


def para_text(p):
    out = []
    for el in p.iter():
        if el.tag == W + 't':
            out.append(el.text or '')
        elif el.tag == W + 'br':
            out.append('\n')
    return ''.join(out)


def read_docx():
    body = ET.fromstring(zipfile.ZipFile(DOCX).read('word/document.xml')).find(W + 'body')
    items = []
    for t in (para_text(p) for p in body.findall(W + 'p')):
        if not t.strip():
            continue
        for ln in [x.strip() for x in t.split('\n') if x.strip()]:
            m = re.match(r'^\d+[\.、]\s*(.+?)\s*[｜|]\s*(\S+)\s*/\s*(\S+)\s*$', ln)
            if m:
                items.append({'name': m.group(1), 'end': m.group(2), 'cat': m.group(3), 'desc': ''})
            elif items and not items[-1]['desc']:
                items[-1]['desc'] = ln
    assert len(items) == 8 and all(i['desc'] for i in items), 'docx 解析不完整'
    return items


def E(s):
    return html.escape(s, quote=False)


def T(x, y, s, size=20, fill=INK, weight=400, anchor='middle', op=None):
    a = (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
         f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"')
    if op:
        a += f' opacity="{op}"'
    return a + '>' + E(s) + '</text>'


# 与页面卡片共用的 8 枚线性图标
ICON = [
    '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4"/><path d="M8.5 14l2.2 2.2 4.3-4.4"/>',
    '<rect x="6" y="3" width="12" height="18" rx="2"/><path d="M9 8h6M9 12h6M9 16h3.5"/>',
    '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18M6.5 14h3.5"/>'
    '<path d="M13 14h5m-2.5-2.5L18 14l-2.5 2.5"/>',
    '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M4 9h16M4 15h16M10 9v12"/>',
    '<path d="M3 19l5-5 4 3 6-8"/><path d="M15 9h3v3"/><path d="M3 21h18"/>',
    '<path d="M3.5 17a8.5 8.5 0 0 1 17 0"/><path d="M12 17l4-5"/>'
    '<circle cx="12" cy="17" r="1"/><path d="M3 21h18"/>',
    '<circle cx="9" cy="8" r="3"/><path d="M3.5 20c0-3 2.5-5.5 5.5-5.5s5.5 2.5 5.5 5.5"/>'
    '<path d="M16 12h5M16 16h3.5"/>',
    '<circle cx="12" cy="5.5" r="2.2"/><circle cx="5" cy="18.5" r="2.2"/>'
    '<circle cx="19" cy="18.5" r="2.2"/><path d="M12 7.7v3.8M6.6 16.6l3.8-4M17.4 16.6l-3.8-4"/>',
]


def make_helpers(items):
    idx = {it['name']: k for k, it in enumerate(items)}

    def icon(x, y, name, scale=.95, op='.85'):
        return (f'<g transform="translate({x},{y}) scale({scale})" fill="none" stroke="{BLUE}" '
                f'stroke-opacity="{op}" stroke-width="1.8" stroke-linecap="round" '
                f'stroke-linejoin="round">{ICON[idx[name]]}</g>')

    return icon


def head(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
            f'height="{h}" role="img" aria-label="茧易通四个端与业务流程架构图">\n')


def ring(cx, cy, rx, ry, op=.3, sw=1.5):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{BLUE}" '
            f'stroke-opacity="{op}" stroke-width="{sw}"/>\n')


def hub(cx, cy, r, fs):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{BLUE}" '
            f'stroke-opacity=".42" stroke-width="1.5"/>\n'
            + T(cx, cy + fs * .35, '茧易通', fs, BLUE, 700))


def cap(cx, cy, txt, w=132, h=40, fs=21):
    return (f'<rect x="{cx-w/2:g}" y="{cy-h/2:g}" width="{w}" height="{h}" rx="{h/2:g}" '
            f'fill="#fff" stroke="{BLUE}" stroke-opacity=".55" stroke-width="1.3"/>\n'
            + T(f'{cx:g}', cy + fs * .35, txt, fs, BLUE, 600))


def bluecap(cx, cy, txt, w, h, fs):
    return (f'<rect x="{cx-w/2:g}" y="{cy-h/2:g}" width="{w}" height="{h}" rx="{h/2:g}" '
            f'fill="{BLUE}"/>\n'
            + T(f'{cx:g}', cy + fs * .36, txt, fs, '#fff', 600))


def arrow_h(x1, x2, y, op='.7'):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{BLUE}" '
            f'stroke-opacity="{op}" stroke-width="1.8"/>\n'
            f'<path d="M{x2-7} {y-5} L{x2} {y} L{x2-7} {y+5} Z" fill="{BLUE}" '
            f'fill-opacity="{op}"/>\n')


def arrow_v(x, y1, y2, op='.7'):
    return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{BLUE}" '
            f'stroke-opacity="{op}" stroke-width="1.8"/>\n'
            f'<path d="M{x-5} {y2-7} L{x} {y2} L{x+5} {y2-7} Z" fill="{BLUE}" '
            f'fill-opacity="{op}"/>\n')


def feature(icon, ix, iy, tx, ty, name, fs, scale):
    """图标 + 原文功能名，文字左对齐。"""
    return icon(ix, iy, name, scale) + T(tx, ty, name, fs, INK, 600, 'start')


def by_end(items, end):
    return [it['name'] for it in items if it['end'] == end]


def build_wide(items, icon):
    """1040 × 640：上＝四端与功能归属（单层环 + 中心枢纽），下＝四步业务流程。"""
    o = [head(1040, 640)]
    o.append(ring(520, 222, 478, 180, .30))
    o.append(hub(520, 222, 74, 30))

    # 四个端胶囊压在椭圆环的四个象限点上
    for x, y, t in [(330, 58, '农户端'), (710, 58, '企业端'),
                    (330, 386, '管理端'), (710, 386, '平台端')]:
        o.append(cap(x, y, t))

    # 左上：农户端功能；右上：企业端功能（2×2）；左下/右下各一项
    f = by_end(items, '农户端')
    for k, name in enumerate(f):
        o.append(feature(icon, 118, 121 + 42 * k, 150, 140 + 42 * k, name, 20, .95))
    f = by_end(items, '企业端')
    for k, name in enumerate(f):
        col, row = k % 2, k // 2
        o.append(feature(icon, 596 + 184 * col, 121 + 42 * row,
                         628 + 184 * col, 140 + 42 * row, name, 20, .95))
    o.append(feature(icon, 118, 281, 150, 300, by_end(items, '管理端')[0], 20, .95))
    # 右下项右移，避免图标贴到中心圆右缘
    o.append(feature(icon, 620, 281, 652, 300, by_end(items, '平台端')[0], 20, .95))

    # 业务流程：端名（原文词）+ 蓝胶囊 + 箭头；不加凭证小字
    chain = items[:4]
    xs = [145, 395, 645, 895]
    for cx, it in zip(xs, chain):
        o.append(T(cx, 486, it['end'], 18, MUT))
        o.append(bluecap(cx, 540, it['name'], 206, 54, 22))
    for k in range(3):
        o.append(arrow_h(256 + 250 * k, 288 + 250 * k, 540))
    o.append('</svg>\n')
    return ''.join(o)


def build_mobile(items, icon):
    """390 × 1020：中心枢纽 + 四端分组（环内，紧凑排布）→ 竖向四步流程（环外）。"""
    v = [head(390, 1020)]
    # 缩小椭圆，消除环内下半部的大空白
    v.append(ring(195, 300, 182, 250, .28, 1.4))
    v.append(hub(195, 50, 44, 24))

    # 四端 2×2：胶囊 + 该端功能名（图标 + 原文功能名）
    # 左列右移 22px：原 x=32 的图标会压在椭圆环线上
    ends = [(100, 140, '农户端', 54, 80, [185, 219]),
            (290, 140, '企业端', 212, 238, [185, 219, 253, 287]),
            (100, 380, '管理端', 54, 80, [425]),
            (290, 380, '平台端', 212, 238, [425])]
    for cx, cy, end, ix, tx, ys in ends:
        v.append(cap(cx, cy, end, 116, 36, 19))
        for k, name in enumerate(by_end(items, end)):
            v.append(feature(icon, ix, ys[k] - 16, tx, ys[k], name, 18, .85))

    # 竖向业务流程（环下缘 550，留白 70 后起）。
    # 手机不重复标端名：胶囊间距要留给箭头，端名与箭头会互相挤；
    # 端名在桌面图与下方卡片里都有，此处只保留四步功能名与箭头。
    chain = items[:4]
    for k, it in enumerate(chain):
        cy = 660 + 90 * k
        v.append(bluecap(195, cy, it['name'], 290, 52, 21))
        if k < 3:
            v.append(arrow_v(195, cy + 30, cy + 55))
    v.append('</svg>\n')
    return ''.join(v)


def main():
    items = read_docx()
    icon = make_helpers(items)
    out = os.path.join(ROOT, 'assets/img/prod')
    for name, body in [('jyt-arch.svg', build_wide(items, icon)),
                       ('jyt-arch-m.svg', build_mobile(items, icon))]:
        path = os.path.join(out, name)
        open(path, 'w', encoding='utf-8').write(body)
        print(path, len(body.encode('utf-8')), 'bytes')
    # 图内文字白名单校验
    allowed = set(it['name'] for it in items) | set(it['end'] for it in items) | {'茧易通'}
    for name in ['jyt-arch.svg', 'jyt-arch-m.svg']:
        s = open(os.path.join(out, name), encoding='utf-8').read()
        texts = [re.sub(r'<[^>]+>', '', m).strip()
                 for m in re.findall(r'<text[^>]*>.*?</text>', s, re.S)]
        extra = [t for t in texts if t not in allowed]
        assert not extra, (name, extra)
        sizes = [float(x) for x in re.findall(r'<text[^>]*font-size="([\d.]+)"', s)]
        print(name, '| 文字节点', len(texts), '| 最小字号', min(sizes), '| 全部原文词 OK')


if __name__ == '__main__':
    main()
