#!/usr/bin/env python3
"""CDP 截图：打开 URL -> 滚动到锚点 -> 截图。
用法: python tools/shot.py <url> <outfile> [anchor] [vw] [vh]
"""
import base64, json, subprocess, sys, time, urllib.request
import websocket

url = sys.argv[1]
out = sys.argv[2]
anchor = sys.argv[3] if len(sys.argv) > 3 else ""
vw = int(sys.argv[4]) if len(sys.argv) > 4 else 1600
vh = int(sys.argv[5]) if len(sys.argv) > 5 else 1000
click_sel = sys.argv[6] if len(sys.argv) > 6 else ""

proc = subprocess.Popen([
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless", "--disable-gpu", "--hide-scrollbars",
    "--remote-debugging-port=9333", "--remote-allow-origins=*",
    "--user-data-dir=/tmp/cdp-shot-profile",
    f"--window-size={vw},{vh}", "about:blank"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    ws_url = None
    for _ in range(50):
        try:
            tabs = json.load(urllib.request.urlopen("http://127.0.0.1:9333/json"))
            page = [t for t in tabs if t.get("type") == "page"]
            if page:
                ws_url = page[0]["webSocketDebuggerUrl"]
                break
        except Exception:
            time.sleep(0.2)
    ws = websocket.create_connection(ws_url, timeout=30)
    mid = [0]

    def cmd(method, params=None):
        mid[0] += 1
        i = mid[0]
        ws.send(json.dumps({"id": i, "method": method, "params": params or {}}))
        while True:
            m = json.loads(ws.recv())
            if m.get("id") == i:
                return m.get("result", {})

    cmd("Network.enable")
    cmd("Network.setCacheDisabled", {"cacheDisabled": True})
    cmd("Emulation.setDeviceMetricsOverride",
        {"width": vw, "height": vh, "deviceScaleFactor": 2, "mobile": False})
    cmd("Page.navigate", {"url": f"{url}{'&' if '?' in url else '?'}t={int(time.time())}"})
    time.sleep(4)
    if click_sel:
        cmd("Runtime.evaluate", {"expression": f"document.querySelector('{click_sel}').click()"})
        time.sleep(2)
    if anchor:
        cmd("Runtime.evaluate",
            {"expression": f"document.querySelector('{anchor}').scrollIntoView({{block:'center'}})"})
        time.sleep(2)
    r = cmd("Page.captureScreenshot", {"format": "png"})
    open(out, "wb").write(base64.b64decode(r["data"]))
    print("saved", out)
finally:
    proc.terminate()
