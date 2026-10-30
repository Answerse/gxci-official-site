# -*- coding: utf-8 -*-
"""生成业务领域 / 场景聚焦 / 产品中心 的 15 个子页（统一版式，内容来自 data 字典）"""
import os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TYPE_CN = {'area': '业务领域', 'scene': '场景聚焦', 'product': '产品中心'}
TYPE_EN = {'area': 'BUSINESS AREA', 'scene': 'SCENE FOCUS', 'product': 'PRODUCTS'}
OVERVIEW = {'area': 'business.html?s=area', 'scene': 'business.html?s=scene', 'product': 'products.html'}

P = []

def E(s): return s

# ============================================================
# 业务领域（内容来源：公司宣传册 20261013 服务板块 01-04）
# ============================================================
P.append(dict(
 key='area-enterprise', type='area', no='01', en='ENTERPRISE DIGITALIZATION',
 title='集团型企业数字化转型', claim='全生命周期技术服务',
 sub='面向广西国控集团及各出资企业，提供数字化业务平台、IT 基础设施、数据安全与专业技术驻场的全生命周期技术服务。',
 banner='assets/img/banners/area-enterprise.webp',
 lead='四十年的 IT 底子，最后落在四件事上：把平台建起来、把基础打牢、把数据管好、把人派到现场。',
 paras=[
  '公司以数智科技为引擎、数据驱动为路径，面向广西国控集团及各出资企业，提供数字化业务平台规划建设、IT 基础设施规划建设与运维、数据管理与安全保障、专业技术驻场服务等全方位技术服务体系。',
  '凭借四十年 IT 行业深耕经验，已助力集团完成多期重大信息化项目建设，覆盖咨询规划、系统开发、部署实施、运维保障的全生命周期服务能力，持续为集团数字化转型和高质量发展注入强劲动能。'],
 state=('ENTERPRISE DIGITALIZATION', '把复杂留给自己，把<em>稳定交给客户</em>。'),
 services=('SERVICE', '服务内容', '平台、基础、数据、人——四个方向，一套体系。',
  [('数字化业务平台规划建设', 'OA 协同办公、财务管理、人力资源、资产管理等核心业务系统的规划、开发与运维。'),
   ('IT 基础设施规划建设与运维', '机房、网络、云资源与终端的一体化建设，以及运维体系建设与运维技能培训。'),
   ('数据管理与安全保障', '数据资产化管理与安全风险化解，保障业务系统安全稳定运行。'),
   ('专业技术驻场服务', '技术人员驻场、桌面运维、信息咨询规划，持续为客户创造数字化价值。')]),
 stats=[(21, '', '子系统全部上线'), (4, '大', '服务方向'), (40, '年', 'IT 行业积淀')],
 values=('VALUE', '价值优势', '懂国资，也懂技术',
  [('国企视角', '理解国资监管逻辑与合规要求，方案天然贴合国企治理结构。'),
   ('全栈能力', '咨询规划、系统开发、部署实施、运维保障，一家单位把链条走完。'),
   ('长期陪伴', '本地化团队与驻场服务能力，系统上线只是开始。')]),
 related=['scene-software', 'area-procure', 'product-software']))

P.append(dict(
 key='area-agri', type='area', no='02', en='AGRI INDUSTRY PLATFORM',
 title='桂农易通产业服务平台', claim='让特色农产品从产地直达交易',
 sub='以农产品收购“反向开票”为切入点，构建多品类、多区域的特色农业产业互联网平台体系。',
 banner='assets/img/banners/area-agri.webp',
 lead='一车蚕茧从地里出来，到变成一张发票、一笔贷款，中间的路我们替它铺好了。',
 paras=[
  '公司立足广西特色农业资源，自主研发“桂农易通”系列平台，依托农产品收购“反向开票”政策，打通交易、支付、开票全链路，破解农产品收购获票难、融资难痛点。',
  '为蚕茧、陈皮、林木、甘蔗等特色农产品提供产地到交易的全程数字化服务，形成茧易通、陈皮通、林易通、蔗易通等垂直平台，以及生产、流通两大板块协同的平台体系。'],
 state=('AGRI INDUSTRY PLATFORM', '让每一笔收购，都<em>开得出票</em>。'),
 services=('SERVICE', '服务内容', '一个平台底座，生产与流通两端同时接住。',
  [('交易结算开票', '农户身份认定、线上交易结算、反向开票、收购资金风控与采购合规数据存证。'),
   ('生产板块', '智能传感器、控制器、农机与无人机、水肥灌溉设施，以及农药肥料种苗、人力物流、农技指导服务。'),
   ('流通板块', '桂农易采买手团队与代采实时追溯，桂农金服适配农产品小额多笔交易的供应链金融。'),
   ('统一功能模块', '统一用户认证、统一资金账户、统一订单管理、统一结算体系、统一信用分数。')]),
 stats=[('10.6', '亿', '茧易通累计交易额'), (14, '万+', '服务农户'),
        ('100', '%', '陈皮通线上开票率'), (4, '个', '垂直产业平台')],
 values=('VALUE', '价值优势', '开得出票，也融得到资',
  [('政策合规', '反向开票与四流合一闭环管控，让收购业务合规可查。'),
   ('全链打通', '交易、支付、开票、物流、金融在同一条链路上跑通。'),
   ('可复制', '浦北样板已经跑通，可向多品类、多区域快速复制。')]),
 related=['scene-rural', 'product-rural', 'scene-software']))

