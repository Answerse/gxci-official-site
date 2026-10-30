#!/usr/bin/env python3
"""逐个页面检查图片加载：<img> 破图 + 网络层 4xx/失败。
用法: python3 tools/check_imgs.py
"""
import json, time, urllib.request, sys
import websocket

PORT = 9336
BASE = "http://127.0.0.1:8410/"
PAGES = ["index.html", "business.html", "area-enterprise.html", "area-agri.html",
         "area-asset.html", "area-procure.html", "products.html",
         "product-nongyi.html", "case-jiayitong.html", "case-chenpitong.html",
         "case-linyitong.html", "case-house.html", "news.html", "news-detail.html",
         "about.html", "scene.html"]


def send(ws, mid, method, params=None, collect=None):
    mid[0] += 1
    ws.send(json.dumps({"id": mid[0], "method": method, "params": params or {}}))
    while True:
        msg = json.loads(ws.recv())
        if collect is not None and "method" in msg:
            collect.append(msg)
        if msg.get("id") == mid[0]:
            if "error" in msg:
                raise RuntimeError(method + ": " + str(msg["error"]))
            return msg.get("result", {})


tabs = json.load(urllib.request.urlopen("http://127.0.0.1:%d/json" % PORT))
p = [t for t in tabs if t.get("type") == "page"][0]
ws = websocket.create_connection(p["webSocketDebuggerUrl"], timeout=60)
mid = [0]
send(ws, mid, "Page.enable")
send(ws, mid, "Network.enable")
send(ws, mid, "Network.setCacheDisabled", {"cacheDisabled": True})
send(ws, mid, "Emulation.setDeviceMetricsOverride",
     {"width": 1440, "height": 900, "deviceScaleFactor": 1, "mobile": False})

bad_total = 0
for page in PAGES:
    evs = []
    send(ws, mid, "Network.clearBrowserCache")
    send(ws, mid, "Page.navigate", {"url": BASE + page})
    # 收集 Network 事件（navigate 后事件会持续到达，先等加载）
    time.sleep(0.3)
    ws.settimeout(0.4)
    deadline = time.time() + 3.0
    while time.time() < deadline:
        try:
            msg = json.loads(ws.recv())
        except Exception:
            continue
        if "method" in msg:
            evs.append(msg)
    ws.settimeout(60)
    fails = []
    for e in evs:
        m = e["method"]
        if m == "Network.responseReceived":
            r = e["params"]["response"]
            if r.get("status", 200) >= 400 and r.get("type") in ("Image", "Stylesheet", "Script", "Document", "Font"):
                fails.append("%s %s" % (r["status"], r["url"]))
        elif m == "Network.loadingFailed":
            fails.append("FAILED %s" % e["params"].get("errorText"))
    r = send(ws, mid, "Runtime.evaluate", {
        "expression": "JSON.stringify({n:document.images.length,"
                      "bad:[...document.images].filter(i=>i.getBoundingClientRect().width>0)"
                      ".filter(i=>!i.complete||i.naturalWidth===0)"
                      ".map(i=>(i.getAttribute('src')||i.currentSrc)),"
                      "hidden:[...document.images].filter(i=>i.getBoundingClientRect().width===0).length})",
        "returnByValue": True})
    res = json.loads(r["result"]["value"])
    ok = not res["bad"] and not fails
    print(("OK   " if ok else "BAD  ") + page +
          "  imgs=%d 隐藏(未取图)=%d" % (res["n"], res["hidden"]) +
          ("" if ok else "  bad=%s fails=%s" % (res["bad"][:5], fails[:5])))
    if not ok:
        bad_total += 1

print("\n有问题的页面:", bad_total)
sys.exit(1 if bad_total else 0)
