#!/usr/bin/env python3
"""把 data/*.json 新闻数据生成为可被 <script> 直接加载的 .js（window 全局）。
背景：双击本地文件（file://）打开时 fetch JSON 被 CORS 拦截，新闻板块永远"加载中"。
改成 script 标签加载的 JS 全局后，file:// 与 http 均可用。
JSON 仍是数据源（爬虫产出）；更新新闻后必须重跑本脚本同步 .js。
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def dump(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))


def main():
    # 1) 新闻索引
    idx = json.load(open(os.path.join(ROOT, "data/news-index.json"), encoding="utf-8"))
    with open(os.path.join(ROOT, "data/news-index.js"), "w", encoding="utf-8") as f:
        f.write("window.NEWS_INDEX=")
        dump_to(f, idx)
        f.write(";")
    print("data/news-index.js", os.path.getsize(os.path.join(ROOT, "data/news-index.js")))

    # 2) 文章分片映射
    amap = json.load(open(os.path.join(ROOT, "data/articles/map.json"), encoding="utf-8"))
    with open(os.path.join(ROOT, "data/articles/map.js"), "w", encoding="utf-8") as f:
        f.write("window.ART_MAP=")
        dump_to(f, amap)
        f.write(";")
    print("data/articles/map.js", os.path.getsize(os.path.join(ROOT, "data/articles/map.js")))

    # 3) 各分片 a0-a6
    for n in range(7):
        src = os.path.join(ROOT, "data/articles/a%d.json" % n)
        if not os.path.exists(src):
            continue
        shard = json.load(open(src, encoding="utf-8"))
        dst = os.path.join(ROOT, "data/articles/a%d.js" % n)
        with open(dst, "w", encoding="utf-8") as f:
            f.write('window.ART_SHARDS=window.ART_SHARDS||{};window.ART_SHARDS["a%d"]="JSSTR";' % n)
        # 直接写 JSON 体，避免二次转义
        with open(dst, "w", encoding="utf-8") as f:
            f.write('window.ART_SHARDS=window.ART_SHARDS||{};window.ART_SHARDS["a%d"]=' % n)
            dump_to(f, shard)
            f.write(";")
        print("data/articles/a%d.js" % n, os.path.getsize(dst))


def dump_to(f, obj):
    s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    # 防止文章正文里的 </script> / <!-- 提前终止 <script> 标签（\/ 在 JS 字符串里就是 /）
    s = s.replace("</", "<\\/").replace("<!--", "<\\!--")
    f.write(s)


if __name__ == "__main__":
    main()