P.append(dict(
 key='area-asset', type='area', no='03', en='ASSET PLATFORM',
 title='桂资通资产管理平台', claim='让国有资产底数更清晰',
 sub='覆盖资产登记、经营管理、交易协同、动态监管、盘活利用全链条的国有资产数字化管理与价值运营平台。',
 banner='assets/img/banners/area-asset.webp',
 lead='一栋楼从“账上有”到“用得起来”，中间差的是一套系统。',
 paras=[
  '公司自主研发“桂资通”国有资产数字化管理与价值运营平台，围绕国有资产管理、经营运营及盘活利用需求，构建涵盖资产登记、经营管理、交易协同、动态监管、盘活利用的全链条数字化服务体系。',
  '面向国资监管部门、各级国有企业及资产运营机构，提供企业侧资产管理、监管侧数据汇聚分析、房产类资产登记管理及产权交易业务对接等综合解决方案，推动国有资产底数更清晰、管理更规范、盘活更高效、监管更有力。'],
 state=('ASSET PLATFORM', '让每一处资产，都<em>找得到、管得住、盘得活</em>。'),
 services=('SERVICE', '服务内容', '五层架构，从物联感知一直做到数据底座。',
  [('业务应用层', '监管应用、资产经营、交易协同三类应用，覆盖底账、驾驶舱、招商租赁、挂牌竞价。'),
   ('智能与物联层', '表计接入、设备监测、门禁道闸、视频联动，以及智能分析、风险预警、闲置识别。'),
   ('数据底座层', '资产主档、权属信息、空间资源、客户租户、合同账单、设备台账、能耗与交易结果。'),
   ('技术支撑层', '标准接口、主数据映射、数据报送回传、IoT 平台、AI 引擎、GIS 服务与分级授权。')]),
 stats=[(2026, '年', '房产登记系统上线'), (5, '层', '平台架构'), (1, '个', '自治区级资产数据库')],
 values=('VALUE', '价值优势', '底数清、盘得活、管得住',
  [('底数清晰', '统一登记标准与数据口径，各级企业资产数据统一归集、动态更新。'),
   ('交易联动', '打通资产登记与盘活、交易业务链条，为进场交易夯实数据底座。'),
   ('监管有力', '风险预警与盘活督办在线，监管从“看报表”变成“看系统”。')]),
 related=['area-enterprise', 'scene-data', 'product-data']))

P.append(dict(
 key='area-procure', type='area', no='04', en='LOCALIZATION PROCUREMENT',
 title='国产软硬件产品集采服务', claim='正版化 · 国产化 · 降本增效',
 sub='作为广西正版软件集中采购平台建设主体，提供产品选型、集中采购、适配改造、系统集成、运维保障的国产化全链条服务。',
 banner='assets/img/banners/area-procure.webp',
 lead='自治区版权局、国资委联合发文指定的建设主体——这件事我们做了六年。',
 paras=[
  '公司深度贯彻国家信息技术应用创新发展战略，响应自治区推进软件正版化和国产化替代工作部署，是自治区版权局、国资委联合发文指定的“广西正版软件集中采购平台”建设主体。',
  '公司发挥国产化领域先发优势与渠道资源积累，构建产品选型、集中采购、适配改造、系统集成、运维保障的全链条服务体系；同时建设广西阳光采购平台直采商城，以规模效应降低采购价格、优化采购流程。'],
 state=('LOCALIZATION PROCUREMENT', '同样的预算，<em>买得更值</em>。'),
 services=('SERVICE', '服务内容', '选型、采购、适配、运维，一条国产化链路。',
  [('产品选型', '国产办公软件、操作系统与信创硬件的选型评估与适配验证。'),
   ('集中采购', '137 家区直国有企业集中签约，以规模效应降低采购价格。'),
   ('适配改造与系统集成', '兼容性适配、迁移实施与系统集成，替换过程不影响业务运行。'),
   ('运维保障', '交付后的运维与培训，保障替换之后长期稳定运行。')]),
 stats=[(137, '家', '累计签约区直国企'), (925, '台/套', '信创硬件设备'),
        (29000, '+', '套办公软件及操作系统'), (500, '万+', '元节约采购及运维成本')],
 values=('VALUE', '价值优势', '政策背书，价格实在',
  [('政策支撑', '版权局、国资委联合发文指定，政策、资源、技术、督查四位一体。'),
   ('价格优势', '规模集采与直采商城并行，把采购成本实实在在降下来。'),
   ('长效机制', '采购、适配、运维一体化，形成可持续的正版化工作机制。')]),
 related=['area-enterprise', 'scene-software', 'product-ca']))

