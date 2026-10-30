#!/usr/bin/env python3
"""按宣传册（20261013-2 版）重写首页发展历程 15 个节点。"""
import re, io

PATH = '/Users/answerose/WorkBuddy/计算机官网/index.html'

NODES = [
    ('1986', '启程 · FOUNDED', [
        '广西壮族自治区计算机技术服务公司成立',
        '主营计算机及外设、办公自动化设备、机房配件，承接计算机工程与技术服务',
    ]),
    ('1990', '更名 · RENAMED', [
        '经广西壮族自治区计划委员会批复同意，更名为广西壮族自治区计算机公司',
    ]),
    ('2002', 'CA 筹建 · SETUP', [
        '由筹备组主要负责人杜文宏、黄山华发起并推动',
        '自治区信息产业局发文，批准成立广西数字证书认证中心',
    ]),
    ('2003', '广西CA · TRUST', [
        '注册成立广西数字证书认证中心（简称广西CA）',
        '以自有人员班底支撑广西CA建设，实行一套人马、两块牌子模式',
    ]),
    ('2008', '体系 · E-CERT', [
        '推动构建全区统一电子认证体系',
        '促进数字证书在电子政务、电子商务等领域应用',
    ]),
    ('2016', '覆盖 · COVERAGE', [
        '推动全区及 14 个地市公共资源交易中心、社保局落地电子认证服务',
    ]),
    ('2017', '划转 · TRANSFER', [
        '经自治区人民政府批准，由自治区工业和信息化委员会划转至广西宏桂资本运营集团有限公司',
    ]),
    ('2018', '公司制 · INC.', [
        '由全民所有制企业改制为有限责任公司',
        '更名为广西计算机有限责任公司',
    ]),
    ('2019', '增资 · CAPITAL', [
        '北部湾交易集团增资并控股广西计算机公司',
    ]),
    ('2020', '混改 · MIXED', [
        '恢复运营并完成混改',
        '启动宏桂集团信息化规划咨询项目',
    ]),
    ('2021', '高新 · HIGH-TECH', [
        '获认定为自治区高新技术企业',
    ]),
    ('2022', '平台 · PLATFORM', [
        '承建的宏桂集团信息化建设数字化运营平台一期项目 21 个子系统全部上线运行',
    ]),
    ('2023', '采购 · PROCUREMENT', [
        '参与规划建设的广西阳光采购服务平台标准化开评标场地投入使用',
    ]),
    ('2025', '产业 · INDUSTRY', [
        '自研“茧易通”在河池上线，助力广西国控集团获广西智慧农业（数字乡村）创新大赛三等奖',
        '自研“浦北陈皮通”在钦州浦北上线',
    ]),
    ('2026', '桂农 · AGRI', [
        '自研“桂农易通”产业互联网平台正式上线',
        '自研“桂资通”国有资产数字化监管与运营底座，支撑自治区国资委上线广西国有企业房产类资产登记管理系统',
        '陈皮多组学 + AI 智能溯源分级项目获自治区科技厅“2026 协同行动计划”首批立项',
    ]),
]

blocks = []
for i, (yr, cap, items) in enumerate(NODES):
    on = ' on' if i == 0 else ''
    aria = 'true' if i == 0 else 'false'
    lis = ''.join('<li>%s</li>' % x for x in items)
    blocks.append(
        '      <article class="hacc-item%s">\n'
        '        <button class="hacc-btn" type="button" aria-expanded="%s"><span class="yr">%s</span><span class="cap">%s</span></button>\n'
        '        <div class="hacc-panel"><div class="yr-lg">%s</div><div class="cap-lg">%s</div><ul class="hacc-list">%s</ul></div>\n'
        '      </article>' % (on, aria, yr, cap, yr, cap, lis)
    )
new_inner = '\n' + '\n'.join(blocks) + '\n'

html = io.open(PATH, encoding='utf-8').read()
m = re.search(r'(<div class="hacc" data-hacc>)(.*?)(\n    </div>\n    <div class="hacc-ctrl">)', html, re.S)
assert m, 'hacc block not found'
old_count = m.group(2).count('<article')
html = html[:m.start(2)] + new_inner + html[m.end(2):]
io.open(PATH, 'w', encoding='utf-8').write(html)
print('replaced articles: %d -> %d' % (old_count, len(NODES)))
