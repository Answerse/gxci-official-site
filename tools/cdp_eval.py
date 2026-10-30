#!/usr/bin/env python3
"""CDP 取值：python tools/cdp_eval.py <width> <page> '<js expr>'
打印表达式 JSON 结果。"""
import json, sys, time, urllib.request
import websocket

PORT = 9336
BASE = "http://127.0.0.1:8410/"

def send(ws, mid, method, params=None):
    mid[0] += 1
    ws.send(json.dumps({"id": mid[0], "method": method, "params": params or {}}))
    while True:
        msg = json.loads(ws.recv())
        if msg.get("id") == mid[0]:
            if "error" in msg:
                raise RuntimeError(method + ": " + str(msg["error"]))
            return msg.get("result", {})

width = int(sys.argv[1]); page = sys.argv[2]; expr = sys.argv[3]
tabs = json.load(urllib.request.urlopen("http://127.0.0.1:%d/json" % PORT))
p = [t for t in tabs if t.get("type") == "page"][0]
ws = websocket.create_connection(p["webSocketDebuggerUrl"], timeout=60)
mid = [0]
send(ws, mid, "Page.enable")
send(ws, mid, "Network.enable")
send(ws, mid, "Network.setCacheDisabled", {"cacheDisabled": True})
send(ws, mid, "Emulation.setDeviceMetricsOverride",
     {"width": width, "height": 900, "deviceScaleFactor": 1, "mobile": False})
send(ws, mid, "Page.navigate", {"url": BASE + page})
time.sleep(2.4)
send(ws, mid, "Runtime.evaluate", {"expression": "document.documentElement.style.scrollBehavior='auto'"})
r = send(ws, mid, "Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
print(json.dumps(r.get("result", {}).get("value"), ensure_ascii=False))
ws.close()