# ============================================================
# 场景聚焦
# ============================================================
P.append(dict(
 key='scene-etrade', type='scene', no='01', en='E-TRADING',
 title='让交易更容易 · E交易', claim='全国性、综合性电子商务云平台',
 sub='集非标资产交易与招标采购于一体，让一宗资产从挂牌到成交，全程在线。',
 banner='assets/img/banners/scene-etrade.webp',
 lead='一宗资产从挂牌到成交，全程在线；一次采购从立项到落槌，全程留痕。',
 paras=[
  'e 交易由北部湾产权交易所集团牵头国内多家省级产权交易机构投资建设运营，广西计算机公司负责广西及东盟区域的推广运营。',
  '平台以资产处理、招标采购、快捷采购三大系统为核心，集成 CA 加密、全国供应商库与行业专家库，为交易机构与企业提供全流程在线交易技术服务。'],
 state=('E-TRADING', '让交易更容易，也让<em>监管更简单</em>。'),
 services=('SYSTEM', '系统构成', '三类交易，三套系统，同一个平台。',
  [('资产处理系统', '实物资产、权益类资产与增资扩股等非标资产处置，专业包装、全国精准推广。'),
   ('招标采购系统', '六种招标采购方式线上全流程，CA 加密保护，海量供应商库与专家库支撑。'),
   ('快捷采购系统', '与企业 ERP 对接，多种竞价方式，解决轻值品、标准品的竞价采购。'),
   ('交易数据服务', '交易全过程数据归集与分析，为监管与决策提供依据。')]),
 stats=[(83000, '+', '入驻会员'), (32000, '+', '产权交易'), (2200, '亿+', '成交金额'),
        (6500, '+', '招标采购'), (110, '亿+', '采购金额')],
 values=('VALUE', '价值优势', '让资产发现真正的价格',
  [('保值增值', '公开竞价与专业包装，让资产在更大的市场里发现价格。'),
   ('阳光规范', '标准公告模板与全程留痕，杜绝交易纠纷，对接监管机构。'),
   ('降本增效', '线上全流程替代线下跑办，缩短周期、降低交易成本。')]),
 related=['area-enterprise', 'product-etrade', 'scene-data']))

P.append(dict(
 key='scene-rural', type='scene', no='02', en='RURAL REVITALIZATION',
 title='服务振兴乡村', claim='“1+N”五级联动',
 sub='按照“1+N”模式构建覆盖全区的农村产权流转交易信息系统，区、市、县、乡、村五级联动。',
 banner='assets/img/banners/scene-rural.webp',
 lead='一片山林、一宗水塘、一间旧校舍，都能在同一个平台上找到它的价格。',
 paras=[
  '公司作为唯一指定系统集成商，应用各类先进技术结合广西农村产权流转交易市场“1+N”建设模式，打造集登记、交易、金融配套、市场监督于一体的五级联动综合信息服务平台。',
  '平台让农村产权流转从“熟人介绍”走向“公开竞价”，让沉睡的资源变成可以抵押、可以入股的资产。'],
 state=('RURAL REVITALIZATION', '让乡村的资源，<em>被看见</em>。'),
 services=('SUBSYSTEM', '系统构成', '六个子系统，覆盖农村产权流转的每一个环节。',
  [('农村产权交易系统', '挂牌申请、审核受理、组织交易、合同签订、价款结算、交易鉴证全生命周期管理。'),
   ('农村征信系统', '采集各类涉农信息，缓解农民贷款难，防范商业银行信贷风险。'),
   ('三资管理系统', '农村集体资金、资产、资源管理民主化、科学化、规范化。'),
   ('涉农招标采购系统', '涉农物资采购全流程电子化，公开透明、规范有序。'),
   ('农业大数据', '汇集各级交易数据，图形化呈现项目分布、交易量与价格趋势。'),
   ('农特电商', 'B2B 农特产交易平台，来源可追溯，连接小农户与大市场。')]),
 stats=[('1+N', '', '建设模式'), (5, '级', '区市县乡村联动'), (6, '个', '业务子系统')],
 values=('VALUE', '价值优势', '一套规则，五级贯通',
  [('五级联动', '区、市、县、乡、村同一套规则、同一个平台。'),
   ('数据归集', '交易、征信、三资数据在县域内打通，形成涉农数据底座。'),
   ('金融下乡', '以交易与征信数据为支撑，让金融资源更顺畅地进入乡村。')]),
 related=['product-rural', 'area-enterprise', 'scene-data']))

