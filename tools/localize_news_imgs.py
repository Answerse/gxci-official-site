#!/usr/bin/env python3
"""下载 data/articles 分片中的全部 gxci.com.cn 图片到 assets/img/news/，
并把分片中的热链/相对路径改写为本地路径。输出清单 data/img-localize-report.json"""
import json, glob, os, re, sys, time, hashlib
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.gxci.com.cn"
PAT = re.compile(r'(?:https?://(?:www\.)?gxci\.com\.cn)?(/file/load/[^"\\\s<>]+?\.(?:jpg|jpeg|png|webp|gif|jfif))')
LOCAL_PREFIX = "assets/img/news"

def collect():
    paths = set()
    for f in glob.glob(os.path.join(ROOT, "data/articles/a*.json")):
        for p in PAT.findall(open(f, encoding="utf-8").read()):
            paths.add(p)
    return sorted(paths)

def local_rel(p):
    # /file/load/topic/20250904/xxx.jpg -> assets/img/news/topic/20250904/xxx.jpg
    return LOCAL_PREFIX + p[len("/file/load/"):]

def download(p):
    dest = os.path.join(ROOT, local_rel(p).lstrip("/"))
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return p, "cached"
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    url = BASE + p
    for attempt in range(3):
        try:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0", "Referer": BASE})
            with urlopen(req, timeout=30) as r:
                data = r.read()
            # 校验是图片而不是错误页
            if len(data) < 500 and b"<" in data[:200]:
                raise ValueError("not an image")
            with open(dest, "wb") as f:
                f.write(data)
            return p, "ok"
        except Exception as e:
            if attempt == 2:
                return p, f"fail: {e}"
            time.sleep(1.5 * (attempt + 1))

def rewrite():
    changed_files = 0
    for f in glob.glob(os.path.join(ROOT, "data/articles/a*.json")):
        s = open(f, encoding="utf-8").read()
        def rep(m):
            return local_rel(m.group(1))
        s2 = PAT.sub(rep, s)
        if s2 != s:
            open(f, "w", encoding="utf-8").write(s2)
            changed_files += 1
    return changed_files

def main():
    paths = collect()
    print("待下载:", len(paths))
    results = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        for p, st in ex.map(download, paths):
            results[p] = st
            if st.startswith("fail"):
                print("FAIL", p, st, flush=True)
    ok = sum(1 for v in results.values() if v in ("ok", "cached"))
    fails = {p: v for p, v in results.items() if v.startswith("fail")}
    # 只重写全部成功的路径；有失败的路径保留原 URL
    if fails:
        print("有失败，先不重写这些路径")
    changed = rewrite() if not fails else 0
    report = {"total": len(paths), "ok": ok, "fail": len(fails),
              "rewritten_files": changed, "failures": fails}
    json.dump(report, open(os.path.join(ROOT, "data/img-localize-report.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in report.items() if k != "failures"}, ensure_ascii=False))

if __name__ == "__main__":
    main()
