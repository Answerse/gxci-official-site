#!/usr/bin/env python3
"""实测：真实鼠标 hover / 激活后，读计算样式，验证交互反馈色符合块内同色系。
口径（用户 2026-10-23）：蓝色结构块（编号/眉题）hover 用蓝，金色/中性块 hover 用金。
注意：页面有 scroll-behavior:smooth，测试时先禁用，否则坐标取在滚动中途。
"""
import json, os, sys, time, urllib.request
import websocket

BASE = os.environ.get("SITE_BASE", "http://127.0.0.1:8410/")  # 可指向 file:///…（页面数据走全局变量，file:// 可渲染）
CDP_PORT = os.environ.get("CDP_PORT", "9335")  # 新版 Chrome 需 --remote-allow-origins=* 才接受 ws
GOLD_RGB = ("200,164,93", "184,134,11")  # --gold / --gold-d
BLUE_RGB = ("43,58,146",)                # --accent #2b3a92（浅底交互）
BLUE2_RGB = ("124,140,232",)             # --accent2 #7c8ce8（深底交互，纯 --accent 在深蓝上不可见）
GHOST_RGB = ("247,248,250",)             # ghost-num 淡灰水印 #f7f8fa
INK_RGB = ("20,20,20",)                  # --ink 正文墨色（中性标签 hover 加深）
MUT_RGB = ("138,138,138",)               # --mut 辅助灰（序号等结构性信息，不占品牌蓝）
WHITE_RGB = ("255,255,255",)             # 图片卡白字（hover 后仍是白，不转蓝）
TINT_RGB = ("46,74,109",)                # 首页业务卡 --t1 藏蓝（取自 card-enterprise 主色）

