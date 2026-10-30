#!/usr/bin/env python3
"""按 (选择器, 旧字号) 精确重设字号，重建层级：14 / 15 / 16 / 17 / 18 ……"""
import re, sys

MICRO = '0.875rem'   # 14px 装饰 / 辅助
SMALL = '0.9375rem'  # 15px 次级 UI
BASE = '1.0625rem'   # 17px 正文

MAP = {
 'css/main.css': {
  ('body', '1rem'): BASE,
  ('.logo-t small', 'clamp(1rem,.95vw,1.0625rem)'): MICRO,
  ('.logo-t', '1.0625rem'): '1.125rem',
  ('.logo-t small', '1rem'): MICRO,
  ('.mega-en', '1rem'): MICRO,
  ('.mega-all', '1rem'): SMALL,
  ('.ml-t small', '1rem'): MICRO,
  ('.ml-grp', '1rem'): MICRO,
  ('a.ml-grp i', '1rem'): MICRO,
  ('.m-drawer a small', '1rem'): MICRO,
  ('.hero-tag', '1rem'): MICRO,
  ('.hero-sub', 'clamp(1rem,1.25vw,1.0625rem)'): 'clamp(1.0625rem,1.3vw,1.1875rem)',
  ('.hero-meta .wrap', '1rem'): SMALL,
  ('.btn', '1rem'): BASE,
  ('.shead .lb', '1rem'): MICRO,
  ('.shead p', '1rem'): BASE,
  ('.smore', '1rem'): SMALL,
  ('.bztabs button', '1rem'): BASE,
  ('.bztabs button em', '1rem'): MICRO,
  ('.bz-lead', '1rem'): '1.125rem',
  ('.bz-more', '1rem'): SMALL,
  ('.bcard .no', '1rem'): MICRO,
  ('.bcard .sub', '1rem'): MICRO,
  ('.bcard .go', '1rem'): SMALL,
  ('.bcard .go i', '1rem'): SMALL,
  ('.scene .tag', '1rem'): MICRO,
  ('.scene h3', '1.0312rem'): '1.125rem',
  ('.scene-go', '1rem'): SMALL,
  ('.hacc-btn .yr', '1rem'): SMALL,
  ('.hacc-btn .cap', '1rem'): MICRO,
  ('.hacc-panel .cap-lg', '1rem'): MICRO,
  ('.hacc-list li', '1rem'): MICRO,
  ('.hacc-count', '1rem'): MICRO,
  ('.hacc-nav button', '1rem'): BASE,
  ('.feat .fd span', '1rem'): MICRO,
  ('.nlist .t', '1rem'): BASE,
  ('.nlist .d', '1rem'): MICRO,
  ('.nlist .lead .fd span', '1rem'): MICRO,
  ('.nlist .lead .fd i', '1rem'): MICRO,
  ('.ntabs button', '1rem'): BASE,
  ('.ft-main h4', '1rem'): MICRO,
  ('.ft-logo b', '1rem'): BASE,
  ('.ft-logo small', '1rem'): MICRO,
  ('.ft-bar', '1rem'): MICRO,
  ('.crumb', '1rem'): MICRO,
  ('.phero .sub', '1rem'): BASE,
  ('.nsearch input', '1rem'): BASE,
  ('.row .t', '1.0312rem'): '1.125rem',
  ('.row .d i', '1rem'): MICRO,
  ('.row .cat', '1rem'): MICRO,
  ('.art-meta', '1rem'): MICRO,
  ('.art-body', '1.0312rem'): '1.125rem',
  ('.art-src', '1rem'): MICRO,
  ('.art-nav a small', '1rem'): MICRO,
  ('.biz-head .no', '1rem'): MICRO,
  ('.biz-head h2 small', '1rem'): MICRO,
  ('.biz-claim', 'clamp(1rem,1.8vw,1.375rem)'): 'clamp(1.0625rem,1.8vw,1.375rem)',
  ('.card .cn', '1rem'): MICRO,
  ('.numline b em', 'max(1rem,.5em)'): 'max(.875rem,.5em)',
  ('.numline span', '1rem'): MICRO,
  ('.atabs button', '1rem'): BASE,
  ('.prose', '1rem'): BASE,
  ('.map-card .mc-b b', '1rem'): BASE,
  ('.pcard .no', '1rem'): MICRO,
  ('.pcard .cat', '1rem'): MICRO,
  ('.pcard .go', '1rem'): SMALL,
 },
 'css/pages.css': {
  ('.phero-en', 'max(1rem,.4em)'): 'max(.875rem,.4em)',
  ('.note-muted', '1rem'): SMALL,
  ('.prof-hero .ph-tag', '1rem'): MICRO,
  ('.prof-hero .ph-sub', '1rem'): BASE,
  ('.prof-body p', '1rem'): BASE,
  ('.prof-kv small', '1rem'): MICRO,
  ('.vmv .vm small', '1rem'): MICRO,
  ('.hist-head .hh-tag', '1rem'): MICRO,
  ('.hist-e p', '1rem'): BASE,
  ('.hist-fig figcaption', '1rem'): MICRO,
  ('.job-head .hh-tag', '1rem'): MICRO,
  ('.jc-no', '1rem'): MICRO,
  ('.jc-tag', '1rem'): MICRO,
  ('.jc-meta', '1rem'): MICRO,
  ('.jc-arrow', '1rem'): BASE,
  ('.ct-lead-body small', '1rem'): MICRO,
  ('.ct-card-body h4', '1rem'): BASE,
  ('.ct-card-body .ct-sub', '1rem'): MICRO,
  ('.ext-mark', '1rem'): MICRO,
  ('.list-count', '1rem'): MICRO,
 },
 'css/sub.css': {
  ('.dhero-crumb', '1rem'): MICRO,
  ('.dhero-eyebrow', '1rem'): MICRO,
  ('.dhero-claim', 'clamp(1rem,1.5vw,1.25rem)'): 'clamp(1.0625rem,1.5vw,1.25rem)',
  ('.dhero-sub', '1rem'): BASE,
  ('.dhero-bot .wrap', '1rem'): MICRO,
  ('.drail .ren', '1rem'): MICRO,
  ('.drail .rcn', '1rem'): MICRO,
  ('.dtext', '1rem'): BASE,
  ('.dhead-en', '1rem'): MICRO,
  ('.dhead-p', '1rem'): BASE,
  ('.dstate .st-note', '1rem'): MICRO,
  ('.dstate .st-en', '1rem'): MICRO,
  ('.dserv-i .sn', '1rem'): MICRO,
  ('.dval h4', '1.0312rem'): BASE,
  ('.dstat b em', 'max(1rem,.4em)'): 'max(.875rem,.4em)',
  ('.dstat > span', '1rem'): MICRO,
  ('.drel h4', '1rem'): MICRO,
  ('.drel .rk', '1rem'): MICRO,
  ('.dpn small', '1rem'): MICRO,
  ('.dpn b', 'clamp(1rem,1.7vw,1.375rem)'): 'clamp(1.0625rem,1.7vw,1.375rem)',
  ('.oarea-k', '1rem'): MICRO,
  ('.oarea .ocl', '1rem'): MICRO,
  ('.olink', '1rem'): SMALL,
  ('.osfeat-t .k', '1rem'): MICRO,
  ('.osc-k', '1rem'): MICRO,
  ('.ocat-no', '1rem'): MICRO,
  ('.dstats-lab', '1rem'): MICRO,
 },
}

