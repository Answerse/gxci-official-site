#!/usr/bin/env python3
"""压缩 assets/img/news 下的图片：最长边 1600px、WebP q82。
阶段1：生成 .webp（不动原文件）→ 改写 data/articles 引用 → 校验。
加 --cleanup 才删除原格式文件。"""
import os, sys, glob, json
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_ROOT = os.path.join(ROOT, "assets/img/news")
IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".jfif", ".gif"}
MAXEDGE = 1600

def convert(path):
    ext = os.path.splitext(path)[1].lower()
    if ext not in IMG_EXT:
        return path, "skip"
    out = os.path.splitext(path)[0] + ".webp"
    if os.path.exists(out) and os.path.getsize(out) > 0:
        return path, "cached"
    try:
        im = Image.open(path)
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGBA" if "A" in im.getbands() or ext == ".png" else "RGB")
        w, h = im.size
        if max(w, h) > MAXEDGE:
            if w >= h:
                nh = round(h * MAXEDGE / w); nw = MAXEDGE
            else:
                nw = round(w * MAXEDGE / h); nh = MAXEDGE
            im = im.resize((nw, nh), Image.LANCZOS)
        im.save(out, "WEBP", quality=82, method=4)
        return path, "ok"
    except Exception as e:
        return path, f"fail: {e}"

def main():
    cleanup = "--cleanup" in sys.argv
    files = []
    for root, _, fs in os.walk(IMG_ROOT):
        for fn in fs:
            files.append(os.path.join(root, fn))
    print("文件总数:", len(files))
    results = {}
    with ThreadPoolExecutor(max_workers=6) as ex:
        for p, st in ex.map(convert, files):
            results[p] = st
            if st.startswith("fail"):
                print("FAIL", p, st, flush=True)
    fails = {p: s for p, s in results.items() if s.startswith("fail")}
    print("转换完成: ok=%d cached=%d skip=%d fail=%d" % (
        sum(1 for s in results.values() if s == "ok"),
        sum(1 for s in results.values() if s == "cached"),
        sum(1 for s in results.values() if s == "skip"),
        len(fails)))
    if fails:
        print("存在失败，不进行引用改写"); return

    # 引用改写：图片引用 → .webp
    shard_files = sorted(glob.glob(os.path.join(ROOT, "data/articles/a*.json")))
    n = 0
    for f in shard_files:
        s = open(f, encoding="utf-8").read()
        s2 = s
        for p in results:
            if results[p] in ("ok", "cached"):
                base = os.path.splitext(p)[0]
                if base.startswith(IMG_ROOT):
                    rel = base[len(ROOT)+1:]
                    s2 = s2.replace(rel + ".jpg", rel + ".webp") \
                           .replace(rel + ".jpeg", rel + ".webp") \
                           .replace(rel + ".png", rel + ".webp") \
                           .replace(rel + ".jfif", rel + ".webp") \
                           .replace(rel + ".gif", rel + ".webp") \
                           .replace(rel + ".JPG", rel + ".webp") \
                           .replace(rel + ".webp.webp", rel + ".webp")
        if s2 != s:
            open(f, "w", encoding="utf-8").write(s2); n += 1
    print("改写分片:", n)

    # 校验：所有引用都存在
    import re
    missing = []
    for f in shard_files:
        for m in re.findall(r'assets/img/news/[^"\\\s<>]+', open(f, encoding="utf-8").read()):
            if not os.path.exists(os.path.join(ROOT, m)):
                missing.append(m)
    print("缺失引用:", len(missing))
    for m in missing[:10]: print("  MISSING", m)
    if missing:
        print("有缺失，不清理原文件"); return

    if cleanup:
        removed = 0
        for p, st in results.items():
            if st in ("ok", "cached") and os.path.splitext(p)[1].lower() in IMG_EXT \
               and os.path.splitext(p)[1].lower() != ".webp":
                os.remove(p); removed += 1
        print("已删除原格式文件:", removed)
    total = sum(os.path.getsize(os.path.join(r, fn)) for r, _, fs in os.walk(IMG_ROOT) for fn in fs)
    print("assets/img/news 总大小: %.1f MB" % (total / 1048576))

if __name__ == "__main__":
    main()