P.append(dict(
 key='scene-software', type='scene', no='03', en='SOFTWARE SERVICE',
 title='软件与信息化服务', claim='阳光、透明的软件交易市场',
 sub='建设阳光、透明的正版软件与 IT 服务交易市场，服务广西国资国企改革和数字化转型升级。',
 banner='assets/img/banners/scene-software.webp',
 lead='正版化不是一次采购，而是一套可以长期运转的机制。',
 paras=[
  '2018 年 9 月，自治区人民政府使用正版软件工作领导小组印发《广西推进企事业单位使用正版软件工作规划》，明确全区企事业单位使用正版软件的工作目标、实施步骤与监督检查。',
  '根据桂权〔2020〕10 号、桂新出〔2020〕56 号文件精神，公司与北部湾产权交易所集团共同作为建设主体，建设广西正版化软件集中采购平台，提供集中采购与软件正版化配套服务。'],
 state=('SOFTWARE SERVICE', '阳光采购，<em>长效常态</em>。'),
 services=('SERVICE', '服务内容', '从政策落地，到资产全生命周期管理。',
  [('正版化推进', '落实全区企事业单位使用正版软件工作规划，提供政策解读与实施路径。'),
   ('集中采购平台', '集中采购信息统一发布常态化，为批量采购提供阳光、规范、长效的平台服务。'),
   ('信息化评估', '第三方独立评估体系，含企业价值、知识产权与信息化项目评估。'),
   ('软件资产管理', '覆盖采购、分发、维护、使用及报废全生命周期的管理与保护。'),
   ('资质管家', 'IT 企业资质建设咨询、申办全流程咨询及涉软政策咨询。')]),
 stats=[(2018, '', '工作规划印发'), (2020, '', '平台启动建设'), (4, '项', '专业服务')],
 values=('VALUE', '价值优势', '把一次采购，做成一套机制',
  [('阳光', '采购信息统一发布，过程公开、结果可查。'),
   ('规范', '依据政策文件建设与运行，流程标准化。'),
   ('长效', '从一次性采购，走向常态化服务机制。')]),
 related=['area-asset', 'product-software', 'scene-rural']))

P.append(dict(
 key='scene-digital', type='scene', no='04', en='DIGITAL ECONOMY',
 title='助力数字经济', claim='可信的数字交易基础设施',
 sub='探索 5G、人工智能、大数据、物联网、云计算、区块链等新技术在交易市场平台建设中的融合应用。',
 banner='assets/img/banners/scene-digital.webp',
 lead='技术不是点缀，它决定了交易平台的上限。',
 paras=[
  '公司积极探索 5G、人工智能、大数据、物联网、云计算、区块链等新技术在交易市场平台建设中的融合应用，为交易场所赋能赋智。',
  '以电子认证、量子保密通信与区块链为底座，构建可信的数字交易基础设施，让新技术在真实的交易场景里落地。'],
 state=('DIGITAL ECONOMY', '为交易场所<em>赋能赋智</em>。'),
 services=('TECHNOLOGY', '技术方向', '四项技术，一个共同的目标：让交易可信。',
  [('创新“基”建安全平台', '唯一性、便利性、公正性、完整性、安全性、防篡改、抗抵赖与法律合规。'),
   ('电子认证服务', '为数据进行传输控制与认证保护，建设可信网络身份认证体系。'),
   ('量子保密通信', '面向政务、司法、金融、交通、能源等领域提供量子信息安全服务。'),
   ('区块链技术应用', '公链、联盟链、私链与“区块链 + 行业 SaaS”，为中小企业建立信用档案。')]),
 stats=[(4, '大', '技术方向'), (8, '项', '安全特性'), (1, '个', '可信底座')],
 values=('VALUE', '价值优势', '不追概念，只解决问题',
  [('可信底座', '认证、加密、存证三层能力，构成交易的技术信任基础。'),
   ('技术融合', '不追逐概念，只选择能在交易场景中跑通的技术。'),
   ('场景赋能', '每一项技术，都对应一个具体的业务问题。')]),
 related=['area-procure', 'product-blockchain', 'scene-data']))

