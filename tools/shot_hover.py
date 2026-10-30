#!/usr/bin/env python3
"""hover 截图：鼠标移到指定元素中心后截图。
用法: python3 tools/shot_hover.py <url> <outfile> <hover_sel> <scroll_sel> [vw] [vh]
"""
import base64, json, subprocess, sys, time, urllib.request
import websocket

url, out, hover_sel = sys.argv[1], sys.argv[2], sys.argv[3]
scroll_sel = sys.argv[4] if len(sys.argv) > 4 else hover_sel
vw = int(sys.argv[5]) if len(sys.argv) > 5 else 1600
vh = int(sys.argv[6]) if len(sys.argv) > 6 else 1000
click_sel = sys.argv[7] if len(sys.argv) > 7 else ""

proc = subprocess.Popen([
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless", "--no-sandbox", "--in-process-gpu", "--hide-scrollbars",
    "--remote-debugging-port=9336", "--remote-allow-origins=*",
    "--user-data-dir=/tmp/cdp-hover-profile",
    f"--window-size={vw},{vh}", "about:blank"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    ws_url = None
    for _ in range(50):
        try:
            tabs = json.load(urllib.request.urlopen("http://127.0.0.1:9336/json"))
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
        time.sleep(1.5)
    cmd("Runtime.evaluate", {"expression": f"document.querySelector('{scroll_sel}').scrollIntoView({{block:'center'}})"})
    time.sleep(1.5)
    r = cmd("Runtime.evaluate", {
        "expression": f"(() => {{ const b = document.querySelector('{hover_sel}').getBoundingClientRect();"
                      " return JSON.stringify({x: b.x + b.width * 0.5, y: b.y + b.height * 0.5}); })()",
        "returnByValue": True})
    pt = json.loads(r["result"]["value"])
    cmd("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": pt["x"], "y": pt["y"], "buttons": 0})
    time.sleep(1.5)
    shot = cmd("Page.captureScreenshot", {"format": "png"})
    open(out, "wb").write(base64.b64decode(shot["data"]))
    print("saved", out)
finally:
    proc.terminate()
