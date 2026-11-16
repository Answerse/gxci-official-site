/* ============================================================
   首页脚本：新闻中心（V403 回到两栏：左焦点图 / 右三个标签栏）
     焦点图**保留 V401 新样式**：图在上、标题单独一行（不覆盖图上、无背景、黑字），
     标题下三条横条指示器按剩余停留时间递减；3 张轮播、横版优先，
     首张固定为真实稿件「成立四十周年发展座谈会」（V404 用户点名）。
     右列 = 站内原来的 .news-tabs 三个可切换标签（公司动态/行业资讯/党建工作）
     + 统一「标题 + 日期 + 细线」列表（V401 用户点定，首条不再带摘要）。
   + 合作伙伴滚动
   ============================================================ */
(function () {
  'use strict';

  var CATS = { 3: '公司动态', 4: '行业资讯', 5: '党建工作' };
  var DEFAULT_CAT = 3;   /* 默认高亮第一个标签，与新闻中心页口径一致 */
  var DEFAULT_COVER = 'assets/img/_img_index_news-header-bg.png?v=96';
  var LIST_MAX = 6;      /* V407：右列列表补到 6 条，与左侧焦点图列高度视觉对齐 */
  var FEAT_MAX = 3;      /* 焦点轮播固定 3 张 */
  var FEAT_DUR = 5200;   /* 每张停留 5.2s */
  /* V404：用户点名「默认要 40 周年座谈会」。这是真实稿件，不是编的 —— 标题、
     日期、链接来自 2026-10-23「北部湾产权交易所集团」公众号原文，封面取自同篇
     座谈会现场照（大屏写明「成立40周年发展座谈会」），已本地化并去掉公众号水印。
     正式域名下新闻索引优先读云数据库（js/cloud-news.js 会覆盖 window.NEWS_INDEX），
     只往 data/news-index.js 里加一条线上不会生效，所以首张在这里固定。 */
  var FEAT_FIRST = {
    title: '【国企四十载 奋进新征程】广西计算机公司召开成立四十周年发展座谈会',
    date: '2026-10-23',
    external: true,
    url: 'https://mp.weixin.qq.com/s?__biz=MzI5MDYxNjY0Mw==&mid=2247487079&idx=1&sn=0e7f2a4e48b5cf79acf4a6c7537c96ff&chksm=edd480c0ad2d873a25d9623037a7757d68ebfda7751e8aa18650b055f5e04d0867e68fbcb297',
    cover: 'assets/img/news/topic/20261023/40th-forum.webp?v=404'
  };

  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
  }
  function attrEsc(s) {
    return esc(s).replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }
  function hrefOf(x) { return x.external ? x.url : ('news-detail.html?id=' + x.id); }
  function attrOf(x) { return x.external ? ' target="_blank" rel="noopener"' : ''; }

  var gridEl = document.getElementById('home-news');
  var tabsEl = document.getElementById('home-news-tabs');
  var listEl = document.getElementById('hn-list');
  var moreEl = document.querySelector('.news-bar .smore');

  if (gridEl && tabsEl && listEl) {
    var dataAll = [];
    var featBox = document.getElementById('hn-feat');
    var slidesEl = document.getElementById('hn-feat-slides');
    var dotsEl = document.getElementById('hn-feat-dots');
    var titleEl = document.getElementById('hn-feat-title');
    var featItems = [], featSlides = [], featDots = [], featIdx = 0;
    var featReduce = window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    /* 剩余停留时间：rAF 驱动，暂停（hover / 聚焦 / 切后台）时进度条停住 */
    var rafId = null, remain = FEAT_DUR, lastTs = 0, paused = true;

    var setFill = function (pct) {
      featDots.forEach(function (b, i) {
        var f = b.querySelector('.fill');
        if (f) f.style.width = (i === featIdx ? Math.max(0, Math.min(100, pct)) : 0) + '%';
      });
    };

    var featGo = function (n) {
      if (!featSlides.length) return;
      featIdx = ((n % featSlides.length) + featSlides.length) % featSlides.length;
      featSlides.forEach(function (s, i) { s.classList.toggle('on', i === featIdx); });
      featDots.forEach(function (b, i) {
        b.classList.toggle('act', i === featIdx);
        b.setAttribute('aria-selected', i === featIdx ? 'true' : 'false');
      });
      var x = featItems[featIdx];
      if (x && titleEl) {
        titleEl.textContent = x.title;
        titleEl.setAttribute('href', hrefOf(x));
        if (x.external) titleEl.setAttribute('target', '_blank');
        else titleEl.removeAttribute('target');
      }
      remain = FEAT_DUR; lastTs = 0; setFill(100);
    };

    var tick = function (ts) {
      if (paused) return;
      if (!lastTs) lastTs = ts;
      remain -= (ts - lastTs);
      lastTs = ts;
      if (remain <= 0) featGo(featIdx + 1);
      else setFill(remain / FEAT_DUR * 100);
      rafId = window.requestAnimationFrame(tick);
    };
    var featPlay = function () {
      if (featReduce || document.hidden || featSlides.length < 2) return;
      if (!paused && rafId) return;
      paused = false; lastTs = 0;
      rafId = window.requestAnimationFrame(tick);
    };
    var featStop = function () {
      paused = true;
      if (rafId) { window.cancelAnimationFrame(rafId); rafId = null; }
    };

    var buildFeature = function (list) {
      if (!slidesEl || !dotsEl || !titleEl || !list.length) return;
      featItems = list.slice(0, FEAT_MAX);
      var h = '', d = '';
      featItems.forEach(function (x, i) {
        h += '<a class="feat-slide' + (i === 0 ? ' on' : '') + '" href="' +
          attrEsc(hrefOf(x)) + '"' + attrOf(x) + ' aria-label="' + attrEsc(x.title) + '">' +
          '<img src="' + attrEsc(x.cover || DEFAULT_COVER) + '" alt="" ' +
          'loading="eager" decoding="async"></a>';
        d += '<button type="button" role="tab" data-i="' + i + '" class="' +
          (i === 0 ? 'act' : '') + '" aria-selected="' + (i === 0 ? 'true' : 'false') +
          '" aria-label="第 ' + (i + 1) + ' 条焦点新闻"><span class="fill"></span></button>';
      });
      slidesEl.innerHTML = h;
      dotsEl.innerHTML = d;
      featSlides = Array.prototype.slice.call(slidesEl.children);
      featDots = Array.prototype.slice.call(dotsEl.children);

      /* 封面外链偶有失效：回退到站点自带兜底图，避免空白 */
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

    /* 右列：「更多新闻 →」跟着当前标签走，点进去落在新闻中心的同一分类 */
    var syncMore = function (catId) {
      if (!moreEl) return;
      moreEl.setAttribute('href', catId === DEFAULT_CAT ? 'news.html' : 'news.html?cat=' + catId);
    };

    /* 统一列表：标题左 + 日期右 + 细线，无摘要、无首条展开（V401 用户点定） */
    var renderList = function (catId) {
      syncMore(catId);
      var set = dataAll.filter(function (x) { return x.cat_id === catId; });
      if (!set.length) {
        listEl.innerHTML = '<li><a><span class="t">该栏目暂无内容。</span><span class="d"></span></a></li>';
        return;
      }
      var h = '';
      set.slice(0, LIST_MAX).forEach(function (x) {
        h += '<li><a href="' + attrEsc(hrefOf(x)) + '"' + attrOf(x) + '>' +
          '<span class="t">' + esc(x.title) + '</span>' +
          '<span class="d">' + esc(x.date) + '</span></a></li>';
      });
      listEl.innerHTML = h;
    };

    /* 站内原来的三个标签：默认高亮第一个，点击切换右列列表 */
    var buildTabs = function () {
      Object.keys(CATS).forEach(function (k, i) {
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.setAttribute('data-cat', k);
        btn.className = (i === 0 ? 'act' : '');
        btn.textContent = CATS[k];
        btn.addEventListener('click', function () {
          Array.prototype.forEach.call(tabsEl.children, function (b) { b.classList.remove('act'); });
          btn.classList.add('act');
          renderList(+k);
        });
        tabsEl.appendChild(btn);
      });
    };

    /* 焦点图取图：首张固定 FEAT_FIRST（40 周年座谈会）；其余优先横版照片封面。
       新闻库里不少封面是 1260×2161 的整页文章截图，铺进 16/10 焦点框会变成一屏正文，
       所以预探测宽高比 >= 1.15 的横版图优先，竖版长截图退后；3.2s 超时按已探明结果渲染。
       V403：外链封面常比 3.2s 慢，超时时先扫一次 Image.complete（onload 可能没触发），
       仍一张都没探明则延后 2.2s 再判，避免「横版优先」退化成按原顺序、首张变成长截图。 */
    var pickFeature = function (list, cb) {
      /* 首张固定为 40 周年座谈会；若数据源里也同步了同一篇，剔除避免重复轮播 */
      var rest = list.filter(function (x) {
        return x.cover && x.url !== FEAT_FIRST.url && x.title !== FEAT_FIRST.title;
      });
      /* 站点自有图优先（微信封面常是缩略图 / 防盗链占位） */
      var own = rest.filter(function (x) { return x.cover && x.cover.indexOf('www.gxci.com.cn/') >= 0; });
      var other = rest.filter(function (x) { return x.cover && x.cover.indexOf('www.gxci.com.cn/') < 0; });
      var cand = own.concat(other).slice(0, 8);
      var meta = [], imgs = [], left = cand.length, done = false, retried = false, timer = null;

      var probe = function (k) {
        if (meta[k]) return meta[k];
        var im = imgs[k];
        if (im && im.complete && im.naturalWidth > 0) {
          meta[k] = { x: cand[k], r: im.naturalWidth / Math.max(1, im.naturalHeight) };
        }
        return meta[k];
      };
      var finish = function () {
        if (done) return;
        var known = 0;
        for (var q = 0; q < cand.length; q++) if (probe(q)) known++;
        if (!known && !retried && cand.length) {
          retried = true;
          timer = window.setTimeout(finish, 2200);
          return;
        }
        done = true;
        window.clearTimeout(timer);
        /* 稀疏数组不能用 forEach（会跳过未探明的洞），这里显式按索引遍历 */
        var wide = [], slight = [], long = [];
        for (var k = 0; k < cand.length; k++) {
          var m = probe(k);
          if (!m) continue;
          if (m.r >= 1.15) wide.push(m.x);
          else if (m.r >= 0.75) slight.push(m.x);
          else long.push(m.x);
        }
        var seq = [FEAT_FIRST];
        var add = function (x) {
          if (seq.length < FEAT_MAX && x && seq.indexOf(x) < 0) seq.push(x);
        };
        wide.concat(slight, long).forEach(add);
        /* 超时未探明的按原顺序补足，保证恒为 3 张 */
        for (var k2 = 0; k2 < cand.length && seq.length < FEAT_MAX; k2++) add(cand[k2]);
        cb(seq.length ? seq : cand.slice(0, FEAT_MAX));
      };
      timer = window.setTimeout(finish, 3200);
      if (!cand.length) { finish(); return; }
      cand.forEach(function (x, i) {
        var im = new Image();
        imgs[i] = im;
        var put = function (r) {
          meta[i] = { x: x, r: r };
          if (--left === 0) finish();
        };
        im.onload = function () { put(im.naturalWidth / Math.max(1, im.naturalHeight)); };
        im.onerror = function () { put(0); };
        im.src = x.cover;
      });
    };

    /* V351：新闻索引 209KB 原随首屏一起拉，但新闻板块在第 3 屏；
       改成进入视口前 600px 才加载。不支持 IntersectionObserver 的内核立即加载。 */
    var loadNews = function () {
      window.__loadNews()
        .then(function () {
          dataAll = (window.NEWS_INDEX || []).filter(function (x) { return CATS[x.cat_id]; });
          if (!dataAll.length) {
            listEl.innerHTML = '<li><a><span class="t">新闻数据加载失败，请稍后重试。</span><span class="d"></span></a></li>';
            return;
          }
          buildTabs();
          renderList(DEFAULT_CAT);
          pickFeature(dataAll.filter(function (x) { return x.cover; }), buildFeature);
        })
        .catch(function () {
          listEl.innerHTML = '<li><a><span class="t">新闻数据加载失败，请稍后重试。</span><span class="d"></span></a></li>';
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
       V353 用户按截图划线删掉 17 家，剩 14 家（两行各 7）：
         北京大学 · e交易 · 科大讯飞 · 卓优 · 国盾量子 · 神州数码 · 南大尚诚 ·
         趣链科技 · 恒生电子 · 太极 · 利亚德 · MAXHUB · 海康威视 · 顶佳 ·
         安全狗 · 启明星辰 · 英拓网络
       顺序保持原图编号顺序。 */
    var names = ['hg', 'ah', 'bbwcqjy', 'czkj', 'fw', 'ca', 'lc',
      'hw', 'sxf', 'h3c', 'dx', '360', 'jsy', 'wps'];

    /* V353：只剩 7 项时一行宽度（7×208≈1456）在 1920 宽的容器里不够，
       无缝滚动会从右侧露出空白。按容器宽度动态复制整数份，保证「半幅」始终盖满，
       并按固定速度折算时长，条数变化后观感速度不变（原来 16 项 / 56s ≈ 59px/s）。 */
    var UNIT = 208;    /* .mq-item 190 + .mq-track gap 18 */
    var SPEED = 59;    /* px/s */
    function row(el, list) {
      var unitW = list.length * UNIT;
      var boxW = (el.parentNode && el.parentNode.clientWidth) || window.innerWidth;
      var reps = Math.max(2, 2 * Math.ceil(boxW / unitW));
      var h = '';
      list.forEach(function (n) {
        /* V351：PNG 转 WebP（306KB → 110KB），并加 lazy —— 合作屏在第 5 屏，
           原来冷启动就一次性拉完（约 250KB / 31 个请求），拖慢首屏。 */
        h += '<span class="mq-item"><img src="assets/img/hzhb_' + n + '.webp?v=353" alt="" loading="lazy" decoding="async"></span>';
      });
      var all = '';
      for (var i = 0; i < reps; i++) all += h;   /* 整数份，-50% 位移仍落在整份边界上 */
      el.innerHTML = all;
      el.style.animationDuration = ((unitW * reps / 2) / SPEED).toFixed(1) + 's';
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
