#!/usr/bin/env python3
"""全站图片冗余审计：源图像素 vs 页面实际渲染宽度。

找出「存了 1200px 却只显示 300px」这类浪费，按可压缩空间排序。

用法：python3 tools/audit_img_ratio.py [viewport宽]
"""
import json, os, sys, time, urllib.request
import websocket

PORT = int(os.environ.get("CDP_PORT", "9336"))
BASE = os.environ.get("SITE_BASE", "http://127.0.0.1:8410/")
PAGES = ["index.html", "business.html", "products.html", "about.html", "news.html",
         "news-detail.html?id=494", "area-agri.html", "area-asset.html", "area-ai.html",
         "area-planning.html", "area-enterprise.html", "area-software.html",
         "area-infra.html", "area-domestic.html", "area-procure.html",
         "product-nongyi.html", "case-jiayitong.html", "case-chenpitong.html",
         "case-linyitong.html", "case-house.html"]

JS = """JSON.stringify([...document.images].map(e=>{
  const r=e.getBoundingClientRect();
  return {src:e.currentSrc||e.src, nw:e.naturalWidth, nh:e.naturalHeight,
          w:Math.round(r.width), h:Math.round(r.height)};
}).filter(x=>x.nw>0))"""


def send(ws, mid, method, params=None):
    mid[0] += 1
    ws.send(json.dumps({"id": mid[0], "method": method, "params": params or {}}))
    while True:
        msg = json.loads(ws.recv())
        if msg.get("id") == mid[0]:
            if "error" in msg:
                raise RuntimeError(method + ": " + str(msg["error"]))
            return msg.get("result", {})


def main():
    vw = int(sys.argv[1]) if len(sys.argv) > 1 else 1440
    tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json"))
    tgt = [t for t in tabs if t["type"] == "page"][0]
    ws = websocket.create_connection(tgt["webSocketDebuggerUrl"], suppress_origin=True, timeout=60)
    mid = [0]
    send(ws, mid, "Network.setCacheDisabled", {"cacheDisabled": False})
    send(ws, mid, "Emulation.setDeviceMetricsOverride",
         {"width": vw, "height": 900, "deviceScaleFactor": 1, "mobile": False})

    best = {}   # src -> (max render w, source w, h)
    for page in PAGES:
        send(ws, mid, "Page.navigate", {"url": BASE + page})
        time.sleep(2.2)
        for y in (0, 700, 1400, 2200, 3000, 4000):
            send(ws, mid, "Runtime.evaluate", {"expression": f"window.scrollTo(0,{y})"})
            time.sleep(0.25)
        send(ws, mid, "Runtime.evaluate", {"expression": "window.scrollTo(0,0)"})
        time.sleep(0.4)
        r = send(ws, mid, "Runtime.evaluate", {"expression": JS, "returnByValue": True})
        items = json.loads(r["result"].get("value") or "[]")
        for it in items:
            src = it["src"]
            path = src[len(BASE):] if src.startswith(BASE) else src
            cur = best.get(path)
            if cur is None or it["w"] > cur[0]:
                best[path] = (it["w"], it["nw"], it["nh"])

    print(f"\n=== 源图 vs 渲染宽度（{vw}px 视口）===")
    print(f"{'渲染宽':>6} {'源图宽':>7} {'源图高':>7}  {'冗余':>5}  路径")
    waste = []
    for path, (rw, nw, nh) in sorted(best.items(), key=lambda kv: -(kv[1][1] - kv[1][0])):
        if not path.startswith("assets/"):
            continue
        ratio = nw / max(rw, 1)
        waste.append((path, rw, nw, nh, ratio))
    for path, rw, nw, nh, ratio in waste[:30]:
        flag = "  <<<" if ratio >= 1.6 else ""
        print(f"{rw:6d} {nw:7d} {nh:7d}  {ratio:5.2f}x  {path}{flag}")
    over = [w for w in waste if w[4] >= 1.6]
    print(f"\n冗余 ≥1.6x 的图片：{len(over)} 张")
    return best


if __name__ == "__main__":
    main()
