# 业务详情页 · 典型业务场景配图提示词（25 张）

5 个业务页 × 每页 5 个场景 = **25 张**，与页面现有「典型业务场景」标题一一对应。

现状：19 张是浅灰占位（图标 + 文字），另 6 张借用的是别的板块图（国产化页借了采购/企业/数字化三张、
基础设施页借了企业卡、软件页借了资产上线和农业交易两张），与标题对不上。所以 25 张全部重新生成。

---

## 通用参数

**比例**：16:9，建议 1536×864 或更大。
> 卡片是 `object-fit:cover`：第一条跨两列（约 2.86:1）、其余单列（约 1.4:1）。16:9 是唯一两头都能接受的比例；
> 构图请把主体放在中间横向带状区域，上下各留约 15% 可裁空间，下三分之一保持干净偏暗（标题白字压在上面）。

**文件命名**：`assets/img/biz/scenes/{ai|domestic|infra|planning|software}-{01..05}.webp`

**每条提示词末尾统一追加（下称 STYLE）**：
```
editorial corporate photography, shot on 35mm, natural light, muted blue-grey palette with warm neutral accents,
photorealistic, high-end annual-report aesthetic, clean uncluttered composition, shallow depth of field,
sharp focus on the subject, lower third uncluttered and slightly darker, no text, no logos, no watermark, 16:9
```

**统一负面提示词**：
```
cartoon, illustration, 3d render, cgi, plastic skin, oversaturated, neon, lens flare, heavy vignette,
text, letters, chinese characters, watermark, logo, distorted hands, extra fingers, cluttered desk, fisheye
```

> 屏幕上出现的界面/文字一律留「抽象、不可读」——让模型画真字必出乱码。

---

## 一、人工智能与智能应用（ai）

1. **交易机器人：国资交易、招投标及通用业务问答**
   `Over-the-shoulder view of a procurement professional at a modern desk using an AI chat assistant on a 27-inch monitor, abstract unreadable conversation panel, glass-walled office softly blurred behind`

2. **招标文件编制辅助与智能审核**
   `Two reviewers in shirtsleeves in a quiet meeting room, long tender document on a large screen with abstract highlighted clauses, printed pages spread across the table, soft side light`

3. **采购需求及评分办法辅助编制**
   `Procurement specialist drafting scoring criteria on a laptop, second screen showing an abstract structured form with checkboxes, notebook and pen beside, calm bright modern office`

4. **业务知识库、制度检索和智能客服**
   `Employee searching an internal knowledge base on a desktop in an open-plan office, abstract search results panel on screen, rows of binders softly out of focus behind`

5. **专业业务文档识别、信息抽取及辅助处理**
   `Hands holding a phone scanning a stack of business documents, tablet beside it showing abstract extracted fields, clean desk, soft daylight, very shallow depth of field`

## 二、国产化产品与服务（domestic）

1. **国产台式机、笔记本电脑及办公终端采购供应**
   `Bright IT staging room with rows of new desktop PCs and laptops neatly arranged on tables, asset tags and cartons, a technician checking inventory in the background`

2. **国产服务器、存储及配套设备供应**
   `Two engineers unpacking and inspecting a new rack server in a data-center staging area, anti-static packaging and storage arrays behind, cool light with warm highlights`

3. **国产操作系统、办公软件、数据库等软件产品供应**
   `IT administrator installing a new operating system on a desktop PC, abstract installation progress screen, software media and license certificates on the desk`

4. **国产化项目设备清单配置、产品选型和交付**
   `Three colleagues at a project table comparing equipment specification sheets and a product catalog on a laptop, sample devices on a shelf behind, bright meeting room`

5. **软硬件安装部署、使用培训及售后服务**
   `Trainer beside a projection screen explaining a new system to a small group of employees in a modern training room, laptops open, natural daylight`

## 三、信息基础设施服务（infra）

1. **数据中心机房设备及配套环境建设**
   `Wide shot of a freshly built data-center cold aisle, symmetrical rows of server racks, blue LED indicators, raised floor, crisp overhead lighting, no people`

2. **服务器、存储和网络设备部署调试**
   `Engineer with a laptop connected to an open rack, patch panels and neatly bundled cabling, adjusting a server in a data-center aisle, concentrated expression`

3. **云资源配置及业务系统运行环境准备**
   `Cloud engineer at a workstation with three monitors showing abstract dashboards and a network topology diagram, dim operations room, cool ambient glow`

4. **数据备份、恢复验证和容灾建设**
   `Two engineers verifying a backup and disaster-recovery run in a secure server room, archive storage library on one side, abstract recovery progress on screen`

5. **网络安全设备部署及安全运维支持**
   `Security operations center, analyst monitoring a wall display of abstract dashboards and network topology, dark room with cool blue light, colleagues blurred behind`

## 四、信息化规划与咨询服务（planning）

1. **集团信息化建设总体规划与专项方案设计**
   `Consulting workshop, four people around a table with a printed enterprise-architecture poster, sticky notes on a glass wall, whiteboard sketches, bright modern office`

2. **统一门户、统一身份认证等系统建设方案设计**
   `Close-up of hands sketching a single-sign-on flow diagram on a whiteboard, laptop beside it showing an abstract portal wireframe, soft natural light`

3. **OA 办公、档案管理及业务系统建设需求分析与方案设计**
   `Business analyst interviewing two department staff at a meeting table, laptop and printed requirement forms, handwritten notes, warm daylight`

4. **集团管理系统架构设计及系统建设路径规划**
   `Architect standing before a large wall-mounted architecture diagram of abstract blocks and arrows, presenting to two colleagues in a modern meeting room`

5. **信息化项目立项咨询、技术路线论证及投资建设计划编制**
   `Formal review meeting, four professionals discussing a roadmap and budget table on a large screen, papers and coffee cups, glass conference room with city view`

## 五、软件研发与数据服务（software）

1. **资产管理与运营应用**
   `Asset management office, staff reviewing a property asset register on dual monitors with an abstract table and map view, modern enterprise workspace`

2. **交易机器人及交易业务应用**
   `Trading platform operations desk, wide monitor showing an abstract transaction dashboard with charts, analyst typing, cool screen glow, evening office`

3. **农业交易服务应用**
   `Agricultural industry service center, staff presenting an order and supply dashboard on a wall screen to a visitor, one person holding a tablet, bright daylight`

4. **业务数据治理与分析**
   `Data analyst at a desk with a large abstract dashboard of charts and tables on screen, data-flow sketch on the whiteboard behind, focused, morning light`

5. **配套业务系统定制开发**
   `Software team at a long desk, two developers pair-programming on an abstract code editor, sticky notes on the monitor edge, task board on the wall behind`