# (页面, 悬停目标, 读取目标, 伪元素, 属性, 期望色, 说明)
# 期望色：gold=交互金  blue=蓝结构块的蓝 hover（块内同色系）
CASES = [
    ("index.html", '.menu a.m[data-nav="business"]', '.menu a.m[data-nav="business"]', '::after', 'backgroundColor', 'blue', '导航主项 hover 下划线（白底态改标准蓝，2026-10-26；深底透明态仍金）'),
    ("index.html", '.ml', '.ml b', None, 'color', 'blue', '子菜单卡片 hover 子模块标题转蓝（V184 卡片式：图标与标题同步变蓝）'),
    ("index.html", '.bcard', '.bcard h3', None, 'color', 'white', '首页业务卡 hover 标题保持白色（V160 图片渐变卡：不再转蓝、不出描边，只浮出摘要）'),
    ("index.html", '.bcard--ent', '.bcard--ent', None, 'backgroundImage', 'tint', '首页业务卡渐变压在卡图主色上（V160：--t1 藏蓝已生效）'),
    ("index.html", '.smore', '.smore', None, 'color', 'blue', '板块“查看更多”hover（V93 金改蓝）'),
    ("index.html", '.nlist a', '.nlist a .t', None, 'color', 'blue', '首页新闻行 hover 标题（V93 金改蓝）'),
    ("index.html", '.ft-rec a', '.ft-rec a', None, 'color', 'blue', '页脚备案链接 hover（V93 金改蓝）'),
    ("index.html", '.ft-links a', '.ft-links a', None, 'color', 'blue', '页脚友情链接 hover（V128 右侧网站地图改友情链接，条目不显金）'),
    ("index.html", '#top', '#top', None, 'backgroundColor', 'blue', '回到顶部 hover 底（V93 金改蓝）'),
    ("index.html", '.hacc-item:nth-child(3)', '.hacc-item.on', '::before', 'backgroundImage', 'gold', '发展历程折叠项 hover 即展开（V133 时间轴），展开卡顶部金线保留'),
    ("index.html", '.hacc-arrow', '.hacc-arrow', None, 'backgroundColor', 'gold', '历程左右箭头 hover（V141 箭头分置两端，深底金底保留）'),
    ("products.html", '.pcard--nongyi', '.pcard--nongyi .pcard-plate', None, 'backgroundColor', 'pc:nongyi', '产品卡 hover 铭牌取配图主色（V194：桂农易通=农田橄榄绿）'),
    ("products.html", '.pcard--cocoon', '.pcard--cocoon .pcard-plate', None, 'backgroundColor', 'pc:cocoon', '产品卡 hover 铭牌取配图主色（V194：茧易通=茶山深绿）'),
    ("products.html", '.pcard--chenpi', '.pcard--chenpi .pcard-plate', None, 'backgroundColor', 'pc:chenpi', '产品卡 hover 铭牌取配图主色（V194：陈皮通=陈皮棕）'),
    ("products.html", '.pcard--forest', '.pcard--forest .pcard-plate', None, 'backgroundColor', 'pc:forest', '产品卡 hover 铭牌取配图主色（V194：林易通=丘陵绿）'),
    ("products.html", '.pcard--house', '.pcard--house .pcard-plate', None, 'backgroundColor', 'pc:house', '产品卡 hover 铭牌取配图主色（V194：房产类=楼宇钢蓝）'),
    ("products.html", '.pcard', '.pplate-h', None, 'color', 'white', '产品中心铭牌 hover 标题转白（取色底上不掺金，也不转蓝）'),
    ("news.html", '.ntabs button:not(.act)', '.ntabs button:not(.act)', None, 'borderColor', 'blue', '新闻分类标签 hover 描边（V83 金改蓝）'),
    ("news.html", '.row', '.row .t', None, 'color', 'blue', '新闻列表行 hover 标题（V83 金改蓝）'),
    ("news.html", '.row', '.row .d', None, 'color', 'blue', '新闻列表行 hover 日期（V83 金改蓝；V187 日期改单行后选择器随之调整）'),
    ("news.html", '#nqbtn', '#nqbtn', None, 'color', 'blue', '搜索按钮 hover（V93 金改蓝；V98 起同位置还叠了清空按钮 .nclear，故按 id 取放大镜）'),
    ("news.html", '.pager button', '.pager button', None, 'borderColor', 'blue', '翻页器 hover（整块蓝系）'),
    ("about.html", '.atabs button:not(.act)', '.atabs button:not(.act)', None, 'color', 'blue', '关于我们 tab hover 文字（V93 金改蓝；当前项 act 仍金，故排除）'),
    ("about.html", '.job-card', '.job-card', '::before', 'backgroundColor', 'blue', '招聘卡 hover 顶条（旧 .card 优势卡已随信息公开改版删除）'),
    ("business.html", '.biz2 .bcard', '.biz2 .bcard h2', None, 'color', 'white', '业务领域索引页卡 hover 标题保持白色（V169 起与首页 .bcard 同款渐变融合卡）'),
]


IMGHOVER_RGB = {  # V194 产品卡 hover 铭牌色（按各卡配图取主色压深）
    "nongyi": "88,110,22", "cocoon": "58,92,58", "chenpi": "133,66,0",
    "forest": "33,99,33", "house": "47,77,114",
}


def ok_color(v, which):
    if which.startswith("pc:"):
        return IMGHOVER_RGB[which[3:]] in str(v).replace(" ", "")
    rgb = {"gold": GOLD_RGB, "blue": BLUE_RGB, "blue2": BLUE2_RGB, "ghost": GHOST_RGB, "ink": INK_RGB, "mut": MUT_RGB, "white": WHITE_RGB, "tint": TINT_RGB}[which]
    return any(g in str(v).replace(" ", "") for g in rgb)


tabs = json.load(urllib.request.urlopen("http://127.0.0.1:%s/json" % CDP_PORT))
page = [t for t in tabs if t.get("type") == "page"][0]
ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=30)
mid = [0]


def cmd(method, params=None):
    mid[0] += 1
    ws.send(json.dumps({"id": mid[0], "method": method, "params": params or {}}))
    while True:
        m = json.loads(ws.recv())
        if m.get("id") == mid[0]:
            return m.get("result", {})


def ev(expr):
    r = cmd("Runtime.evaluate", {"expression": expr, "returnByValue": True})
    if "exceptionDetails" in r:
        return "ERR " + json.dumps(r["exceptionDetails"])[:160]
    return r.get("result", {}).get("value")


