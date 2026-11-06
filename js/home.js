/* ============================================================
   首页脚本：新闻中心（左固定头条 + 右列标签/列表 + 下方 3 卡）+ 合作伙伴滚动
   ============================================================ */
(function () {
  'use strict';

  /* 与新闻页 site.js 的 CATS 口径一致（按 cat_id 过滤）
     V352：党建工作已回到新闻中心当一个标签，但首页这块只做「公司动态 / 行业资讯」
     的摘要位，仍然不收党建(5)与主题教育(17) —— 要看党建走新闻中心的标签 */
  var CATS = { 0: '全部', 3: '公司动态', 4: '行业资讯' };
  var PARTY_CATS = { 5: 1, 17: 1 };
  var DEFAULT_COVER = 'assets/img/_img_index_news-header-bg.png?v=96';
  var LIST_MAX = 5; /* 右侧列表总条数（含带摘要的首条）；V144 由 6 收到 5，压新闻区高度 */

  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
  }
  function hrefOf(x) { return x.external ? x.url : ('news-detail.html?id=' + x.id); }
  function attrOf(x) { return x.external ? ' target="_blank" rel="noopener"' : ''; }
  function dateParts(d) {
    var p = (d || '').split('-');
    return { y: p[0] || '', m: p[1] || '', d: p[2] || '' };
  }

  var tabsEl = document.getElementById('home-news-tabs');
  var gridEl = document.getElementById('home-news');
  var listEl = document.getElementById('hn-list');

  if (gridEl && listEl) {
    var dataAll = [];

    /* ---------- V340 左侧焦点新闻：3 张淡入淡出轮播 ----------
       取新闻数据里按日期倒序的前 3 条带封面稿件（与右列同一数据源，不新增内容）。
       自动 5.2s 切换；鼠标悬停、键盘聚焦、标签页隐藏时暂停；点圆点立即切换；
       prefers-reduced-motion 下不自动播，仍可手动点。 */
    var FEAT_MAX = 3;
    var FEAT_DUR = 5200;
    var featBox = document.getElementById('hn-feat');
    var slidesEl = document.getElementById('hn-feat-slides');
    var dotsEl = document.getElementById('hn-feat-dots');
    var featSlides = [], featDots = [], featIdx = 0, featTimer = null;
    var featReduce = window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var attrEsc = function (s) {
      return esc(s).replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    };

    var featGo = function (n) {
      if (!featSlides.length) return;
      featIdx = ((n % featSlides.length) + featSlides.length) % featSlides.length;
      featSlides.forEach(function (s, i) { s.classList.toggle('on', i === featIdx); });
      featDots.forEach(function (b, i) {
        b.classList.toggle('act', i === featIdx);
        b.setAttribute('aria-selected', i === featIdx ? 'true' : 'false');
      });
    };
    var featStop = function () {
      if (featTimer) { clearInterval(featTimer); featTimer = null; }
    };
    var featPlay = function () {
      if (featTimer || featReduce || featSlides.length < 2 || document.hidden) return;
      featTimer = setInterval(function () { featGo(featIdx + 1); }, FEAT_DUR);
    };

    var buildFeature = function (list) {
      if (!slidesEl || !dotsEl || !list.length) return;
      var h = '', d = '';
      list.forEach(function (x, i) {
        var dp = dateParts(x.date);
        h += '<a class="feat-slide' + (i === 0 ? ' on' : '') + '" href="' +
          attrEsc(hrefOf(x)) + '"' + attrOf(x) + '>' +
          '<img src="' + attrEsc(x.cover || DEFAULT_COVER) + '" alt="" ' +
          'loading="eager" decoding="async">' +
          '<div class="cap"><span class="fd"><b>' + dp.d + '</b><span>' +
          dp.y + '-' + dp.m + '</span></span>' +
          '<span class="cap-txt"><b>' + esc(x.title) + '</b></span></div></a>';
        d += '<button type="button" role="tab" data-i="' + i + '" class="' +
          (i === 0 ? 'act' : '') + '" aria-selected="' + (i === 0) +
          '" aria-label="第 ' + (i + 1) + ' 条焦点新闻"></button>';
      });
      slidesEl.innerHTML = h;
      dotsEl.innerHTML = d;
      featSlides = Array.prototype.slice.call(slidesEl.children);
      featDots = Array.prototype.slice.call(dotsEl.children);

      /* 封面外链偶有失效：回退到站点自带兜底图，避免空白蓝块 */
      featSlides.forEach(function (s) {
        var im = s.querySelector('img');
        if (!im) return;
        im.addEventListener('error', function () {
          if (im.getAttribute('src') !== DEFAULT_COVER) im.setAttribute('src', DEFAULT_COVER);
        });
      });
      featDots.forEach(function (b) {
        b.addEventListener('click', function () {
          featGo(+b.getAttribute('data-i'));
          featStop(); featPlay();
        });
      });
      if (featBox) {
        featBox.addEventListener('mouseenter', featStop);
        featBox.addEventListener('mouseleave', featPlay);
        featBox.addEventListener('focusin', featStop);
        featBox.addEventListener('focusout', featPlay);
      }
      document.addEventListener('visibilitychange', function () {
        if (document.hidden) featStop(); else featPlay();
      });
      featIdx = 0; featGo(0); featPlay();
    };

    /* 右侧列表：首条带摘要 + 其余，随标签切换 */
    var renderList = function (catId) {
      var set = catId === 0
        ? dataAll
        : dataAll.filter(function (x) { return x.cat_id === catId; });

      if (!set.length) {
        listEl.innerHTML = '<li><span class="t">该栏目暂无内容。</span></li>';
        return;
      }

      var h = '';
      set.slice(0, LIST_MAX).forEach(function (x, i) {
        var href = hrefOf(x), attr = attrOf(x);
        if (i === 0) {
          var dp = dateParts(x.date);
          var sum = (x.summary || '').replace(/\s+/g, ' ').trim();
          if (sum.length > 96) sum = sum.slice(0, 96) + '…';
          h += '<li class="lead"><a href="' + href + '"' + attr + '>' +
            '<span class="lmain">' +
              '<span class="t">' + esc(x.title) + '</span>' +
              /* 摘要节点恒定存在（无摘要时留空占位），保证首条高度不随稿件变化 */
              '<span class="sum">' + esc(sum) + '</span>' +
            '</span>' +
            '<span class="fd"><b>' + dp.d + '</b><span>' + dp.y + '-' + dp.m + '</span><i>→</i></span>' +
            '</a></li>';
        } else {
          h += '<li><a href="' + href + '"' + attr + '>' +
            '<span class="t">' + esc(x.title) + '</span>' +
            '<span class="d">' + x.date + '</span></a></li>';
        }
      });
      listEl.innerHTML = h;
    };

    /* 直接复用新闻页 .ntabs 的按钮结构与口径 */
    var buildTabs = function () {
      Object.keys(CATS).forEach(function (k) {
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.setAttribute('data-cat', k);
        btn.className = (+k === 0 ? 'act' : '');
        btn.textContent = CATS[k];
        btn.addEventListener('click', function () {
          Array.prototype.forEach.call(tabsEl.children, function (b) { b.classList.remove('act'); });
          btn.classList.add('act');
          renderList(+k);
        });
        tabsEl.appendChild(btn);
      });
    };

    /* V351：新闻索引 209KB（gzip 后 54KB）原来随首屏一起拉，但新闻板块在第 3 屏。
       改成进入视口前 600px 才加载，首屏少一个请求、也少一次 200KB JSON 解析；
       不支持 IntersectionObserver 的内核仍按原逻辑立即加载。 */
    var loadNews = function () {
      window.__loadNews()
        .then(function () {
          dataAll = (window.NEWS_INDEX || []).filter(function (x) {
            return !x.external && !PARTY_CATS[x.cat_id];
          });
          if (!dataAll.length) {
            listEl.innerHTML = '<li><span class="t">新闻数据加载失败，请稍后重试。</span></li>';
            return;
          }
          /* 封面优先取站点自有图源：微信 mmbiz.qpic.cn 的封面常是 140px 缩略图或
             防盗链占位，轮到时会糊掉；不足 3 张再按原顺序补其它来源。 */
          var covers = dataAll.filter(function (x) { return x.cover; });
          var own = covers.filter(function (x) { return x.cover.indexOf('www.gxci.com.cn/') >= 0; });
          var other = covers.filter(function (x) { return x.cover.indexOf('www.gxci.com.cn/') < 0; });
          buildFeature(own.concat(other).slice(0, FEAT_MAX));
          buildTabs();
          renderList(0);
        })
        .catch(function () {
          listEl.innerHTML = '<li><span class="t">新闻数据加载失败，请稍后重试。</span></li>';
        });
    };

    var secNews = document.querySelector('.sec-news');
    if (secNews && window.IntersectionObserver) {
      var newsIO = new IntersectionObserver(function (es) {
        for (var i = 0; i < es.length; i++) {
          if (es[i].isIntersecting) { newsIO.disconnect(); loadNews(); break; }
        }
      }, { rootMargin: '600px 0px' });
      newsIO.observe(secNews);
    } else {
      loadNews();
    }
  }

  /* ---------- 合作伙伴：双行反向无缝滚动 ---------- */
  var mq1 = document.getElementById('mq1');
  var mq2 = document.getElementById('mq2');
  if (mq1 && mq2) {
    /* V338：新增 7 家（安恒信息 / 承章科技 / 泛微 / 浪潮 / 深信服 / H3C / 360）。
       华为（hw）原已在列，不重复添加；「广西一禾」V324 已删。
       新 Logo 分散插入，避免全挤在队尾；两行按总数自动均分（31 → 16 + 15）。 */
    var names = ['hg', 'ah', 'bjdx', 'bbwcqjy', 'czkj', 'ejy', 'kd', 'fw',
      'zy', 'ca', 'lc', 'hw', 'gdlz', 'sxf', 'szsm', 'nd',
      'ld', 'h3c', 'dx', 'hsdz', '360', 'jsy', 'wps', 'tj',
      'liyade', 'maxhub', 'hk', 'dj', 'aqg', 'qm', 'yt'];

    function row(el, list) {
      var h = '';
      list.forEach(function (n) {
        /* V351：PNG 转 WebP（306KB → 110KB），并加 lazy —— 合作屏在第 5 屏，
           原来冷启动就一次性拉完 31 张（约 250KB / 31 个请求），拖慢首屏。 */
        h += '<span class="mq-item"><img src="assets/img/hzhb_' + n + '.webp?v=351" alt="" loading="lazy" decoding="async"></span>';
      });
      el.innerHTML = h + h; /* 复制一份以实现无缝滚动 */
    }

    var half = Math.ceil(names.length / 2);
    row(mq1, names.slice(0, half));
    row(mq2, names.slice(half));

    /* V341：两列滚动动画改为「进入视口才启动」。原来动画随页面加载就跑，
       用户滚到合作屏时第一列已左移数百像素、开头 Logo 被移出，看着像没在动。
       进出视口用同一个观察器切换 .run，离开即暂停，不白耗性能。 */
    var mqBoxes = [].slice.call(document.querySelectorAll('.mq'));
    if (window.IntersectionObserver && mqBoxes.length) {
      var mqIO = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          e.target.classList.toggle('run', e.isIntersecting);
        });
      }, { threshold: 0.2 });
      mqBoxes.forEach(function (m) { mqIO.observe(m); });
    } else {
      mqBoxes.forEach(function (m) { m.classList.add('run'); });
    }
  }

})();
