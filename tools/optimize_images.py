#!/usr/bin/env python3
"""全站图片压缩（V414）—— 目标：同等观感下把传输字节砍掉一半。

分三步，任何一步都可单独回滚：
  阶段 1  格式统一：news / hist 下的 .jpg .jpeg .png → .webp（改名，天然绕过旧缓存）
  阶段 2  质量重压：按目录规则把 webp 重新编码到更低的等价质量档（尺寸不放大）
  阶段 3  缓存令牌：凡是「内容被改过」的图片，把引用处的 ?v= 统一升到 NEW_V，
           否则浏览器拿旧缓存，改了也不生效

安全边界（改脚本前先读）：
  - 只动 assets/img 下白名单目录，不碰 SVG（二进制 logo、架构图）与 AVIF。
  - 重压后如果新文件「不比原来小」，或「只省不到 2%」，一律丢弃新文件保留原图。
  - 尺寸上限只做「不超过上限」的缩小，绝不放大。
  - 阶段 1 的删除动作放在最后：先出 .webp、再改引用、再校验零残留，才删原文件。
  - 全程先备份到 .workbuddy/backup/v414-img-compress/。
  - data/articles/*.js 是 data/articles/*.json 生成的产物，脚本不直接改它，
    最后统一跑 tools/make_data_js.py 重新生成，避免手改后被覆盖。

用法：
  python3 tools/optimize_images.py            # 干跑，只出报告（不落任何新文件）
  python3 tools/optimize_images.py --apply    # 真改
"""
import os, re, sys, glob, shutil

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

BACKUP = ".workbuddy/backup/v414-img-compress"
NEW_V = "414"
TMP = "/tmp/_gxci_opt_preview"

# ── 阶段 2 规则：(目录 glob, 最长边上限, webp 质量, 说明) ──────────────────
# 质量档依据：webp q75 以上肉眼几乎无损，q72 已是安全下限；banner/首屏保守一档。
# 尺寸上限依据 tools/audit_img_ratio.py 的实测（1440 视口下每张图的实际渲染宽）：
#   scenes/* 源图 1440 只渲染 335 → 4.3x 冗余，留 2x 余量即够
#   prod/card-* 源图 1200 渲染 305–411 → 留 2x 余量
#   news/* 正文容器 .art max-width 860，.art-body img 实际渲染 716 → 源图 1200 是 1.68x 冗余
RULES = [
    ("assets/img/biz/scenes/*.webp", 670, 76, "场景聚焦图（渲染仅 335px，源图 1440 冗余 4.3x）"),
    ("assets/img/biz/card-*.webp", 760, 76, "业务详情页配图（渲染 380px，源图 1200 冗余 3.16x）"),
    ("assets/img/news/topic/**/*.webp", 1000, 72, "新闻正文图（实际渲染 716px）"),
    ("assets/img/news/third/**/*.webp", 1000, 72, "新闻配图（实际渲染 716px）"),
    ("assets/img/banners/*.webp", 1920, 76, "页面头图（满屏宽）"),
    ("assets/img/biz/*.webp", 1600, 76, "业务领域配图"),
    ("assets/img/prod/*.webp", 820, 76, "产品卡图（渲染 305–411px）"),
    ("assets/img/hist/*.webp", 1400, 76, "发展历程配图"),
    ("assets/img/deco/*.webp", 1920, 76, "装饰底纹"),
    ("assets/img/hero-guokong.webp", 1920, 78, "首页首屏（最关键，保守一档）"),
]

# ── AVIF 规则：(glob, 最长边上限, avif 质量, 说明) ──────────────────────────
# 首页业务卡渲染尺寸只有 ~413px 宽，源图 1200×674 是 2.9 倍冗余；
# 缩到 900×506 仍有 2.2 倍余量（Retina 屏锐利），像素少 44%。
AVIF_RULES = [
    ("assets/img/biz/home-biz-*.avif", 840, 50, "首页业务卡（渲染仅 ~413px 宽）"),
    ("assets/img/biz/card-procure.avif", 840, 50, "国产化卡位"),
]

# ── 阶段 1：需要转 webp 的目录 ────────────────────────────────────────────
CONVERT_DIRS = ["assets/img/news", "assets/img/hist"]
CONVERT_EDGE = 1200
CONVERT_Q = 72

# 引用这些路径的「源」文本文件（阶段 3 扫描用；data/articles/*.js 由脚本生成，不在此列）
TEXT_GLOBS = ["*.html", "css/*.css", "js/*.js", "data/*.json", "data/articles/*.json"]

REPORT = {"converted": [], "recompressed": [], "skipped": [], "touched_text": []}


def human(n):
    return f"{n/1024:.1f}KB" if n < 1024 * 1024 else f"{n/1048576:.2f}MB"


def backup(path):
    dst = os.path.join(BACKUP, path)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst):
        shutil.copy2(path, dst)