P.append(dict(
 key='scene-data', type='scene', no='05', en='DATA OPERATION',
 title='交易数据运营', claim='中国—东盟交易数据运营平台',
 sub='建设中国—东盟交易数据运营平台，以交易数据为新型生产要素，丰富平台数字化服务生态。',
 banner='assets/img/banners/scene-data.webp',
 lead='从“交易在哪发生”，到“价值在哪产生”——数据给出答案。',
 paras=[
  '围绕中国—东盟资源要素交易平台建设中国—东盟交易数据实验室，通过整合、运营各类资源要素交易数据，为各类企业提供数字化转型和资源优化配置服务。',
  '建立中国—东盟交易数据中台，提供安全、高效的交易数据分析与存储，以交易数据作为新型生产要素，创新交易价值。'],
 state=('DATA OPERATION', '让交易更有价值，<em>让数据说话</em>。'),
 services=('DIRECTION', '运营方向', '五个方向，把数据变成服务。',
  [('政府引导市场监管', '以数据支撑政府监管，让交易全程阳光透明。'),
   ('发挥平台聚集功能', '聚集各类资源要素交易场景与数据资产。'),
   ('连接金融服务机构', '建立政府、企业及金融机构之间高效的沟通桥梁。'),
   ('服务中小企业成长', '为企业提供多维度数字化、信息化服务。'),
   ('助推产业升级发展', '助推中国—东盟产业数字化发展。')]),
 stats=[],
 values=('VALUE', '价值优势', '看得见、算得清、用得上',
  [('看得见', '交易全景可视化，区域、品类、价格趋势一目了然。'),
   ('算得清', '统一口径与模型，让数据可以比较、可以预测。'),
   ('用得上', '数据产品直接嵌入监管、金融与经营决策。')]),
 related=['area-agri', 'product-data', 'scene-etrade']))

# ============================================================
# 产品中心
# ============================================================
P.append(dict(
 key='product-etrade', type='product', no='01', en='E-TRADING PLATFORM',
 title='e交易平台', claim='全国性、综合性电子商务云平台',
 sub='集非标资产交易与招标采购于一体，覆盖资产处置、招标采购与快捷采购三类交易。',
 banner='assets/img/banners/product-etrade.webp',
 lead='一套平台，覆盖资产处置、招标采购与快捷采购三类交易。',
 paras=[
  'e 交易由北部湾产权交易所集团牵头国内多家省级产权交易机构投资建设运营，是集非标资产交易与招标采购为一体的全国性、综合性电子商务云平台。',
  '平台包含资产处理、招标采购、快捷采购三大系统，集成 CA 加密、全国供应商库与行业专家库，为交易机构与企业提供全流程在线交易服务。'],
 state=('E-TRADING PLATFORM', '让交易<em>更容易</em>。'),
 services=('MODULE', '产品构成', '三个系统，覆盖非标与标准两类交易。',
  [('资产处理系统', '实物资产、权益类资产、增资扩股等非标资产处置，专业包装、全国推广。'),
   ('招标采购系统', '六种招标采购方式线上全流程，CA 加密、供应商库、专家库与模板库。'),
   ('快捷采购系统', '与企业 ERP 对接，多种竞价方式，服务轻值品与标准品采购。'),
   ('平台运营服务', '广西及东盟区域推广运营、交易规则配置与用户服务。')]),
 stats=[(83000, '+', '入驻会员'), (32000, '+', '产权交易'), (2200, '亿+', '成交金额')],
 values=('VALUE', '产品特性', '全国网络，全流程在线',
  [('全国性网络', '多家省级产权交易机构共同建设运营，资源跨区域配置。'),
   ('全流程在线', '从挂牌、报名、竞价到结算鉴证，全部线上完成。'),
   ('安全合规', 'CA 加密保护与标准公告模板，全程留痕、对接监管。')]),
 related=['area-enterprise', 'scene-etrade', 'product-data']))

P.append(dict(
 key='product-rural', type='product', no='02', en='E-RURAL PLATFORM',
 title='E农村 · 农村产权流转交易信息系统', claim='“1+N”五级联动',
 sub='按照“1+N”模式构建、覆盖全区的农村产权流转交易信息系统平台。',
 banner='assets/img/banners/product-rural.webp',
 lead='一个平台，把登记、交易、金融配套与市场监督放在一起。',
 paras=[
  '平台按照“1+N”模式构建，覆盖全区、统一规则，集登记、交易、金融配套、市场监督于一体，实现区、市、县、乡、村五级联动。',
  '系统包含产权交易、农村征信、三资管理、涉农招标采购、农业大数据、农特电商六大子系统，为农村产权便捷、高效流转提供支撑。'],
 state=('E-RURAL PLATFORM', '让乡村资源<em>顺畅流转</em>。'),
 services=('SUBSYSTEM', '子系统', '六个子系统，一套涉农数据底座。',
  [('农村产权交易系统', '挂牌申请、审核受理、组织交易、合同签订、价款结算、交易鉴证全流程管理。'),
   ('农村征信系统', '采集涉农信息，缓解农民贷款难，防范信贷风险。'),
   ('三资管理系统', '集体资金、资产、资源管理民主化、科学化、规范化。'),
   ('涉农招标采购系统', '涉农物资采购全流程电子化，公开透明。'),
   ('农业大数据', '交易数据图形化展示，分析交易量、金额与价格趋势。'),
   ('农特电商', 'B2B 农特产交易平台，来源可追溯，连接小农户与大市场。')]),
 stats=[('1+N', '', '建设模式'), (5, '级', '区市县乡村'), (6, '个', '子系统')],
 values=('VALUE', '产品特性', '统一平台，五级贯通',
  [('统一规则', '全区一套交易规则与流程，跨层级数据互通。'),
   ('数据归集', '交易、征信、三资数据在县域内打通。'),
   ('金融配套', '以数据和交易为支撑，引入信贷与保险服务。')]),
 related=['scene-rural', 'area-enterprise', 'product-software']))

