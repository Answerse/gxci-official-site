/* 广西计算机公司官网 · 公共逻辑 */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* 以 <script> 标签加载数据：双击本地文件（file://）打开时 fetch JSON 会被
     CORS 拦截，新闻板块会永远停在"加载中"；script 标签不受此限制，
     file:// 与 http 部署两种方式通用。数据源仍为 data/*.json，
     由 tools/make_data_js.py 生成为同名 .js，更新新闻后要重跑该脚本。 */
  function loadScript(src) {
    return new Promise(function (res, rej) {
      var s = document.createElement('script');
      s.src = src;
      s.onload = function () { res(); };
      s.onerror = function () { rej(new Error('数据加载失败: ' + src)); };
      document.head.appendChild(s);
    });
  }
  window.__loadData = loadScript;

  /* ---------- 导航 & 页脚 ---------- */
  /* 线形图标集（V184）：24×24 / 1.4 描边 / 圆头圆角，颜色一律 currentColor。
     只定义一次，子菜单卡片用 <use href="#id"> 引用。 */
  var SPRITE = '<svg class="ico-sprite" aria-hidden="true" focusable="false">'
    + '<symbol id="ic-org" viewBox="1.8 1.8 20.4 20.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<rect x="9" y="3" width="6" height="5.4" rx="1"/><rect x="3" y="15.6" width="6" height="5.4" rx="1"/><rect x="15" y="15.6" width="6" height="5.4" rx="1"/><path d="M12 8.4V12M6 15.6V12h12v3.6"/></symbol>'
    + '<symbol id="ic-leaf" viewBox="1.8 1.8 20.4 20.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<path d="M12 2.6c4 1.2 6.6 4.6 6.6 9.2 0 4.2-2.4 7.6-6.6 9.6-4.2-2-6.6-5.4-6.6-9.6 0-4.6 2.6-8 6.6-9.2Z"/><path d="M12 5.6v15.8"/></symbol>'
    + '<symbol id="ic-build" viewBox="1.8 1.8 20.4 20.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<path d="M3 21h18"/><path d="M4.4 21V8.6l5.2-3.2V21"/><path d="M9.6 21V11.6L19 8.8V21"/><path d="M6.6 11.4v1.4M6.6 15.4v1.4M13.4 13.4v1.4M13.4 17.4v1.4"/></symbol>'
    + '<symbol id="ic-chip" viewBox="1.8 1.8 20.4 20.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<rect x="6.6" y="6.6" width="10.8" height="10.8" rx="1.6"/><path d="M9.6 2.6v4M14.4 2.6v4M9.6 17.4v4M14.4 17.4v4M2.6 9.6h4M2.6 14.4h4M17.4 9.6h4M17.4 14.4h4"/></symbol>'
    + '<symbol id="ic-cloud" viewBox="1.8 1.8 20.4 20.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<path d="M6 19h12a5 5 0 0 0 .6-10 7.4 7.4 0 0 0-14 1.8A4.6 4.6 0 0 0 6 19Z"/></symbol>'
    + '<symbol id="ic-cocoon" viewBox="1.8 1.8 20.4 20.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<ellipse cx="12" cy="12" rx="7" ry="8.6"/><path d="M5.6 8.4c3.9 2.3 8.9 2.3 12.8 0M5.6 15.6c3.9-2.3 8.9-2.3 12.8 0"/></symbol>'
    + '<symbol id="ic-orange" viewBox="1.8 1.8 20.4 20.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<circle cx="12" cy="13.6" r="7.4"/><path d="M12 6.2C11.6 3.8 12.9 2.3 15.2 2"/><path d="M15.2 2c1.9-.2 3.2.9 3.5 2.8-2 .3-3.2-.8-3.5-2.8Z"/></symbol>'
    + '<symbol id="ic-tree" viewBox="1.8 1.8 20.4 20.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<path d="M12 2.8 4.6 12.4h3.7L3.6 18.6h16.8l-4.7-6.2h3.7L12 2.8Z"/><path d="M12 18.6V21.4"/></symbol>'
    + '<symbol id="ic-house" viewBox="1.8 1.8 20.4 20.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<path d="M3 10.4 12 3l9 7.4"/><path d="M5.6 9V20.6h12.8V9"/><path d="M9.8 20.6v-5.6h4.4v5.6"/></symbol>'
    + '<symbol id="ic-horn" viewBox="1.8 1.8 20.4 20.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<path d="M3.2 9.4v5.2h3.8l5.6 4V5.4L7 9.4H3.2Z"/><path d="M16.6 7.6a4.4 4.4 0 0 1 0 8.8"/></symbol>'
    + '<symbol id="ic-paper" viewBox="1.8 1.8 20.4 20.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<rect x="3.2" y="4.4" width="17.6" height="15.2" rx="1.6"/><path d="M7.4 9h4.8M7.4 12.6h9.2M7.4 16.2h6.4"/></symbol>'
    + '<symbol id="ic-flag" viewBox="1.8 1.8 20.4 20.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<path d="M5.4 21.2V2.8"/><path d="M5.4 3.6h12.4l-2.1 4.2 2.1 4.2H5.4"/></symbol>'
    + '<symbol id="ic-cap" viewBox="1.8 1.8 20.4 20.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<path d="M12 3 2.6 7.6 12 12.2l9.4-4.6L12 3Z"/><path d="M6.8 9.8v4.6c0 1.9 2.3 3.2 5.2 3.2s5.2-1.3 5.2-3.2V9.8"/></symbol>'
    + '<symbol id="ic-info" viewBox="1.8 1.8 20.4 20.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<circle cx="12" cy="12" r="8.6"/><path d="M12 11v5.4"/><path d="M12 7.4v.6"/></symbol>'
    + '<symbol id="ic-mile" viewBox="1.8 1.8 20.4 20.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<path d="M6.4 2.8v18.4"/><path d="M6.4 7.2h7.4M6.4 12h11M6.4 16.8h6"/></symbol>'
    + '<symbol id="ic-user" viewBox="1.8 1.8 20.4 20.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<circle cx="12" cy="7.8" r="4"/><path d="M4.4 20.8c0-4 3.4-7 7.6-7s7.6 3 7.6 7"/></symbol>'
    + '<symbol id="ic-pin" viewBox="1.8 1.8 20.4 20.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<path d="M12 21.2c4.3-5 7.2-8.8 7.2-11.6A7.2 7.2 0 0 0 4.8 9.6c0 2.8 2.9 6.6 7.2 11.6Z"/><circle cx="12" cy="9.6" r="2.8"/></symbol>'
    + '<symbol id="ic-doc" viewBox="1.8 1.8 20.4 20.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<path d="M5.6 2.8h8.2L18.4 7.4V21.2H5.6Z"/><path d="M13.8 2.8v4.6h4.6"/><path d="M8.8 12.2h6M8.8 16h4"/></symbol>'
    /* V200 新增：发展历程=钟表 / 公司动态=报纸 / 公司简介=钢笔 */
    + '<symbol id="ic-clock" viewBox="1.8 1.8 20.4 20.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<circle cx="12" cy="12" r="8.6"/><path d="M12 6.9V12l3.7 2.3"/></symbol>'
    + '<symbol id="ic-news" viewBox="1.8 1.8 20.4 20.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<rect x="3.4" y="5.2" width="17.2" height="13.6" rx="1.4"/><rect x="6.6" y="8.6" width="5.6" height="3.8" rx=".6"/><path d="M14.9 8.6h2.5M14.9 12.4h2.5M6.6 15.8h10.8"/></symbol>'
    + '<symbol id="ic-pen" viewBox="1.8 1.8 20.4 20.4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    + '<path d="M16.8 3.4 20.6 7.2 8.9 18.9l-4.9 1.2 1.2-4.9L16.8 3.4Z"/><path d="M14.4 5.8l3.8 3.8"/><path d="M5.6 15.6l2.6 2.6"/></symbol>'
    + '</svg>';

  /* 通栏子菜单（V184）：一行卡片 —— 线形图标 + 子模块标题 + 一行说明。
     左侧「模块名 + 简介 + 查看全部」整块已撤：一级导航项本身就是模块索引页入口，
     面板里再放一遍标题和「查看全部」是把同一件事说两遍。 */
  function mega(items) {
    var h = '<div class="mega"><div class="wrap"><div class="mega-cards">';
    items.forEach(function (it) {
      h += '<a class="ml" href="' + it[1] + '">'
        + '<svg class="ml-ic" aria-hidden="true" focusable="false"><use href="#' + it[3] + '"></use></svg>'
        + '<b>' + it[0] + '</b><small>' + it[2] + '</small></a>';
    });
    return h + '</div></div></div>';
  }

  var NAV = SPRITE
    + '<div class="pbar"></div>'
    + '<nav class="nav"><div class="nav-in">'
    + '<a class="logo" href="index.html">'
    + '<img src="assets/img/_img_index_bbw-logo.png?v=75" alt="logo">'
    + '<span class="logo-t">广西计算机有限责任公司<small>GUANGXI COMPUTER INC.</small></span></a>'
    + '<ul class="menu">'
    + '<li><a class="m" data-nav="index" href="index.html">首页</a></li>'
    + '<li class="has-mega"><a class="m" data-nav="business" href="business.html">业务领域</a>'
    + mega([
      ['集团型企业数字化转型', 'area-enterprise.html', '全周期数字化建设与运维', 'ic-org'],
      ['桂农易通产业服务平台', 'area-agri.html', '特色农业产业互联网平台', 'ic-leaf'],
      ['桂资通资产运营平台', 'area-asset.html', '国有资产数字化管理运营', 'ic-build'],
      ['国产软硬件产品集采服务平台', 'area-procure.html', '正版化 · 国产化 · 降本增效', 'ic-chip']
    ])
    + '</li>'
    + '<li class="has-mega"><a class="m" data-nav="products" href="products.html">产品中心</a>'
    /* V181：桂资通是业务领域（area-asset.html），不进产品中心，故原「桂资通」分组撤掉；
       菜单与 products.html 的 5 张卡一一对应，桂农易通既是业务也是产品，这里作为产品条目 */
    + mega([
      ['桂农易通', 'product-nongyi.html', '特色农产品产业服务平台', 'ic-leaf'],
      ['茧易通', 'case-jiayitong.html', '桑蚕茧丝绸产业服务平台', 'ic-cocoon'],
      ['陈皮通', 'case-chenpitong.html', '浦北陈皮产业服务平台', 'ic-orange'],
      ['林易通', 'case-linyitong.html', '林产品交易线上综合平台', 'ic-tree'],
      ['桂资通', 'case-house.html', '国企房产资产统一登记', 'ic-house']
    ])
    + '</li>'
    + '<li class="has-mega"><a class="m" data-nav="news" href="news.html">新闻中心</a>'
    + mega([
      ['公司动态', 'news.html?cat=3', '经营与项目进展', 'ic-news'],
      ['行业资讯', 'news.html?cat=4', '政策与产业观察', 'ic-paper'],
      ['党建工作', 'news.html?cat=5', '党建活动与学习', 'ic-flag'],
      ['主题教育', 'news.html?cat=17', '专题教育成果', 'ic-cap']
    ])
    + '</li>'
    + '<li class="has-mega"><a class="m" data-nav="about" href="about.html">关于我们</a>'
    + mega([
      ['公司简介', 'about.html?s=profile', '定位、使命与价值主张', 'ic-pen'],
      ['发展历程', 'about.html?s=history', '1986—2026 四个十年', 'ic-clock'],
      ['招聘信息', 'about.html?s=jobs', '人才招聘与录用公示', 'ic-user'],
      ['联系我们', 'about.html?s=contact', '地址、热线与交通', 'ic-pin'],
      ['信息公开', 'about.html?s=open', '企业信息公开', 'ic-doc']
    ])
    + '</li>'
    + '</ul>'
    + '<button class="burger" aria-label="菜单"><i></i><i></i><i></i></button>'
    + '</div></nav>'
    + '<div class="m-drawer">'
    + '<a href="index.html">首页</a>'
    + '<a href="business.html">业务领域</a>'
    + '<a href="products.html">产品中心</a>'
    + '<a href="news.html">新闻中心</a>'
    + '<a href="about.html">关于我们</a>'
    + '</div>'
    + '<button id="top" aria-label="回到顶部">↑</button>';

  /* 友情链接：取自 www.gxci.com.cn 页脚（名称、地址与官网一致） */
  /* V199：显示名改短名、按用户指定分两列（列序即数组序，CSS 按 4 行竖排）；
     江苏易交易随两列方案移除。URL 仍为各机构官网，与 gxci.com.cn 页脚一致 */
  /* V210：友链名称改回原站全称（gxci.com.cn 页脚原文，除已删的江苏易交易外逐条照抄） */
  var FLINKS = [
    ['广西壮族自治区人民政府国有资产监督管理委员会', 'http://gzw.gxzf.gov.cn'],
    ['广西国控资本运营集团有限责任公司', 'https://www.gxgkjt.com'],
    ['广西宏桂资本运营集团有限公司', 'https://www.gxhgzb.com'],
    ['北部湾产权交易所集团股份有限公司', 'http://www.bbwcq.com'],
    ['广西壮族自治区数字证书认证中心有限公司', 'http://www.gxca.com.cn'],
    ['广西电子学会', 'http://www.gxie.org'],
    ['中国东盟-知识产权运营平台', 'http://www.gxipop.com'],
    ['南宁市互联网举报·辟谣网站', 'http://www.nnjbpy.org.cn/']
  ];
  var FCONTACT = [
    ['地址', '南宁市青秀区枫林路18号'],
    ['网址', 'www.gxci.com.cn'],
    ['邮箱', 'gxjsj@bbwcq.com'],
    ['举报电话', '0771-5851825'],
    ['举报邮箱', 'gxcc@bbwcq.com']
  ];

  var FOOT = ''
    + '<footer>'
    + '<div class="wrap ft-main">'
    + '<div class="ft-logo"><img src="assets/img/_img_index_bbw-logo.png?v=75" alt=""><span><b>广西计算机有限责任公司</b><small>GUANGXI COMPUTER INC.</small></span></div>'
    + '<div class="ft-cols">'
    + '<div class="ft-left">'
    + '<div class="ft-qrbox"><img class="qrcode ft-qr" src="assets/img/_img_index_ewm.png?v=109" alt="官方微信二维码"><span class="ft-qr-t">微信公众号</span></div>'
    + '<div class="ft-contact"><dl>'
    + FCONTACT.map(function (it) { return '<div><dt>' + it[0] + '</dt><dd>' + it[1] + '</dd></div>'; }).join('')
    + '</dl></div>'
    + '</div>'
    + '<div class="ft-links"><h4>友情链接</h4><ul>'
    + FLINKS.map(function (it) { return '<li><a href="' + it[1] + '" target="_blank" rel="noopener">' + it[0] + '</a></li>'; }).join('')
    + '</ul></div>'
    + '</div>'
    + '</div>'
    + '<div class="wrap ft-bar"><span class="ft-cr"><span>Copyright &copy; 1986-2026</span> <span>广西计算机有限责任公司 版权所有</span></span>'
    + '<span class="ft-rec"><a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener">桂ICP备20002211号-4</a><i>|</i>'
    + '<a href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=45010802000357" target="_blank" rel="noopener">桂公网安备 45010802000357号</a></span></div></footer>';

  document.body.insertAdjacentHTML('afterbegin', NAV);
  document.body.insertAdjacentHTML('beforeend', FOOT);

  var page = document.body.dataset.page || '';
  var cur = $('.menu a.m[data-nav="' + page + '"]');
  if (cur) cur.classList.add('act');

  /* 锚点兜底：scroll-behavior:smooth 下浏览器初始锚点跳转可能失效；
     目标若带 .rv 入场动画（translateY 46px），先置为最终态再定位，避免 46px 偏差 */
  function revealNow(el) {
    if (el.classList.contains('rv') && !el.classList.contains('in')) {
      el.style.transition = 'none';
      el.classList.add('in');
      requestAnimationFrame(function () { requestAnimationFrame(function () { el.style.transition = ''; }); });
    }
  }
  function jumpTo(hash, instant) {
    var el = document.querySelector(hash);
    if (!el) return false;
    revealNow(el);
    if (instant) {
      /* html{scroll-behavior:smooth} 下 behavior:'auto' 仍是平滑滚动，需临时关掉 */
      var root = document.documentElement;
      var prev = root.style.scrollBehavior;
      root.style.scrollBehavior = 'auto';
      el.scrollIntoView({ block: 'start' });
      root.style.scrollBehavior = prev;
      return true;
    }
    requestAnimationFrame(function () { el.scrollIntoView({ behavior: 'smooth', block: 'start' }); });
    return true;
  }
  /* 落位后 800ms 内校正几次：图片/字体陆续加载会让上方高度变化，落点因此漂移十几像素 */
  function settleTo(hash) {
    jumpTo(hash, true);
    var n = 0;
    (function step() {
      var el = $(hash);
      if (el) {
        var off = el.getBoundingClientRect().top - 96;
        if (Math.abs(off) > 3 && Math.abs(off) < 140) jumpTo(hash, true);
      }
      if (++n < 6) setTimeout(step, 200);
    })();
  }
  var hsh = location.hash.split('?')[0];
  if (hsh.length > 1 && $(hsh)) setTimeout(function () { settleTo(hsh); }, 80);
  /* 同页锚点链接：统一走 revealNow 定位，绕开入场动画位移 */
  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[href*="#"]') : null;
    if (!a) return;
    var u = new URL(a.href, location.href);
    if (u.pathname !== location.pathname || !u.hash || u.hash === location.hash) return;
    if (jumpTo(u.hash)) { history.replaceState(null, '', u.hash); e.preventDefault(); }
  });

  /* ---------- 通栏子菜单：展开时页头转白（深色首屏上也保持可读），
     同时给页面内容加黑色半透明遮罩（body.mega-open，V193）。
     V213：关闭延迟 350ms（纯 CSS :hover 移出一帧即消失，长距离移动
     误出就全关）；面板显隐改由 JS 类 .open 控制，:hover 只管链接配色 ---------- */
  var navEl = $('.nav');
  var megaT = null, megaCur = null, megaQ = null, megaIntentT = null;
  var MEGA_DELAY = 350;
  /* V258：已展开状态下换面板所需的停留时间（毫秒），见下方 mouseenter 注释 */
  var MEGA_INTENT = 180;
  function megaSet(on) {
    navEl.classList.toggle('mega-on', on);
    document.body.classList.toggle('mega-open', on);
  }
  /* V229：面板已展开时在触发项之间切换，旧/新面板都跳过过渡（瞬切）——
     各面板几何全同（同位同尺寸同白底），瞬切后视觉即「面板不动、只换内容」，
     消除收起又展开的闪动；从关闭态首次唤出仍保留淡入动画 */
  function megaQuickClear() {
    clearTimeout(megaQ);
    megaQ = setTimeout(function () {
      $$('.menu>li.mega-quick').forEach(function (el) { el.classList.remove('mega-quick'); });
    }, 100);
  }
  function megaOpen(li) {
    clearTimeout(megaT);
    if (megaCur && megaCur !== li) {
      var switching = megaCur.classList.contains('open');
      megaCur.classList.remove('open');
      if (switching) {
        megaCur.classList.add('mega-quick');
        li.classList.add('mega-quick');
        megaQuickClear();
      }
    }
    megaCur = li;
    li.classList.add('open');
    megaSet(true);
  }
  function megaCloseSoon() {
    clearTimeout(megaT);
    megaT = setTimeout(function () {
      if (megaCur) { megaCur.classList.remove('open'); megaCur = null; }
      megaSet(false);
    }, MEGA_DELAY);
  }
  $$('.menu>li.has-mega').forEach(function (li) {
    /* V258：面板已展开时，横向穿过别的标签不再立刻换面板——
       从「关于我们」斜着移向面板左侧子项时会路过中间几个标签，
       mouseenter 立即切换就会误展开左侧那个菜单。改为要求停留
       MEGA_INTENT 毫秒才允许换；穿过（<MEGA_INTENT）则忽略。
       面板未开时首开仍立即响应，不影响手感 */
    li.addEventListener('mouseenter', function () {
      clearTimeout(megaIntentT);
      clearTimeout(megaT);
      if (!megaCur || megaCur === li) { megaOpen(li); return; }
      if (!megaCur.classList.contains('open')) { megaOpen(li); return; }
      megaIntentT = setTimeout(function () { megaOpen(li); }, MEGA_INTENT);
    });
    li.addEventListener('focusin', function () { megaOpen(li); });
    li.addEventListener('focusout', function () {
      if (!li.contains(document.activeElement)) megaCloseSoon();
    });
    /* V258b：只清「待切换」定时器，不关面板（关闭交给 nav 的 mouseleave）。
       少了这一句，鼠标掠过中间标签后停在标签之间的空白处，180ms 后
       待切换定时器照样把那个标签的面板掀开 */
    li.addEventListener('mouseleave', function () { clearTimeout(megaIntentT); });
  });
  /* V258：关闭改在整条导航上判定——原先绑定在 li 上，鼠标从标签滑向面板
     途中擦过标签之间的空隙就算「离开」，350ms 后整个面板消失；现在只要还在
     导航条或面板（面板是 li 后代，几何在导航外也不触发离开）里就保持 */
  if (navEl) navEl.addEventListener('mouseleave', function () {
    clearTimeout(megaIntentT);   /* 否则鼠标已离开，待切换的定时器仍会把面板掀开 */
    megaCloseSoon();
  });

  /* ---------- 汉堡 ---------- */
  var burger = $('.burger'), drawer = $('.m-drawer');
  if (burger) burger.addEventListener('click', function () {
    burger.classList.toggle('x');
    drawer.classList.toggle('open');
    document.body.style.overflow = drawer.classList.contains('open') ? 'hidden' : '';
    $$('a', drawer).forEach(function (a, i) { a.style.transitionDelay = (0.06 * i) + 's'; });
  });
  $$('a', drawer).forEach(function (a) {
    a.addEventListener('click', function () { burger.classList.remove('x'); drawer.classList.remove('open'); document.body.style.overflow = ''; });
  });

  /* ---------- 导航滚动态 & 进度条 & 回顶 ---------- */
  var nav = $('.nav'), pbar = $('.pbar'), topBtn = $('#top');
  var darkHero = document.body.classList.contains('dark-hero');
  var heroEl = $('.hero') || $('.dhero') || $('.phero');
  var navFlip = heroEl ? Math.max(heroEl.offsetHeight - nav.offsetHeight - 8, 60) : 40;
  function onScroll() {
    var y = window.scrollY;
    nav.classList.toggle('on', darkHero ? y > navFlip : y > 40);
    topBtn.classList.toggle('on', y > 600);
    var h = document.documentElement.scrollHeight - window.innerHeight;
    pbar.style.width = (h > 0 ? (y / h) * 100 : 0) + '%';
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  topBtn.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });

  /* ---------- 入场动画 ---------- */
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
  $$('.rv').forEach(function (el) { io.observe(el); });

  /* ---------- 数字滚动 ---------- */
  function count(el) {
    var target = parseFloat(el.dataset.count.replace(/,/g, ''));
    var dec = (el.dataset.count.split('.')[1] || '').length;
    var t0 = null, dur = 1800;
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / dur, 1);
      p = 1 - Math.pow(1 - p, 3);
      el.textContent = (target * p).toFixed(dec).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var cio = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { count(e.target); cio.unobserve(e.target); } });
  }, { threshold: 0.5 });
  $$('[data-count]').forEach(function (el) { cio.observe(el); });

  /* ---------- 发展历程：横向手风琴 + 自动循环轮播 ---------- */
  var histBox = $('[data-hist]');
  if (histBox) {
    var hacc = $('[data-hacc]', histBox);
    var hItems = $$('.hacc-item', hacc);
    var hProg = $('.hacc-prog i', histBox);
    var hCur = $('.hacc-count b', histBox);
    var hTotal = hItems.length;
    var hIdx = 0, hTimer = null, hPaused = false, hVisible = false;
    var H_DUR = 4000;
    var hReduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var hIsMobile = function () { return window.matchMedia('(max-width:1279px)').matches; };
    var hCanHover = function () { return window.matchMedia('(hover:hover) and (pointer:fine)').matches && !hIsMobile(); };

    function hGo(n, byUser) {
      hIdx = ((n % hTotal) + hTotal) % hTotal;
      hItems.forEach(function (it, k) {
        var on = k === hIdx;
        it.classList.toggle('on', on);
        var b = $('.hacc-btn', it);
        if (b) b.setAttribute('aria-expanded', on ? 'true' : 'false');
      });
      if (hProg) hProg.style.width = ((hIdx + 1) / hTotal * 100) + '%';
      if (hCur) hCur.textContent = ('0' + (hIdx + 1)).slice(-2);
      if (byUser) hRestart();
    }
    function hStop() { if (hTimer) { clearInterval(hTimer); hTimer = null; } }
    function hStart() {
      hStop();
      if (hReduce || hIsMobile()) return;
      hTimer = setInterval(function () {
        if (!hPaused && hVisible) hGo(hIdx + 1);
      }, H_DUR);
    }
    function hRestart() { hStart(); }

    hItems.forEach(function (it, k) {
      var b = $('.hacc-btn', it);
      if (b) b.addEventListener('click', function () { hGo(k, true); });
    });
    /* 桌面：悬停即展开。用「鼠标停稳后再取指针下的项」而不是 mouseenter——
       展开会改变格子宽度，mouseenter 在边界上会来回触发抖动；停稳采样只切一次。 */
    var hMoveT = null;
    hacc.addEventListener('mousemove', function (e) {
      if (!hCanHover()) return;
      var mx = e.clientX, my = e.clientY;
      clearTimeout(hMoveT);
      hMoveT = setTimeout(function () {
        var el = document.elementFromPoint(mx, my);
        var item = el && el.closest ? el.closest('.hacc-item') : null;
        if (!item) return;
        var k = hItems.indexOf(item);
        if (k > -1 && k !== hIdx) hGo(k, true);
      }, 110);
    });
    var hPrev = $('.hacc-ctrl .prev', histBox), hNext = $('.hacc-ctrl .next', histBox);
    if (hPrev) hPrev.addEventListener('click', function () { hGo(hIdx - 1, true); });
    if (hNext) hNext.addEventListener('click', function () { hGo(hIdx + 1, true); });

    histBox.addEventListener('mouseenter', function () { hPaused = true; });
    histBox.addEventListener('mouseleave', function () { hPaused = false; });
    histBox.addEventListener('focusin', function () { hPaused = true; });
    histBox.addEventListener('focusout', function () { hPaused = false; });
    histBox.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { hGo(hIdx + 1, true); e.preventDefault(); }
      if (e.key === 'ArrowLeft') { hGo(hIdx - 1, true); e.preventDefault(); }
    });
    document.addEventListener('visibilitychange', function () { hPaused = document.hidden; });

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        hVisible = es[0].isIntersecting;
        if (hVisible) hStart(); else hStop();
      }, { threshold: 0.2 }).observe(histBox);
    }
    hGo(0);
  }

  /* ---------- 新闻中心 tabs / 搜索 / 分页 ---------- */
  var nlApp = $('#news-app');
  if (nlApp) {
    var CATS = { 0: '全部', 3: '公司动态', 5: '党建工作', 4: '行业资讯', 17: '主题教育' };
    var state = { cat: 0, q: '', page: 1, per: 12 };
    loadScript('data/news-index.js').then(function () {
      window.__NEWS = window.NEWS_INDEX || []; render();
      var q = new URLSearchParams(location.search).get('cat');
      if (q) { state.cat = +q; render(); }
    }).catch(function () {
      nlApp.innerHTML = '<div class="empty">新闻数据加载失败，请稍后重试。</div>';
    });
    function filtered() {
      return window.__NEWS.filter(function (x) {
        return !x.external && (state.cat === 0 || x.cat_id === state.cat) &&
          (!state.q || x.title.toLowerCase().indexOf(state.q) > -1);
      });
    }
    function escHtml(s) {
      return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }
    /* 标题命中关键字用金色 mark 高亮，逐段匹配，避免破坏原文 */
    function markTitle(t) {
      if (!state.q) return escHtml(t);
      var low = String(t).toLowerCase(), q = state.q, out = '', i = 0, idx;
      while ((idx = low.indexOf(q, i)) > -1) {
        out += escHtml(t.slice(i, idx)) + '<mark class="hl">' + escHtml(t.slice(idx, idx + q.length)) + '</mark>';
        i = idx + q.length;
      }
      return out + escHtml(t.slice(i));
    }
    function render() {
      var list = filtered();
      var pages = Math.max(1, Math.ceil(list.length / state.per));
      state.page = Math.min(state.page, pages);
      var slice = list.slice((state.page - 1) * state.per, state.page * state.per);
      var h = '<div class="nfilter"><div class="ntabs">';
      Object.keys(CATS).forEach(function (k) {
        h += '<button data-cat="' + k + '" class="' + (+k === state.cat ? 'act' : '') + '">' + CATS[k] + '</button>';
      });
      h += '</div><div class="nsearch"><input id="nq" placeholder="搜索标题关键字" value="' + state.q.replace(/"/g, '&quot;') + '">'
        + '<span class="nacts"><button type="button" class="nclear" id="nqclr" aria-label="清空搜索条件" title="清空"><svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg></button>'
        + '<button type="button" id="nqbtn" aria-label="搜索"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><line x1="16.2" y1="16.2" x2="21" y2="21"/></svg></button></span></div></div>';
      h += '<div class="rows">';
      if (!slice.length) h += '<div class="empty">未找到相关新闻</div>';
      slice.forEach(function (x) {
        var href = x.external ? x.url : ('news-detail.html?id=' + x.id);
        var ext = x.external ? ' <small class="ext-mark">↗微信</small>' : '';
        var d = x.date || '';
        h += '<a class="row" href="' + href + '"' + (x.external ? ' target="_blank" rel="noopener"' : '') + '>'
          + '<span class="rmain"><span class="t">' + markTitle(x.title) + ext + '</span>'
          + '<span class="cat">' + x.cat + '</span></span>'
          + '<span class="d">' + d + '</span></a>';
      });
      h += '</div><div class="pager">';
      h += '<button data-p="prev"' + (state.page === 1 ? ' disabled' : '') + '>‹</button>';
      for (var i = 1; i <= pages; i++) {
        if (pages > 9 && i > 2 && i < pages - 1 && Math.abs(i - state.page) > 1) {
          if (i === 3) h += '<button disabled>…</button>';
          continue;
        }
        h += '<button data-p="' + i + '" class="' + (i === state.page ? 'act' : '') + '">' + i + '</button>';
      }
      h += '<button data-p="next"' + (state.page === pages ? ' disabled' : '') + '>›</button></div>';
      h += '<p class="list-count">共 ' + list.length + ' 条 · 第 ' + state.page + '/' + pages + ' 页</p>';
      nlApp.innerHTML = h;
      fitCats();

      $$('.ntabs button', nlApp).forEach(function (b) {
        b.addEventListener('click', function () { state.cat = +b.dataset.cat; state.page = 1; render(); });
      });
      var q = $('#nq');
      function resetSearch() {
        state.q = ''; state.page = 1; render();
        var n = $('#nq'); if (n) n.focus();
      }
      q.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') { state.q = q.value.trim().toLowerCase(); state.page = 1; render(); }
        else if (e.key === 'Escape') { e.preventDefault(); resetSearch(); }
      });
      $('#nqbtn').addEventListener('click', function () { state.q = q.value.trim().toLowerCase(); state.page = 1; render(); });
      $('#nqclr').addEventListener('click', resetSearch);
      $$('.pager button', nlApp).forEach(function (b) {
        b.addEventListener('click', function () {
          var v = b.dataset.p;
          if (v === 'prev') state.page--; else if (v === 'next') state.page++; else state.page = +v;
          render();
          window.scrollTo({ top: nlApp.offsetTop - 90, behavior: 'smooth' });
        });
      });
    }
    /* V192：标题+分类标签同一行；横向放不下时整枚标签隐藏（标题保持完整不截断） */
    function fitCats() {
      $$('.row', nlApp).forEach(function (r) {
        var m = $('.rmain', r), c = $('.cat', r);
        if (!m || !c) return;
        r.classList.remove('tuck');
        if (m.scrollWidth > m.clientWidth) r.classList.add('tuck');
      });
    }
    var fitT;
    window.addEventListener('resize', function () { clearTimeout(fitT); fitT = setTimeout(fitCats, 120); });
    window.addEventListener('load', fitCats);
  }

  /* ---------- 新闻详情 ---------- */
  var art = $('#art-app');
  if (art) {
    var id = new URLSearchParams(location.search).get('id');
    loadScript('data/articles/map.js').then(function () {
      var map = window.ART_MAP || {};
      if (!map[id]) { art.innerHTML = '<div class="empty">文章不存在，<a class="link-ac" href="news.html">返回新闻中心</a></div>'; art.style.opacity = 1; return; }
      return loadScript('data/articles/a' + map[id] + '.js').then(function () {
        var shard = (window.ART_SHARDS || {})['a' + map[id]] || {};
        var x = shard[id];
        if (!x) { art.innerHTML = '<div class="empty">文章不存在</div>'; art.style.opacity = 1; return; }
        var idx = window.__NEWS ? null : null;
        document.title = x.title + ' - 广西计算机有限责任公司';
        art.innerHTML =
          '<div class="art">'
          + '<div class="crumb art-crumb"><a href="index.html">首页</a> / <a href="news.html">新闻中心</a> / <a href="news.html?cat=' + x.cat_id + '">' + x.cat + '</a></div>'
          + '<div class="art-head"><h1>' + x.title + '</h1>'
          + '<div class="art-meta"><span class="cat">' + x.cat + '</span><span>' + x.date + '</span><span>浏览 ' + x.views + ' 次</span>'
          + (x.source ? '<span>来源：' + x.source + '</span>' : '') + '</div></div>'
          + '<div class="art-body">' + x.html + '</div>'
          + (x.source ? '<p class="art-src">（来源：' + x.source + '）</p>' : '')
          + '</div>'
          + '<div class="art-nav"><a class="pv" href="news.html"><small>← 返回列表</small><b>新闻中心</b></a>'
          + '<a class="nx" href="news.html?cat=' + x.cat_id + '"><small>更多' + x.cat + ' →</small><b>查看同类新闻</b></a></div>';
        art.style.opacity = 1;
      });
    }).catch(function () {
      art.innerHTML = '<div class="empty">文章数据加载失败，<a class="link-ac" href="news.html">返回新闻中心</a></div>';
      art.style.opacity = 1;
    });
    art.style.opacity = 0; art.style.transition = 'opacity .5s';
  }

  /* ---------- 页内标签：关于我们（5 项） ---------- */
  var at = $('.atabs, .bztabs');
  if (at) {
    var tabs = $$('button', at);
    function show(key) {
      tabs.forEach(function (b) { b.classList.toggle('act', b.dataset.t === key); });
      $$('.apane').forEach(function (p) { p.classList.toggle('act', p.id === 'pane-' + key); });
    }
    function paneKey(el) {
      return el && el.classList.contains('apane') ? el.id.replace('pane-', '') : '';
    }
    function tabTop() {
      return at.getBoundingClientRect().top + window.pageYOffset - 92;
    }
    tabs.forEach(function (b) {
      b.addEventListener('click', function () {
        show(b.dataset.t);
        history.replaceState(null, '', '?s=' + b.dataset.t);
        if (window.pageYOffset > tabTop()) window.scrollTo({ top: tabTop(), behavior: 'smooth' });
      });
    });
    /* 内文里的跨面板按钮：切标签而不是刷新页面 */
    $$('[data-tab]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        show(a.dataset.tab);
        history.replaceState(null, '', '?s=' + a.dataset.tab);
        window.scrollTo({ top: tabTop(), behavior: 'smooth' });
      });
    });
    /* 同页跨面板锚点：先切到目标所在面板，再即时定位 */
    document.addEventListener('click', function (e) {
      var a = e.target.closest ? e.target.closest('a[href*="#"]') : null;
      if (!a) return;
      var u = new URL(a.href, location.href);
      if (u.pathname !== location.pathname || !u.hash) return;
      var el = null;
      try { el = document.querySelector(u.hash); } catch (err) { return; }
      var pane = el && el.closest('.apane');
      var k = paneKey(pane);
      if (!k || pane.classList.contains('act')) return;
      show(k);
      e.preventDefault();
      history.replaceState(null, '', '?s=' + k + u.hash);
      requestAnimationFrame(function () { settleTo(u.hash); });
    }, true);
    /* 初始面板：?s= 优先，其次按地址锚点落在哪个面板 */
    var s = new URLSearchParams(location.search).get('s');
    var h0 = location.hash.split('?')[0];
    if (h0.length > 1) {
      var he = null;
      try { he = document.querySelector(h0); } catch (err) { he = null; }
      var hk = paneKey(he && he.closest('.apane'));
      if (hk) s = hk;
    }
    if (s && document.getElementById('pane-' + s)) show(s);
  }
})();