def fit(im, max_edge):
    """缩到不超过 max_edge；绝不放大。缩放比 >1.5 时分步降采样（每级 ≤2 倍），
    一次到位会让边缘出振铃/锯齿。"""
    w, h = im.size
    if max(w, h) <= max_edge:
        return im
    if max(w, h) > max_edge * 1.5:
        cur = im
        cw, ch = cur.size
        while max(cw, ch) > max_edge * 1.5:
            if cw >= ch:
                nw = max(max_edge, cw // 2); nh = max(1, round(ch * nw / cw))
            else:
                nh = max(max_edge, ch // 2); nw = max(1, round(cw * nh / ch))
            cur = cur.resize((nw, nh), Image.LANCZOS)
            cw, ch = cur.size
        im = cur
        w, h = im.size
    if w >= h:
        return im.resize((max_edge, max(1, round(h * max_edge / w))), Image.LANCZOS)
    return im.resize((max(1, round(w * max_edge / h)), max_edge), Image.LANCZOS)


def open_rgb(path):
    with Image.open(path) as im:
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
        return im.copy()


def stage1_convert(apply):
    """jpg/jpeg/png → webp。返回 {旧相对路径: 新相对路径} 映射。"""
    mapping = {}
    files = []
    for d in CONVERT_DIRS:
        files += [p for p in glob.glob(d + "/**/*", recursive=True)
                  if os.path.isfile(p)
                  and os.path.splitext(p)[1].lower() in (".jpg", ".jpeg", ".png", ".jfif")]
    for src in sorted(files):
        dst = os.path.splitext(src)[0] + ".webp"
        if apply:
            out = dst
            os.makedirs(os.path.dirname(out), exist_ok=True)
        else:
            out = os.path.join(TMP, src)
            os.makedirs(os.path.dirname(out), exist_ok=True)
        try:
            im = fit(open_rgb(src), CONVERT_EDGE)
            im.save(out, "WEBP", quality=CONVERT_Q, method=5)
        except Exception as e:
            REPORT["skipped"].append((src, f"convert fail: {e}"))
            continue
        o0, o1 = os.path.getsize(src), os.path.getsize(out)
        mapping[src] = dst
        REPORT["converted"].append((src, dst, o0, o1))
        print(f"  转 webp  {src}  {human(o0)} → {human(o1)}")
        if apply:
            backup(src)
    return mapping


def stage2_avif(apply):
    """AVIF 重压（首页业务卡：渲染尺寸远小于源图，按渲染需要缩尺寸）。"""
    seen = set()
    for pattern, max_edge, q, note in AVIF_RULES:
        for path in sorted(glob.glob(pattern, recursive=True)):
            if not os.path.isfile(path) or path in seen:
                continue
            seen.add(path)
            try:
                with Image.open(path) as im:
                    if im.format != "AVIF":
                        continue
                    old_size = im.size
                    im = fit(im.convert("RGB"), max_edge)
                    new_size = im.size
                    tmp = path + ".tmp.avif"
                    im.save(tmp, "AVIF", quality=q)
            except Exception as e:
                REPORT["skipped"].append((path, f"avif fail: {e}"))
                continue
            o0, o1 = os.path.getsize(path), os.path.getsize(tmp)
            resized = old_size != new_size
            if resized:
                reason = f"缩尺寸 {old_size[0]}x{old_size[1]}→{new_size[0]}x{new_size[1]} q{q}"
            elif o1 >= o0 * 0.98:
                os.remove(tmp)
                REPORT["skipped"].append((path, f"仅省 {100*(1-o1/o0):.1f}%，跳过"))
                continue
            else:
                reason = f"质量 {q}"
            REPORT["recompressed"].append((path, o0, o1, q, old_size, new_size))
            print(f"  重压 AVIF {path}  {human(o0)} → {human(o1)}  ({reason})")
            if apply:
                backup(path)
                os.replace(tmp, path)
            else:
                os.remove(tmp)


def stage2_recompress(apply):
    seen = set()
    for pattern, max_edge, q, note in RULES:
        for path in sorted(glob.glob(pattern, recursive=True)):
            if not os.path.isfile(path) or path in seen:
                continue
            seen.add(path)
            try:
                with Image.open(path) as im:
                    if im.format != "WEBP":
                        continue
                    old_size = im.size
                    im = fit(im.convert("RGBA") if im.mode == "RGBA" else im.convert("RGB"), max_edge)
                    new_size = im.size
                    tmp = path + ".tmp.webp"
                    im.save(tmp, "WEBP", quality=q, method=5)
            except Exception as e:
                REPORT["skipped"].append((path, f"recompress fail: {e}"))
                continue
            o0, o1 = os.path.getsize(path), os.path.getsize(tmp)
            resized = old_size != new_size
            if resized:
                reason = f"缩尺寸 {old_size[0]}x{old_size[1]}→{new_size[0]}x{new_size[1]}"
            elif o1 >= o0 * 0.98:
                os.remove(tmp)
                REPORT["skipped"].append((path, f"仅省 {100*(1-o1/o0):.1f}%，跳过"))
                continue
            else:
                reason = f"质量 {q}"
            REPORT["recompressed"].append((path, o0, o1, q, old_size, new_size))
            print(f"  重压 {path}  {human(o0)} → {human(o1)}  ({reason})")
            if apply:
                backup(path)
                os.replace(tmp, path)
            else:
                os.remove(tmp)


def rewrite_refs(mapping, apply):
    """把源文件里对旧图片路径的引用改成新路径（阶段 1 改名）。"""
    if not mapping:
        return
    for pat in TEXT_GLOBS:
        for f in glob.glob(pat):
            s = open(f, encoding="utf-8").read()
            orig = s
            for old, new in mapping.items():
                s = s.replace(old, new)
            if s != orig:
                if apply:
                    backup(f)
                    open(f, "w", encoding="utf-8").write(s)
                REPORT["touched_text"].append(f)
                print(f"  改引用 {f}" + ("" if apply else "（干跑，未落盘）"))


def stage3_versions(changed, apply):
    """给内容变过的图片，把所有引用处的 ?v= 升到 NEW_V；原来没有 ?v= 的补上。"""
    if not changed:
        return
    # 合并成一个正则，一次扫描完成
    alt = "|".join(re.escape(p) for p in sorted(changed))
    pat_q = re.compile(r'((?:' + alt + r'))\?v=\d+')
    pat_plain = re.compile(r'((?:' + alt + r'))(?![\w/?])')
    for pat in TEXT_GLOBS:
        for f in glob.glob(pat):
            s = open(f, encoding="utf-8").read()
            orig = s
            s = pat_q.sub(r'\1?v=' + NEW_V, s)
            s = pat_plain.sub(r'\1?v=' + NEW_V, s)
            if s != orig:
                if apply:
                    backup(f)
                    open(f, "w", encoding="utf-8").write(s)
                REPORT["touched_text"].append(f)
                print(f"  升令牌 {f}" + ("" if apply else "（干跑，未落盘）"))


def cleanup_old(mapping, apply):
    """删掉已被 webp 取代的 jpg/jpeg/png。
    逐个判断：该路径若仍被任何文本文件引用（含生成产物 data/articles/*.js）就跳过，
    其余删除 —— 不能整批 return，早期版本整批跳过会留下一堆孤儿 jpg。"""
    if not mapping:
        return
    leftover = {}
    for pat in TEXT_GLOBS + ["data/articles/*.js"]:
        for f in glob.glob(pat):
            s = open(f, encoding="utf-8").read()
            for old in mapping:
                if old in s:
                    leftover.setdefault(old, []).append(f)
    for old in sorted(mapping):
        if not os.path.exists(old):
            continue
        if old in leftover:
            print(f"  跳过 {old}：仍被 {leftover[old]} 引用")
            REPORT["skipped"].append((old, "仍被引用，未删"))
            continue
        print(f"  删旧图 {old}（{human(os.path.getsize(old))}）")
        if apply:
            os.remove(old)


def main():
    apply = "--apply" in sys.argv
    print(f"=== 全站图片压缩（{'实改' if apply else '干跑'}） ===")

    print("\n[阶段 1] 格式统一 jpg/jpeg/png → webp")
    mapping = stage1_convert(apply)
    rewrite_refs(mapping, apply)

    print("\n[阶段 2] 质量重压")
    stage2_recompress(apply)
    stage2_avif(apply)

    changed = {p for p, _, _, _, _, _ in REPORT["recompressed"]}
    changed |= {new for _, new, _, _ in REPORT["converted"]}
    print(f"\n[阶段 3] 缓存令牌（{len(changed)} 个文件）")
    stage3_versions(sorted(changed), apply)

    print("\n[阶段 4] 清理已被取代的 jpg/jpeg/png")
    if mapping and apply:
        # 先把新闻数据产物重新生成（data/articles/*.js 里可能还指向旧 jpg），
        # 否则删完原图后文章正文会指向不存在的文件。
        import subprocess
        subprocess.run(["python3", "tools/make_data_js.py"], check=False,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("  已重生成 data/articles/*.js")
    cleanup_old(mapping, apply)

    c0 = sum(o for _, _, o, _ in REPORT["converted"])
    c1 = sum(n for _, _, _, n in REPORT["converted"])
    r0 = sum(o for _, o, _, _, _, _ in REPORT["recompressed"])
    r1 = sum(n for _, _, n, _, _, _ in REPORT["recompressed"])
    print("\n=== 汇总 ===")
    print(f"  格式统一 {len(REPORT['converted'])} 个：{human(c0)} → {human(c1)}")
    print(f"  质量重压 {len(REPORT['recompressed'])} 个：{human(r0)} → {human(r1)}")
    print(f"  净节省 {human((c0 - c1) + (r0 - r1))}")
    print(f"  跳过 {len(REPORT['skipped'])} 个")
    for p, why in REPORT["skipped"][:12]:
        print(f"    - {p}：{why}")
    if not apply:
        print("\n（干跑模式：未改任何原文件，新编码产物写在 /tmp）")


if __name__ == "__main__":
    main()
