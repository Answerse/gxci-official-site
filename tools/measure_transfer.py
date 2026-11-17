#!/usr/bin/env python3
"""页面传输实测：用 CDP Network 事件统计某页实际传输的字节（按类型/文件分组）。

用法：python3 tools/measure_transfer.py <page> [viewport宽]
例：  python3 tools/measure_transfer.py index.html 1440
"""
import json, os, sys, time, urllib.request
import websocket

PORT = int(os.environ.get("CDP_PORT", "9336"))
BASE = os.environ.get("SITE_BASE", "http://127.0.0.1:8410/")


def send(ws, mid, method, params=None):
    mid[0] += 1
    ws.send(json.dumps({"id": mid[0], "method": method, "params": params or {}}))
    while True:
        msg = json.loads(ws.recv())
        if msg.get("id") == mid[0]:
            if "error" in msg:
                raise RuntimeError(method + ": " + str(msg["error"]))
            return msg.get("result", {})


def drain(ws, mid, seconds):
    """收集事件直到超时或收满。"""
    end = time.time() + seconds
    events = []
    ws.settimeout(0.4)
    while time.time() < end:
        try:
            msg = json.loads(ws.recv())
        except Exception:
            continue
        if msg.get("method"):
            events.append(msg)
    return events


def main():
    page = sys.argv[1]
    vw = int(sys.argv[2]) if len(sys.argv) > 2 else 1440
    url = BASE + page

    tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json"))
    tgt = [t for t in tabs if t["type"] == "page"][0]
    ws = websocket.create_connection(tgt["webSocketDebuggerUrl"], suppress_origin=True, timeout=60)
    mid = [0]

    send(ws, mid, "Network.enable")
    send(ws, mid, "Network.setCacheDisabled", {"cacheDisabled": True})
    send(ws, mid, "Emulation.setDeviceMetricsOverride",
         {"width": vw, "height": 900, "deviceScaleFactor": 1, "mobile": False})
    send(ws, mid, "Page.navigate", {"url": url})
    events = drain(ws, mid, 3.0)
    # 触发懒加载
    for y in (0, 900, 1800, 2700, 3600, 4500, 6000):
        send(ws, mid, "Runtime.evaluate", {"expression": f"window.scrollTo(0,{y})"})
        events += drain(ws, mid, 0.6)
    send(ws, mid, "Runtime.evaluate", {"expression": "window.scrollTo(0,0)"})
    events += drain(ws, mid, 1.0)

    req_url = {}
    for e in events:
        if e.get("method") == "Network.requestWillBeSent":
            req_url[e["params"]["requestId"]] = e["params"]["request"]["url"]

    seen = {}
    for e in events:
        if e.get("method") != "Network.loadingFinished":
            continue
        rid = e["params"]["requestId"]
        url = req_url.get(rid)
        if not url or not url.startswith(BASE):
            continue
        rel = url[len(BASE):]
        seen[rel] = seen.get(rel, 0) + e["params"].get("encodedDataLength", 0)

    def kind(u):
        p = u.split("?")[0]
        if p.endswith(".css"):
            return "CSS"
        if p.endswith(".js"):
            return "JS"
        if p.endswith(".html"):
            return "HTML"
        if p.endswith((".avif", ".webp", ".jpg", ".jpeg", ".png", ".svg", ".gif")):
            return "IMG"
        return "其他"

    buckets = {}
    for u, n in seen.items():
        buckets.setdefault(kind(u), []).append((n, u))
    total = sum(seen.values())
    print(f"\n=== {page}  @{vw}px ===")
    print(f"总传输 {total/1024:.1f}KB，共 {len(seen)} 个资源")
    for k in ("HTML", "CSS", "JS", "IMG", "其他"):
        if k not in buckets:
            continue
        items = sorted(buckets[k], reverse=True)
        sub = sum(n for n, _ in items)
        print(f"  {k:5} {len(items):3d} 个  {sub/1024:8.1f}KB")
        if k in ("IMG", "其他"):
            for n, u in items[:10]:
                print(f"        {n/1024:7.1f}KB  {u}")
    return seen


if __name__ == "__main__":
    main()
