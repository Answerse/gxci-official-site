#!/usr/bin/env python3
"""校验：首页业务领域 hover 不再出现缩略图，且公共 JS 仍正常执行。"""
import json, subprocess, time, urllib.request
import websocket

JS = r"""
(async () => {
  const r = {};
  r.floatImgBefore = !!document.querySelector('.float-img');
  const row = document.querySelector('.biz-row');
  ['mouseenter', 'mousemove'].forEach(t => {
    row.dispatchEvent(new MouseEvent(t, {bubbles: true, clientX: 500, clientY: 400}));
  });
  await new Promise(r => setTimeout(r, 600));
  r.floatImgAfter = !!document.querySelector('.float-img');
  r.bizRows = document.querySelectorAll('.biz-row').length;
  r.dataImgLeft = document.querySelectorAll('[data-img]').length;
  r.haccItems = document.querySelectorAll('.hacc-item').length;
  r.homeNews = document.querySelectorAll('#hn-list li').length;
  r.rowPaddingLeft = getComputedStyle(row).paddingLeft;
  return JSON.stringify(r);
})()
"""

proc = subprocess.Popen([
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless", "--disable-gpu", "--hide-scrollbars",
    "--remote-debugging-port=9335", "--remote-allow-origins=*",
    "--user-data-dir=/tmp/cdp-check-profile",
    "--window-size=1600,1000", "about:blank"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    ws_url = None
    for _ in range(50):
        try:
            tabs = json.load(urllib.request.urlopen("http://127.0.0.1:9335/json"))
            page = [t for t in tabs if t.get("type") == "page"]
            if page:
                ws_url = page[0]["webSocketDebuggerUrl"]
                break
        except Exception:
            time.sleep(0.2)
    ws = websocket.create_connection(ws_url, timeout=30)
    mid = [0]
    errs = []

    def cmd(method, params=None):
        mid[0] += 1
        i = mid[0]
        ws.send(json.dumps({"id": i, "method": method, "params": params or {}}))
        while True:
            m = json.loads(ws.recv())
            if m.get("id") == i:
                return m.get("result", {})
            if m.get("method") == "Runtime.exceptionThrown":
                errs.append(str(m["params"]["exceptionDetails"].get("text")))

    cmd("Runtime.enable")
    cmd("Network.enable")
    cmd("Network.setCacheDisabled", {"cacheDisabled": True})
    cmd("Emulation.setDeviceMetricsOverride",
        {"width": 1600, "height": 1000, "deviceScaleFactor": 1, "mobile": False})
    cmd("Page.navigate", {"url": f"http://127.0.0.1:8410/index.html?t={int(time.time())}"})
    time.sleep(5)
    r = cmd("Runtime.evaluate", {"expression": JS, "returnByValue": True, "awaitPromise": True})
    print(r["result"]["value"])
    print("JS exceptions:", errs or "none")
finally:
    proc.terminate()
