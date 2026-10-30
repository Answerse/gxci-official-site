#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广西计算机公司官网 新闻全量抓取
- 枚举 4 个分类的全部分页，收集条目（站内 artId / 微信公众号外链）
- 抓取站内文章详情：标题、日期、浏览量、正文 HTML、来源
- 输出 data/news.json（不经过模型上下文，纯脚本落盘）
用法:
  python3 tools/crawl_news.py --limit 10      # 样本，只抓 10 篇
  python3 tools/crawl_news.py --all           # 全量 358 条
"""
import argparse, json, os, re, sys, time, html
import urllib.request

BASE = "https://www.gxci.com.cn"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
CATS = [(3, "公司动态"), (5, "党建工作"), (4, "行业资讯"), (17, "学习宣传贯彻党的二十届四中全会精神")]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get(url, retry=2):
    for i in range(retry + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", errors="ignore")
        except Exception as e:
            if i == retry:
                print(f"  ! fail {url} {e}", file=sys.stderr)
                return ""
            time.sleep(1.2)


def strip_tags(s):
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"</p>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s).replace("\xa0", " ")
    s = re.sub(r"[ \t]+", " ", s)
    return "\n".join(l.strip() for l in s.split("\n") if l.strip())


def enumerate_category(cat_id, cat_name):
    items, seen = [], set()
    page, max_page = 1, 1
    while page <= max_page and page <= 60:
        url = f"{BASE}/pages/media_center?catId={cat_id}&page={page}" if page > 1 else f"{BASE}/pages/media_center?catId={cat_id}"
        s = get(url)
        if not s:
            break
        # 从分页控件读取最大页码
        nums = [int(x) for x in re.findall(rf"catId={cat_id}&(?:amp;)?page=(\d+)", s)]
        if nums:
            max_page = max(max_page, max(nums))
        blocks = re.findall(
            r'<div class="item-list-box">([\s\S]*?)<div class="item-list-date">([\d\-]+)</div>', s)
        new = 0
        for b, date in blocks:
            m = re.search(r'href="([^"]+)"', b)
            t = re.search(r'item-list-title">([\s\S]*?)</div>', b)
            if not m or not t:
                continue
            link = html.unescape(m.group(1))
            title = html.unescape(re.sub(r"<[^>]+>", "", t.group(1))).strip()
            mm = re.search(r"artId=(\d+)", link)
            art_id = int(mm.group(1)) if mm else None
            key = art_id if art_id else link
            if key in seen:
                continue
            seen.add(key)
            items.append({"cat_id": cat_id, "cat": cat_name, "title": title,
                          "date": date,
                          "url": link if link.startswith("http") else BASE + link,
                          "art_id": art_id, "external": art_id is None})
            new += 1
        if new == 0:
            break
        page += 1
        time.sleep(0.35)
    return items


def parse_detail(art_id):
    s = get(f"{BASE}/pages/article_details?artId={art_id}")
    if not s:
        return None
    d = {"art_id": art_id}
    m = re.search(r'<div class="info-title">\s*<h3>([\s\S]*?)</h3>', s)
    if not m:
        m = re.search(r"<title>([\s\S]*?)</title>", s)
    d["title"] = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else ""
    m = re.search(r"<span>(\d{4}-\d{2}-\d{2})</span>", s) or re.search(r"(\d{4}-\d{2}-\d{2})", s)
    d["date"] = m.group(1) if m else ""
    m = re.search(r"浏览[:：]\s*([\d]+)", s)
    d["views"] = int(m.group(1)) if m else 0
    m = re.search(r"当前位置[\s\S]{0,800}?<a[^>]*>([\s\S]*?)</a>\s*>\s*<a[^>]*>([\s\S]*?)</a>", s)
    d["crumb"] = [strip_tags(m.group(1)), strip_tags(m.group(2))] if m else []
    # 正文容器：info-details-center 起，到 footer 注释止
    start = s.find('<div class="info-details-center">')
    end = s.find("<!-- footer", start) if start > 0 else -1
    body = s[start + len('<div class="info-details-center">'):end] if start > 0 and end > start else ""
    if not body:
        body = s[s.find("<body"):]
    body = re.sub(r"<section>\s*</section>", "", body)
    body = re.sub(r"\s+", " ", body).strip()
    # 去掉末尾多余闭合标签
    body = re.sub(r"(?:\s*</div>)+\s*$", "", body).strip()
    d["content_html"] = body
    d["content_text"] = strip_tags(body)
    d["images"] = re.findall(r'<img[^>]+src="([^"]+)"', body)
    d["source"] = ""
    m = re.search(r"（来源[:：]\s*([^）]+)）", d["content_text"])
    if m:
        d["source"] = m.group(1).strip()
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="只抓 N 篇站内文章做样本")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()

    index = []
    for cid, cname in CATS:
        got = enumerate_category(cid, cname)
        print(f"{cname}: {len(got)} 条")
        index.extend(got)

    internal = [x for x in index if x["art_id"]]
    external = [x for x in index if x["external"]]
    print(f"合计 {len(index)} 条 | 站内 {len(internal)} | 微信外链 {len(external)}")

    targets = internal if args.all else internal[:args.limit] if args.limit else []
    details = []
    t0 = time.time()
    for n, it in enumerate(targets, 1):
        d = parse_detail(it["art_id"])
        if d:
            d.update({"cat_id": it["cat_id"], "cat": it["cat"], "list_title": it["title"], "list_date": it["date"]})
            details.append(d)
        if n % 10 == 0 or n == len(targets):
            print(f"  详情 {n}/{len(targets)}  {time.time()-t0:.1f}s")
        time.sleep(0.1)

    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    out = {"index": index, "details": details,
           "stat": {"total": len(index), "internal": len(internal), "external": len(external),
                    "detail_fetched": len(details)}}
    p = os.path.join(ROOT, "data", "news.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=0)
    size = os.path.getsize(p)
    chars = sum(len(d.get("content_text", "")) for d in details)
    print(f"写入 {p}  {size/1024:.1f} KB | 正文合计 {chars} 字 | 耗时 {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
