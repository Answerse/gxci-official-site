#!/usr/bin/env python3
"""把全站交互反馈色统一为金色（浅底 --gold-d / 深底 --gold）。
蓝色只保留给品牌结构性元素（标题、编号、静态强调）。
"""
import re, sys

ROOT = "/Users/answerose/WorkBuddy/计算机官网/css/"

# (文件, 旧串, 新串)
EDITS = [
    # ---------- 导航 ----------
    ("main.css",
     '.menu a.m::after{content:"";position:absolute;left:0;bottom:2px;width:0;height:2px;background:var(--accent)',
     '.menu a.m::after{content:"";position:absolute;left:0;bottom:2px;width:0;height:2px;background:var(--gold-d)'),
    ("main.css", ".menu a.m.act{color:var(--accent)}", ".menu a.m.act{color:var(--gold-d)}"),
    # ---------- 通栏子菜单 ----------
    ("main.css", ".mega-all:hover{border-color:var(--accent)}", ".mega-all:hover{border-color:var(--gold-d)}"),
    ("main.css", ".ml:hover .ml-t b{color:var(--accent)}", ".ml:hover .ml-t b{color:var(--gold-d)}"),
    # ---------- 按钮 ----------
    ("main.css", ".btn.ac::before{background:#1e2a70}", ".btn.ac::before{background:var(--gold-d)}"),
    ("main.css", ".btn.ac:hover{color:#fff;border-color:#1e2a70}", ".btn.ac:hover{color:#fff;border-color:var(--gold-d)}"),
    # ---------- 板块“更多” ----------
    ("main.css", ".smore:hover{color:var(--accent);border-color:var(--accent)}",
     ".smore:hover{color:var(--gold-d);border-color:var(--gold-d)}"),
    # ---------- 业务列表行 ----------
    ("main.css", ".biz-row:hover h3{color:var(--accent)}", ".biz-row:hover h3{color:var(--gold-d)}"),
    ("main.css", ".biz-row:hover .arr{background:var(--accent);border-color:var(--accent);color:#fff;",
     ".biz-row:hover .arr{background:var(--gold-d);border-color:var(--gold-d);color:#fff;"),
    ("main.css", '.biz-row::after{content:"";position:absolute;left:0;bottom:-1px;height:1px;width:0;background:var(--accent);',
     '.biz-row::after{content:"";position:absolute;left:0;bottom:-1px;height:1px;width:0;background:var(--gold-d);'),
    # ---------- 发展历程（深底 → 亮金） ----------
    ("main.css", ".hacc-item.on::before{content:\"\";position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#6a7ade,#4353c0)}",
     ".hacc-item.on::before{content:\"\";position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--gold),var(--gold-d))}"),
    ("main.css", ".hacc-prog i{position:absolute;inset:0 auto 0 0;width:0;background:#6a7ade;",
     ".hacc-prog i{position:absolute;inset:0 auto 0 0;width:0;background:var(--gold);"),
    ("main.css", ".hacc-btn:hover{color:#fff}", ".hacc-btn:hover{color:var(--gold)}"),
    ("main.css", ".hacc-nav button:hover{background:#fff;color:#1a2470;border-color:#fff}",
     ".hacc-nav button:hover{background:var(--gold-d);color:#fff;border-color:var(--gold-d)}"),
    # ---------- 首页新闻列表 ----------
    ("main.css", ".nlist a:hover .t{color:var(--accent)}", ".nlist a:hover .t{color:var(--gold-d)}"),
    ("main.css", ".nlist .lead .fd i{display:block;margin-top:10px;font-style:normal;font-size:15px;color:var(--accent);",
     ".nlist .lead .fd i{display:block;margin-top:10px;font-style:normal;font-size:15px;color:var(--gold-d);"),
    # ---------- 合作伙伴 ----------
    ("main.css", ".mq-track .mq-item:hover{border-color:var(--accent);", ".mq-track .mq-item:hover{border-color:var(--gold-d);"),
    # ---------- 页脚 ----------
    ("main.css", ".ft-main a:hover{color:var(--accent2)}", ".ft-main a:hover{color:var(--gold-d)}"),
    ("main.css", ".ft-bar a:hover{color:var(--ink)}", ".ft-bar a:hover{color:var(--gold-d)}"),
    # ---------- 子页头面包屑（深底） ----------
    ("main.css", ".crumb a:hover{color:#fff}", ".crumb a:hover{color:var(--gold)}"),
    # ---------- 新闻列表页 ----------
    ("main.css", ".nsearch button:hover{color:var(--accent)}", ".nsearch button:hover{color:var(--gold-d)}"),
    ("main.css", ".row:hover .t{color:var(--accent)}", ".row:hover .t{color:var(--gold-d)}"),
    # ---------- 新闻详情上下篇 ----------
    ("main.css", ".art-nav a:hover{border-color:var(--accent)}", ".art-nav a:hover{border-color:var(--gold-d)}"),
    # ---------- 业务卡片 ----------
    ("main.css", '.card::before{content:"";position:absolute;top:0;left:0;width:100%;height:2px;background:var(--accent);',
     '.card::before{content:"";position:absolute;top:0;left:0;width:100%;height:2px;background:var(--gold-d);'),
    # ---------- 关于我们 tabs ----------
    ("main.css", '.atabs button::after{content:"";position:absolute;left:0;bottom:-1px;width:100%;height:3px;background:var(--accent);',
     '.atabs button::after{content:"";position:absolute;left:0;bottom:-1px;width:100%;height:3px;background:var(--gold-d);'),
    ("main.css", ".atabs button:hover{color:var(--ink)}", ".atabs button:hover{color:var(--gold-d)}"),
    ("main.css", ".atabs button:hover::after{transform:scaleX(.35);background:var(--accent2)}",
     ".atabs button:hover::after{transform:scaleX(.35);background:var(--gold-d)}"),
    ("main.css", ".atabs button.act{color:var(--accent);font-weight:600}",
     ".atabs button.act{color:var(--gold-d);font-weight:600}"),
    ("main.css", ".atabs button.act::after{transform:scaleX(1);background:var(--accent)}",
     ".atabs button.act::after{transform:scaleX(1);background:var(--gold-d)}"),
    # ---------- 产品卡片 ----------
    ("main.css", ".pcard:hover{border-color:var(--accent);box-shadow:0 24px 48px rgba(15,25,45,.07)}",
     ".pcard:hover{border-color:var(--gold-d);box-shadow:0 24px 48px rgba(15,25,45,.07)}"),
    ("main.css", ".pcard .go{margin-top:22px;display:inline-flex;align-items:center;gap:10px;font-size:13px;letter-spacing:.16em;color:var(--accent)}",
     ".pcard .go{margin-top:22px;display:inline-flex;align-items:center;gap:10px;font-size:13px;letter-spacing:.16em;color:var(--gold-d)}"),
    # ---------- 招聘卡片 ----------
    ("pages.css", '.job-card::before{content:"";position:absolute;left:-1px;right:-1px;top:-1px;height:2px;background:var(--accent);',
     '.job-card::before{content:"";position:absolute;left:-1px;right:-1px;top:-1px;height:2px;background:var(--gold-d);'),
    ("pages.css", ".job-card:hover h4{color:var(--accent)}", ".job-card:hover h4{color:var(--gold-d)}"),
    ("pages.css", ".jc-arrow{font-family:var(--font);font-size:15px;color:var(--accent);",
     ".jc-arrow{font-family:var(--font);font-size:15px;color:var(--gold-d);"),
    # ---------- 场景卡（深底）hover ----------
    ("main.css", ".scene:hover img{transform:scale(1.07);opacity:.6}",
     ".scene:hover img{transform:scale(1.07);opacity:.6}\n.scene:hover h3{color:var(--gold)}\n.scene:hover .go{color:var(--gold)}"),
]

changed, missing = [], []
for f, old, new in EDITS:
    p = ROOT + f
    s = open(p, encoding="utf-8").read()
    if old not in s:
        missing.append((f, old[:60]))
        continue
    if s.count(old) > 1:
        print("!! 多处命中，跳过：", f, old[:50])
        missing.append((f, "MULTI " + old[:50]))
        continue
    open(p, "w", encoding="utf-8").write(s.replace(old, new))
    changed.append((f, old[:50]))

print("已改 %d 处" % len(changed))
for f, o in missing:
    print("未命中：", f, "|", o)
