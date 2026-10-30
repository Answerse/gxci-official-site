"""CDP 截图/量测小工具（V125）

用法：
  SHOT_W=1440 python3 tools/cdp_shot.py http://127.0.0.1:8410/business.html /tmp/out.png
注意：
- 视口必须在导航之前设定，否则页面按默认窗口（约 1080 宽）布局，截出来会被缩放。
- 截图前把 .rv 置终态、懒加载图强制 eager，否则整页截图会漏块、留白。
"""
import base64
import io
import json
import os
import subprocess
import sys
import time
import urllib.request

import websocket

PORT = os.environ.get('CDP_PORT', '9336')
W = int(os.environ.get('SHOT_W', '1440'))


def ensure_chrome():
    try:
        urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json/version', timeout=1)
        return None
    except Exception:
        pass
    p = subprocess.Popen([
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        f'--remote-debugging-port={PORT}', '--headless=new', '--no-first-run',
        '--no-sandbox', '--in-process-gpu', '--disable-gpu',
        '--user-data-dir=/tmp/cdp-prof-%s' % PORT, 'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(60):
        time.sleep(0.3)
        try:
            urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json/version', timeout=1)
            return p
        except Exception:
            continue
    raise RuntimeError('chrome not up')


class CDP:
    def __init__(self):
        tabs = json.load(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json'))
        page = [t for t in tabs if t['type'] == 'page'][0]
        self.ws = websocket.create_connection(page['webSocketDebuggerUrl'],
                                              suppress_origin=True, timeout=60)
        self.i = 0

    def send(self, method, **params):
        self.i += 1
        self.ws.send(json.dumps({'id': self.i, 'method': method, 'params': params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get('id') == self.i:
                if 'error' in msg:
                    raise RuntimeError(msg['error'])
                return msg.get('result', {})

    def eval(self, expr):
        r = self.send('Runtime.evaluate', expression=expr, returnByValue=True,
                      awaitPromise=True)
        return r.get('result', {}).get('value')

    def viewport(self, w, h, mobile=False):
        self.send('Emulation.setDeviceMetricsOverride', width=w, height=h,
                  deviceScaleFactor=1, mobile=mobile)

    def goto(self, url):
        self.send('Page.enable')
        self.send('Network.enable')
        self.send('Network.setCacheDisabled', cacheDisabled=True)
        self.viewport(W, 900, W < 700)
        self.send('Page.navigate', url=url)
        time.sleep(0.8)
        for _ in range(80):
            if self.eval('document.readyState') == 'complete':
                break
            time.sleep(0.25)
        time.sleep(0.4)
        # 入场动画未进入视口时 opacity:0，截图前直接置终态
        self.eval("(function(){var s=document.createElement('style');"
                  "s.textContent='.rv{opacity:1!important;transform:none!important}'"
                  "+'nav.nav,.pbar,#top{position:absolute!important}'"
                  "+'.bizhead,.drail{position:static!important}';"
                  "document.head.appendChild(s);"
                  "document.documentElement.style.scrollBehavior='auto';return 1})()")
        # 懒加载图强制 eager 并滚一遍
        self.eval("(function(){var n=0;[].forEach.call(document.images,function(i){"
                  "if(i.loading==='lazy'){i.loading='eager';n++;}"
                  "var s=i.getAttribute('src'); if(i.naturalWidth===0){i.src=s;}});"
                  "return n})()")
        self.eval("(async function(){var h=document.body.scrollHeight;"
                  "for(var y=0;y<h;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,50));}"
                  "window.scrollTo(0,0);await new Promise(r=>setTimeout(r,300));return 1})()")
        for _ in range(60):
            if self.eval("[].every.call(document.images,function(i){return i.complete&&i.naturalWidth>0})"):
                break
            time.sleep(0.2)
        time.sleep(0.5)

    def shot(self, path):
        """分段截图再拼接：一次性把视口撑到整页高度会被 Chrome 降采样（实测 0.75 倍），拼接可保证 1:1。"""
        from PIL import Image
        h = self.eval('Math.max(document.body.scrollHeight,document.documentElement.scrollHeight)')
        vh = 900
        self.viewport(W, vh, W < 700)
        time.sleep(0.5)
        ys = list(range(0, max(h - vh, 0) + 1, vh))
        if not ys or ys[-1] != max(h - vh, 0):
            ys.append(max(h - vh, 0))
        canvas = Image.new('RGB', (W, h), (255, 255, 255))
        for y in ys:
            self.eval(f'window.scrollTo(0,{y})')
            time.sleep(0.45)
            r = self.send('Page.captureScreenshot', format='png')
            img = Image.open(io.BytesIO(base64.b64decode(r['data']))).convert('RGB')
            canvas.paste(img, (0, y))
        self.eval('window.scrollTo(0,0)')
        canvas.save(path)
        return h


if __name__ == '__main__':
    ensure_chrome()
    c = CDP()
    c.goto(sys.argv[1])
    h = c.shot(sys.argv[2])
    print(sys.argv[2], 'height', h)