P.append(dict(
 key='product-software', type='product', no='03', en='SOFTWARE PROCUREMENT',
 title='广西正版软件集中采购平台', claim='阳光、规范、长效',
 sub='提供集中采购服务和软件正版化配套服务，实现集中采购信息统一发布常态化。',
 banner='assets/img/banners/product-software.webp',
 lead='让每一次正版软件采购，都发生在阳光下。',
 paras=[
  '根据桂权〔2020〕10 号、桂新出〔2020〕56 号文件精神，公司与北部湾产权交易所集团共同作为建设主体，建设广西正版化软件集中采购平台。',
  '平台为批量采购正版软件提供阳光、规范、长效的服务，并配套信息化评估、软件资产管理与资质咨询，覆盖软件资产的全生命周期。'],
 state=('SOFTWARE PROCUREMENT', '阳光采购，<em>长效常态</em>。'),
 services=('SERVICE', '平台服务', '采购只是起点，管理才是长期价值。',
  [('集中采购服务', '采购信息统一发布，批量采购流程标准化、结果可查。'),
   ('正版化配套服务', '政策解读、实施路径与正版化工作支撑。'),
   ('软件资产管理', '采购、分发、维护、使用及报废全生命周期管理。'),
   ('评估与资质咨询', '第三方信息化评估、IT 企业资质建设与涉软政策咨询。')]),
 stats=[(2020, '', '平台启动建设'), (2, '份', '政策文件依据'), (4, '项', '配套服务')],
 values=('VALUE', '产品特性', '政策依据清晰，流程标准统一',
  [('阳光', '集中采购信息统一发布，过程公开、结果可查。'),
   ('规范', '依据政策文件建设与运行，流程标准化。'),
   ('长效', '从一次性采购走向常态化服务机制。')]),
 related=['area-asset', 'scene-software', 'product-ca']))

P.append(dict(
 key='product-data', type='product', no='04', en='DATA PLATFORM',
 title='中国—东盟交易数据运营平台', claim='交易数据实验室与数据中台',
 sub='提供交易数据的采集、治理、分析与运营服务，让数据成为可运营的生产要素。',
 banner='assets/img/banners/product-data.webp',
 lead='交易数据在这里被整理、被理解，然后被使用。',
 paras=[
  '平台围绕中国—东盟资源要素交易平台建设交易数据实验室与交易数据中台，开展数据资产化及确权登记、流转交易研究。',
  '为政府监管、资产配置和投资顾问提供综合交易数据运营服务，打造交易大数据获取、分析及应用的生态体系。'],
 state=('DATA PLATFORM', '让数据<em>真正可用</em>。'),
 services=('MODULE', '平台构成', '从数据接入，到数据产品。',
  [('数据实验室', '数据资产化、确权登记与流转交易规则研究。'),
   ('交易数据中台', '多源数据采集、治理、存储与统一资产目录。'),
   ('数据分析服务', '区域、品类、价格趋势分析与可视化。'),
   ('数据产品运营', '面向政府、企业与金融机构的指数、报告与风控服务。')]),
 stats=[(1, '个', '数据实验室'), (1, '个', '数据中台'), (5, '类', '数据服务')],
 values=('VALUE', '产品特性', '统一、安全、可运营',
  [('统一口径', '跨区域、跨品类数据在同一套标准下治理。'),
   ('安全合规', '分级授权与脱敏机制，保障数据使用边界。'),
   ('可运营', '数据以产品形式输出，直接进入业务场景。')]),
 related=['area-agri', 'scene-data', 'product-ca']))

