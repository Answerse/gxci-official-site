#!/usr/bin/env python3
"""量测发展历程手风琴每个展开面板的 padding 与内容溢出情况。
用法: python3 tools/measure_hist.py [vw] [vh]
"""
import json, subprocess, sys, time, urllib.request
import websocket

vw = int(sys.argv[1]) if len(sys.argv) > 1 else 1600
vh = int(sys.argv[2]) if len(sys.argv) > 2 else 1000

JS = r"""
(async () => {
  const items = [...document.querySelectorAll('.hacc-item')];
  items.forEach(x => x.style.transition = 'none');
  document.querySelectorAll('.hacc-panel').forEach(x => x.style.transition = 'none');
  const wait = () => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
  const out = [];
  const pad = getComputedStyle(document.querySelector('.hacc-panel')).padding;
  for (const it of items) {
    items.forEach(x => x.classList.remove('on'));
    it.classList.add('on');
    await wait(); await wait();
    const p = it.querySelector('.hacc-panel');
    const list = p.querySelector('.hacc-list');
    const cs = getComputedStyle(p);
    const pr = p.getBoundingClientRect();
    out.push({
      year: it.querySelector('.hacc-btn .yr').textContent.trim(),
      panelH: +pr.height.toFixed(1),
      contentH: +p.scrollHeight.toFixed(1),
      overflow: +(p.scrollHeight - pr.height).toFixed(1),
      listH: +list.getBoundingClientRect().height.toFixed(1),
      padTop: cs.paddingTop, padRight: cs.paddingRight,
      padBottom: cs.paddingBottom, padLeft: cs.paddingLeft,
      contentW: +(pr.width - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight)).toFixed(1)
    });
  }
  return JSON.stringify({pad: pad, items: out}, null, 1);
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
    cmd("Page.navigate", {"url": f"http://127.0.0.1:8410/index.html?t={int(time.time())}"})
    time.sleep(4)
    cmd("Runtime.evaluate", {"expression": "document.querySelector('.hacc').scrollIntoView({block:'center'})"})
    time.sleep(1.5)
    r = cmd("Runtime.evaluate", {"expression": JS, "returnByValue": True, "awaitPromise": True})
    print(r["result"]["value"])
finally:
    proc.terminate()
