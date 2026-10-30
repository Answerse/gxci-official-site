#!/usr/bin/env python3
"""量测关于我们·公司简介：标题规格一致性 + 右侧信息列表与正文首行文字的顶对齐偏差。
用法: python3 tools/measure_profile.py [vw] [vh]
"""
import json, subprocess, sys, time, urllib.request
import websocket

vw = int(sys.argv[1]) if len(sys.argv) > 1 else 1440
vh = int(sys.argv[2]) if len(sys.argv) > 2 else 1000

JS = r"""
(() => {
  const textRect = (el) => {
    const tn = [...el.childNodes].find(n => n.nodeType === 3 && n.textContent.trim());
    if (!tn) return null;
    const r = document.createRange();
    const i = tn.textContent.search(/\S/);
    r.setStart(tn, i); r.setEnd(tn, i + 1);
    return r.getBoundingClientRect();
  };
  const spec = (el) => {
    const cs = getComputedStyle(el);
    return {fs: cs.fontSize, fw: cs.fontWeight, ls: cs.letterSpacing, color: cs.color, lh: cs.lineHeight};
  };
  const h5 = document.querySelector('.prof-body .pb-h');
  const h4s = [...document.querySelectorAll('.vmv .vm h4')];
  const p = document.querySelector('.prof-body p');
  const kvb = document.querySelector('.prof-kv b');
  const pR = textRect(p), kR = textRect(kvb);
  const box = (el) => { const r = el.getBoundingClientRect(); return {top: +r.top.toFixed(1), left: +r.left.toFixed(1), w: +r.width.toFixed(1)}; };
  return JSON.stringify({
    h5: spec(h5), h4s: h4s.map(h => ({t: h.textContent.trim(), ...spec(h)})),
    h5box: box(h5), pbox: box(p),
    pTextTop: +pR.top.toFixed(1), kvTextTop: +kR.top.toFixed(1),
    kvOffset: +(kR.top - pR.top).toFixed(1),
    kvPadTop: getComputedStyle(document.querySelector('.prof-kv')).paddingTop
  }, null, 1);
})()
"""

proc = subprocess.Popen([
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless", "--disable-gpu", "--hide-scrollbars",
    "--remote-debugging-port=9334", "--remote-allow-origins=*",
    "--user-data-dir=/tmp/cdp-measure-profile",
    f"--window-size={vw},{vh}", "about:blank"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    ws_url = None
    for _ in range(50):
        try:
            tabs = json.load(urllib.request.urlopen("http://127.0.0.1:9334/json"))
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
        {"width": vw, "height": vh, "deviceScaleFactor": 1, "mobile": False})
    cmd("Page.navigate", {"url": f"http://127.0.0.1:8410/about.html?t={int(time.time())}"})
    time.sleep(4)
    r = cmd("Runtime.evaluate", {"expression": JS, "returnByValue": True, "awaitPromise": True})
    print(r["result"]["value"])
finally:
    proc.terminate()