def norm(s):
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'\s*,\s*', ',', s)
    return s

total = 0
for f, mapping in MAP.items():
    lines = open(f, encoding='utf-8').read().split('\n')
    selbuf = ''
    hits = {k: 0 for k in mapping}
    for i, line in enumerate(lines):
        if '{' in line:
            head = line.split('{', 1)[0]
            sel = (selbuf + ' ' + head) if head.strip() == '' else head
            sel = norm(sel.replace('@media', ''))
            selbuf = ''
        elif line.strip() and '}' not in line and ':' not in line:
            selbuf += ' ' + line
            continue
        if 'font-size:' not in line:
            continue
        m = re.search(r'font-size:\s*([^;}]+)', line)
        old = m.group(1).strip()
        key = None
        for (s, o) in mapping:
            if norm(s) == sel and o == old:
                key = (s, o)
                break
        if key is None:
            continue
        new = mapping[key]
        lines[i] = line[:m.start(1)] + new + line[m.end(1):]
        hits[key] += 1
        total += 1
    open(f, 'w', encoding='utf-8').write('\n'.join(lines))
    miss = [k for k, v in hits.items() if v == 0]
    print(f, 'hit', sum(hits.values()), 'miss', len(miss))
    for k in miss:
        print('   MISS', k)
print('total', total)
