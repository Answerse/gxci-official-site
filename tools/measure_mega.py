#!/usr/bin/env python3
"""复用 9335 上的页面，逐个 hover 导航项，测量通栏子菜单几何 + 截图。"""
import base64, json, sys, time, urllib.request
import websocket

url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8410/index.html"
vw = int(sys.argv[2]) if len(sys.argv) > 2 else 1600
vh = 1000
shot_dir = "/Users/answerose/WorkBuddy/计算机官网/docs/shots/"
TAG = sys.argv[3] if len(sys.argv) > 3 else "mega"

tabs = json.load(urllib.request.urlopen("http://127.0.0.1:9335/json"))
page = [t for t in tabs if t.get("type") == "page"]
ws = websocket.create_connection(page[0]["webSocketDebuggerUrl"], timeout=30)
mid = [0]


def cmd(method, params=None):
    mid[0] += 1
    i = mid[0]
    ws.send(json.dumps({"id": i, "method": method, "params": params or {}}))
    while True:
        m = json.loads(ws.recv())
        if m.get("id") == i:
            return m.get("result", {})


def ev(expr):
    r = cmd("Runtime.evaluate", {"expression": expr, "returnByValue": True})
    if "exceptionDetails" in r:
        return "ERR " + json.dumps(r["exceptionDetails"])[:300]
    return r.get("result", {}).get("value")


cmd("Network.enable")
cmd("Network.setCacheDisabled", {"cacheDisabled": True})
cmd("Emulation.setDeviceMetricsOverride",
    {"width": vw, "height": vh, "deviceScaleFactor": 1, "mobile": False})
cmd("Page.navigate", {"url": f"{url}?t={int(time.time())}"})
time.sleep(3.5)

for n in ["business", "products", "news", "about"]:
    pt = json.loads(ev("""(() => {
      const a = document.querySelector('.menu a.m[data-nav="%s"]');
      if (!a) return JSON.stringify({x:0,y:0});
      window.scrollTo(0, 0);
      const b = a.getBoundingClientRect();
      return JSON.stringify({x: b.x + b.width/2, y: b.y + b.height/2});
    })()""" % n))
    cmd("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": pt["x"], "y": pt["y"], "buttons": 0})
    time.sleep(1.1)
    info = ev("""(() => {
      const li = document.querySelector('li:has(> a[data-nav="%s"])');
      const mg = li.querySelector('.mega');
      if (!mg) return 'NO MEGA';
      const cs = getComputedStyle(mg);
      const r = mg.getBoundingClientRect();
      const head = mg.querySelector('.mega-head').getBoundingClientRect();
      const links = mg.querySelector('.mega-links').getBoundingClientRect();
      const cols = getComputedStyle(mg.querySelector('.mega-links')).gridTemplateColumns;
      const items = [...mg.querySelectorAll('.ml')].map(a => {
        const b = a.getBoundingClientRect();
        return {t: a.querySelector('b').textContent, x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height), href: a.getAttribute('href')};
      });
      return JSON.stringify({
        op: cs.opacity, vis: cs.visibility,
        box: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)],
        head: [Math.round(head.x), Math.round(head.width)],
        links: [Math.round(links.x), Math.round(links.width)],
        cols, items
      });
    })()""" % n)
    print("==", n, info)
    shot = cmd("Page.captureScreenshot", {"format": "png"})
    path = shot_dir + TAG + "-" + n + ".png"
    open(path, "wb").write(base64.b64decode(shot["data"]))
    print("   saved", path)
ws.close()