cmd("Network.enable")
cmd("Network.setCacheDisabled", {"cacheDisabled": True})
cmd("Emulation.setDeviceMetricsOverride",
    {"width": 1600, "height": 1000, "deviceScaleFactor": 1, "mobile": False})

cur, fails = None, []
for page_, hover_sel, read_sel, pseudo, prop, which, label in CASES:
    if page_ != cur:
        # 页面参数已带 ?s=xx（业务聚焦的两个标签面板）时用 & 接时间戳，否则会被拼成 ?s=xx?t=…
        _sep = "&" if "?" in page_ else "?"
        cmd("Page.navigate", {"url": BASE + page_ + _sep + "t=" + str(int(time.time()))})
        time.sleep(6)  # banner 图大，等页面完全就绪
        cur = page_
    if '历程折叠项' in label:
        # 该板块 6s 自动轮播，测量与读取之间会切项 → 先停表，锁定结构
        ev("for (let i = 1; i < 3000; i++) clearInterval(i);")
    if '导航主项' in label:
        # 导航是 fixed：跳过 scrollIntoView（会把页面拉回顶部、退回深底透明态），
        # 直接滚动触发 .nav.on 白底态再测；深底透明态的 hover 线按深底口径仍是金
        # 首页 .on（白底态）要滚过整个首屏才触发，滚 2000px 确保进入白底态
        ev("document.documentElement.style.scrollBehavior = 'auto'; window.scrollTo(0, 2000);")
    else:
        pt = json.loads(ev("""(() => {
      document.documentElement.style.scrollBehavior = 'auto';
      const el = document.querySelector('%s');
      if (!el) return JSON.stringify({x:-1,y:-1});
      el.scrollIntoView({block:'center'});
      return JSON.stringify({x: 0, y: 0});
    })()""" % hover_sel))
    time.sleep(1.4)  # 等 .rv 入场动画落定，否则元素还在位移
    pt = json.loads(ev("""(() => {
      const el = document.querySelector('%s');
      if (!el) return JSON.stringify({x:-1,y:-1});
      const b = el.getBoundingClientRect();
      return JSON.stringify({x: Math.round(b.x + b.width/2), y: Math.round(b.y + b.height/2)});
    })()""" % hover_sel) or '{"x":-1,"y":-1}')
    if pt["x"] < 0:
        fails.append((label, "元素不存在"))
        print("✗", label, "元素不存在")
        continue
    cmd("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": 3, "y": 3, "buttons": 0})
    time.sleep(0.8)  # mega 关闭动画 .32s，等它关完再传送，避免鼠标落进子菜单把 hover 卡死
    # 子菜单内的元素先悬停导航主项把面板拉下来，否则 visibility:hidden 的层收不到 hover
    if hover_sel.startswith('.ml') or 'ml-grp' in hover_sel or 'mega-all' in hover_sel:
        # 悬停哪个导航项由目标元素反查（V124：业务领域面板已无 .ml-grp，硬编码 business 会拉到隐藏层）
        pre = json.loads(ev("""(() => {
          const t = document.querySelector('%s');
          const li = t && t.closest('li.has-mega');
          const el = li ? li.querySelector('a.m') : document.querySelector('.menu a.m[data-nav="business"]');
          const b = el.getBoundingClientRect();
          return JSON.stringify({x: Math.round(b.x + b.width/2), y: Math.round(b.y + b.height/2)});
        })()""" % hover_sel) or '{"x":-1,"y":-1}')
        cmd("Input.dispatchMouseEvent", {"type": "mouseMoved",
                                         "x": pre["x"], "y": pre["y"], "buttons": 0})
        time.sleep(0.9)
    cmd("Input.dispatchMouseEvent", {"type": "mouseMoved",
                                     "x": pt["x"], "y": pt["y"], "buttons": 0})
    time.sleep(0.9)
    val = ev("getComputedStyle(document.querySelector('%s'), '%s').%s"
             % (read_sel, pseudo or "", prop))
    good = ok_color(val, which)
    print(("✓ " if good else "✗ ") + label + " → " + str(val))
    if not good:
        fails.append((label, val))

print("\n合计不符：%d" % len(fails))
for f in fails:
    print("  -", f)
ws.close()
