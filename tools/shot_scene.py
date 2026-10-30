import base64, json, time, urllib.request, websocket
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
tabs=json.load(opener.open("http://127.0.0.1:9335/json"))
pg=[t for t in tabs if t.get("type")=="page"][0]
ws=websocket.create_connection(pg["webSocketDebuggerUrl"],timeout=30); mid=[0]
def cmd(m,p=None):
    mid[0]+=1; ws.send(json.dumps({"id":mid[0],"method":m,"params":p or {}}))
    while True:
        r=json.loads(ws.recv())
        if r.get("id")==mid[0]: return r.get("result",{})
def ev(e):
    r=cmd("Runtime.evaluate",{"expression":e,"returnByValue":True})
    if "exceptionDetails" in r: return "ERR "+json.dumps(r["exceptionDetails"])[:200]
    return r.get("result",{}).get("value")
def desktop():
    cmd("Network.enable"); cmd("Network.setCacheDisabled",{"cacheDisabled":True})
    cmd("Emulation.clearDeviceMetricsOverride")
    cmd("Emulation.setDeviceMetricsOverride",{"width":1600,"height":1000,"deviceScaleFactor":1,"mobile":False})
def shot(url, out, hover_sel=None, wait=4.5, scroll_to=".scenes", dy=0):
    desktop()
    cmd("Page.navigate",{"url":url+("?t="+str(int(time.time())))})
    time.sleep(wait)
    ev("document.documentElement.style.scrollBehavior='auto'; document.querySelector('%s').scrollIntoView({block:'center'});" % scroll_to)
    time.sleep(2)
    if hover_sel:
        pt=json.loads(ev("""(() => { const c=document.querySelector('%s'); const b=c.getBoundingClientRect();
          return JSON.stringify({x:Math.round(b.x+b.width/2), y:Math.round(b.y+b.height/2)+%d}); })()""" % (hover_sel, dy)))
        cmd("Input.dispatchMouseEvent",{"type":"mouseMoved","x":pt["x"],"y":pt["y"],"buttons":0})
        time.sleep(1.4)
    d=cmd("Page.captureScreenshot",{"format":"png"})
    open(out,"wb").write(base64.b64decode(d["data"]))
    print("saved", out)
if __name__ == "__main__":
    u = "http://127.0.0.1:8410/index.html"
    shot(u, "docs/shots/v52-collage-default.png")
    shot(u, "docs/shots/v52-collage-hover5.png", hover_sel=".scene:nth-child(5)")
    shot(u, "docs/shots/v52-collage-hover1.png", hover_sel=".scene.lead")
ws.close()