P.append(dict(
 key='product-ca', type='product', no='05', en='GUANGXI CA',
 title='广西CA · 可信数字身份与量子安全', claim='区内唯一电子认证服务机构',
 sub='广西区内唯一获国家工信部行政许可的电子认证服务机构，提供数字证书与量子安全服务。',
 banner='assets/img/banners/product-ca.webp',
 lead='一张证书，是数字世界里的身份证。',
 paras=[
  '广西 CA 于 2003 年注册成立，是广西区内唯一获国家工信部行政许可的电子认证服务机构，推动构建全区统一电子认证体系。',
  '服务覆盖全区及 14 个地市公共资源交易中心、社保等领域；同时应用量子安全保密传输技术产品，为政务、司法、金融、交通、能源等重点领域提供量子信息安全服务。'],
 state=('GUANGXI CA', '无身份，<em>不交易</em>。'),
 services=('SERVICE', '服务内容', '认证、签名、加密，构成可信身份体系。',
  [('数字证书服务', '面向机构与个人的证书签发、更新、吊销与身份核验。'),
   ('电子签名与时间戳', '可靠的电子签名与可信时间戳，具备法律效力。'),
   ('量子安全服务', '量子保密通信与量子安全产品，服务重点行业领域。'),
   ('密码应用集成', '与业务系统融合的密码应用方案设计与实施。')]),
 stats=[(2003, '', '广西 CA 成立'), (14, '个', '地市覆盖'), (20, '年+', '认证服务')],
 values=('VALUE', '产品特性', '唯一、合规、可验证',
  [('区内唯一', '国家工信部行政许可的电子认证服务机构。'),
   ('法律效力', '符合电子签名法与密码管理相关规范。'),
   ('体系覆盖', '全区统一电子认证体系，跨系统互认。')]),
 related=['area-procure', 'scene-digital', 'product-blockchain']))

P.append(dict(
 key='product-blockchain', type='product', no='06', en='BLOCKCHAIN',
 title='科技金融区块链系统', claim='区块链 + 行业 SaaS',
 sub='提供公链、联盟链、私链核心底层产品，以及“区块链 + 行业 SaaS”解决方案。',
 banner='assets/img/banners/product-blockchain.webp',
 lead='让没有抵押物的中小企业，也能凭信用获得融资。',
 paras=[
  '系统提供公链、联盟链、私链等核心区块链底层产品，以及 SWTC 公链 + 行业 SaaS 平台 + 金融服务。',
  '企业无需购买软硬件、建设机房、招聘 IT 人员，即可通过互联网使用信息系统，为中小企业建立信用档案，破解融资难题。'],
 state=('BLOCKCHAIN', '让信用<em>可以被计算</em>。'),
 services=('MODULE', '产品构成', '底层链、行业应用与金融服务，三层组合。',
  [('区块链底层', '公链、联盟链、私链三类底层产品，按场景选型。'),
   ('行业 SaaS', '面向行业的区块链应用平台，开箱即用。'),
   ('信用档案', '为中小企业建立可验证的信用记录。'),
   ('供应链金融', '以真实交易与信用数据支撑融资服务。')]),
 stats=[(3, '类', '底层链产品'), (1, '套', '行业 SaaS'), (1, '个', '信用档案体系')],
 values=('VALUE', '产品特性', '低成本、可验证、易接入',
  [('低成本', '无需自建机房与团队，按需使用云端服务。'),
   ('可验证', '链上数据防篡改、可追溯，信用可核验。'),
   ('易接入', '标准化接口，与现有业务系统快速对接。')]),
 related=['area-procure', 'scene-digital', 'product-ca']))

BY = {p['key']: p for p in P}
GROUPS = {'area': [], 'scene': [], 'product': []}
for p in P: GROUPS[p['type']].append(p['key'])


def esc(s): return html.escape(s, quote=True)


def stat_html(v, suf, lab):
    if isinstance(v, int):
        num = f'<span data-count="{v}">0</span>'
    else:
        num = esc(str(v))
    suffix = f'<em>{esc(suf)}</em>' if suf else ''
    return f'<div class="dstat"><b>{num}{suffix}</b><span>{esc(lab)}</span></div>'


