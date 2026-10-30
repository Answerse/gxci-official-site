#!/usr/bin/env python3
"""审计：抓取全站 CSS 中所有交互态规则（:hover / .act / :focus / .on），检查交互反馈色。

V94 口径（2026-10-26 用户两次明令「不要多此一举」，划定金色保留区）：
  浅底交互用 --accent #2b3a92；深底交互用 --accent2 #7c8ce8（纯 --accent 在 #141c52 上不可见）。
  金色**只允许**出现在 GOLD_ALLOWED 的四类位置，其余交互态一律蓝/中性：
    1. 页头当前栏目 .menu a.m.act（用户 2026-10-26 明令 active 必须金）
    2. 首页 banner 按钮 .hero .btn（用户 2026-10-26 明令 hover 金色保留）
    3. 发展历程整块 .hacc（深底区块，金色是它自己的装饰语言，用户明令保留）
    4. 关于我们 / 业务聚焦标签栏的**当前项** .atabs/.bztabs button.act（只改 hover，act 不动）
  其余中性色（白/墨/灰/线/透明）不计问题。
"""
import re

FILES = ["/Users/answerose/WorkBuddy/计算机官网/css/main.css",
         "/Users/answerose/WorkBuddy/计算机官网/css/pages.css",
         "/Users/answerose/WorkBuddy/计算机官网/css/sub.css"]

COLOR_PROPS = ("color", "background", "background-color", "background-image",
               "border-color", "border-top-color", "border-bottom-color",
               "border-left-color", "border-right-color", "box-shadow")

BLUE_HINTS = ("--accent", "--accent2", "#2b3a92", "#7c8ce8", "#1e2a70",
              "#6a7ade", "#4353c0", "#9aa8f0", "143,196,240")
NEUTRAL = ("#fff", "#ffffff", "white", "transparent", "inherit", "none",
           "rgba(255,255,255", "rgba(20,20,20", "rgba(15,25,45", "var(--ink)", "var(--ink2)",
           "var(--line)", "var(--panel)", "var(--panel-2)", "#e9ecf2", "currentcolor", "var(--dark)", "var(--dark2)",
           "var(--mut)")
GOLD = ("--gold", "--gold-d")

# 允许保留金色的交互态（白名单，每条都有用户明确指令，禁止擅自"统一成蓝"）
GOLD_ALLOWED = (
    ".menu a.m.act", "a.m.act",      # 页头当前栏目
    ".hero .btn",                    # 首页 banner 按钮
    ".hacc",                         # 发展历程整块（深底装饰语言）
    ".atabs button.act", ".bztabs button.act",  # 标签栏当前项（只改 hover）
)


def css_rules(text):
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.findall(r"([^{}]+)\{([^{}]*)\}", text)


def is_gold(v):
    return any(g in v for g in GOLD) or "#c8a45d" in v or "#b8860b" in v


def is_blue(v):
    return any(b in v for b in BLUE_HINTS)


def is_neutral(v):
    lv = v.lower()
    return any(n in lv for n in NEUTRAL)


# V194 用户指令：产品卡 hover 铭牌色按各卡配图取主色（非蓝非金，逐色白名单）
IMAGE_HOVER = ("#586e16", "#3a5c3a", "#854200", "#216321", "#2f4d72")


def is_image_hover(v):
    lv = v.lower()
    return any(c in lv for c in IMAGE_HOVER)


blue, gold_ok, gold_bad, other = 0, 0, [], []
for f in FILES:
    for sel, body in css_rules(open(f, encoding="utf-8").read()):
        sel = " ".join(sel.split())
        if not re.search(r":hover|:focus|\.act\b|\.on\b|:focus-within", sel):
            continue
        allowed = any(a in sel for a in GOLD_ALLOWED)
        for decl in body.split(";"):
            if ":" not in decl:
                continue
            prop, val = decl.split(":", 1)
            prop, val = prop.strip(), val.strip()
            if prop not in COLOR_PROPS:
                continue
            if is_gold(val):
                if allowed:
                    gold_ok += 1
                else:
                    gold_bad.append((f.split("/")[-1], sel, prop, val))
            elif is_blue(val) or is_neutral(val) or is_image_hover(val):
                blue += 1
            else:
                other.append((f.split("/")[-1], sel, prop, val))

print("交互态蓝色/中性声明：%d 条" % blue)
print("金色（白名单：页头当前栏目 / banner 按钮 / 发展历程 / 标签栏当前项）：%d 条" % gold_ok)
print("需要复核：%d 条" % (len(gold_bad) + len(other)))
for row in gold_bad:
    print("  - [%s] %s { %s: %s }  ← 金色残留，应改蓝（浅底 --accent / 深底 --accent2）" % row)
for row in other:
    print("  - [%s] %s { %s: %s }  ← 未知颜色" % row)