def build(p):
    t, k = p['type'], p['key']
    group = GROUPS[t]
    i = group.index(k)
    total = len(group)
    prev_k = group[i - 1] if i > 0 else None
    next_k = group[i + 1] if i < total - 1 else None

    # 相关模块
    rel = ''
    for rk in p['related']:
        r = BY[rk]
        rel += (f'<a href="{r["key"]}.html"><div class="rimg"><img src="{r["banner"]}" alt="{esc(r["title"])}" loading="lazy"></div>'
                f'<div class="rt"><h4>{esc(r["title"])}</h4><span class="rk">{TYPE_CN[r["type"]]}</span></div></a>')

    # 上/下一篇
    if prev_k:
        pr = BY[prev_k]
        prev_html = f'<a href="{pr["key"]}.html"><small>← 上一篇</small><b>{esc(pr["title"])}</b></a>'
    else:
        prev_html = f'<a href="{OVERVIEW[t]}"><small>{TYPE_EN[t]}</small><b>查看全部{TYPE_CN[t]}</b></a>'
    if next_k:
        nx = BY[next_k]
        next_html = f'<a href="{nx["key"]}.html"><small>下一篇 →</small><b>{esc(nx["title"])}</b></a>'
    else:
        next_html = f'<a href="{OVERVIEW[t]}"><small>{TYPE_EN[t]}</small><b>查看全部{TYPE_CN[t]}</b></a>'

    serv_items = ''.join(
        f'<div class="dserv-i"><span class="sn">{n:02d}</span><h3>{esc(h)}</h3><p>{esc(txt)}</p></div>'
        for n, (h, txt) in enumerate(p['services'][3], 1))
    val_items = ''.join(
        f'<div class="dval"><h4>{esc(h)}</h4><p>{esc(txt)}</p></div>'
        for h, txt in p['values'][3])
    stats_block = ''
    if p['stats']:
        stats_block = ('<section class="dsec"><div class="wrap"><div class="dstats-lab">KEY FIGURES · 关键数据</div>'
                       '<div class="dstats">' + ''.join(stat_html(*s) for s in p['stats']) + '</div></div></section>')

    paras = ''.join(f'<p class="dtext">{esc(x)}</p>' for x in p['paras'])

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{esc(p['sub'])}">
<title>{esc(p['title'])} - 广西计算机有限责任公司</title>
<link rel="icon" type="image/png" href="assets/img/_img_index_bbw-logo.png">
<link rel="stylesheet" href="css/main.css">
<link rel="stylesheet" href="css/pages.css">
<link rel="stylesheet" href="css/sub.css">
</head>
<body class="dark-hero" data-page="{'products' if t == 'product' else 'business'}">

<header class="dhero">
  <div class="dhero-media"><img src="{p['banner']}" alt="{esc(p['title'])}"></div>
  <div class="dhero-shade"></div>
  <div class="wrap dhero-in">
    <div class="dhero-crumb"><a href="index.html">首页</a><i>/</i><a href="{OVERVIEW[t]}">{TYPE_CN[t]}</a><i>/</i><b>{esc(p['title'])}</b></div>
    <div class="dhero-eyebrow">{t.upper()} {p['no']} · {TYPE_CN[t]}</div>
    <h1>{esc(p['title'])}</h1>
    <p class="dhero-claim">{esc(p['claim'])}</p>
    <p class="dhero-sub">{esc(p['sub'])}</p>
  </div>
  <div class="dhero-bot"><div class="wrap"><span><b>{p['no']}</b> / {total:02d} &nbsp; {p['en']}</span><span class="sc">SCROLL</span></div></div>
</header>

<main>
  <section class="dsec no-line">
    <div class="wrap dgrid">
      <aside class="drail"><span class="rno">01</span><span class="ren">OVERVIEW</span></aside>
      <div class="dbody">
        <p class="dlead">{esc(p['lead'])}</p>
        {paras}
      </div>
    </div>
  </section>

  <section class="dstate">
    <div class="wrap st-in">
      <div><div class="st-en">{p['state'][0]}</div><p>{p['state'][1]}</p></div>
      <div class="st-note"><b>广西计算机有限责任公司</b>{TYPE_CN[t]} · {esc(p['title'])}</div>
    </div>
  </section>

  <section class="dsec">
    <div class="wrap dgrid">
      <aside class="drail"><span class="rno">02</span><span class="ren">{p['services'][0]}</span></aside>
      <div class="dbody">
        <div class="dhead"><h2 class="dhead-h">{p['services'][1]}</h2><p class="dhead-p">{esc(p['services'][2])}</p></div>
        <div class="dserv">{serv_items}</div>
      </div>
    </div>
  </section>

  {stats_block}

  <section class="dsec">
    <div class="wrap dgrid">
      <aside class="drail"><span class="rno">03</span><span class="ren">{p['values'][0]}</span></aside>
      <div class="dbody">
        <div class="dhead"><h2 class="dhead-h">{p['values'][2]}</h2></div>
        <div class="dvals">{val_items}</div>
      </div>
    </div>
  </section>

  <section class="dsec">
    <div class="wrap dgrid">
      <aside class="drail"><span class="rno">04</span><span class="ren">RELATED</span></aside>
      <div class="dbody"><div class="drel">{rel}</div></div>
    </div>
  </section>

  <section class="dpn-sec">
    <div class="wrap"><div class="dpn">{prev_html}{next_html}</div></div>
  </section>
</main>

<script src="js/site.js"></script>
</body>
</html>
'''


for p in P:
    path = os.path.join(ROOT, p['key'] + '.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(build(p))
    print('built', p['key'] + '.html')
