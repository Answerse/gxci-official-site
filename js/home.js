/* ============================================================
   首页脚本：新闻中心（左固定头条 + 右列标签/列表 + 下方 3 卡）+ 合作伙伴滚动
   ============================================================ */
(function () {
  'use strict';

  /* 与新闻页 site.js 的 CATS 口径一致（按 cat_id 过滤） */
  var CATS = { 0: '全部', 3: '公司动态', 5: '党建工作', 4: '行业资讯', 17: '主题教育' };
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
    var featured = null;

    /* 左侧头条：一次性填充，之后不随标签变化 */
    var fillFeature = function (x) {
      if (!x) return;
      var fimg = document.getElementById('hn-feat-img');
      var ft = document.getElementById('hn-feat-title');
      var fd = document.getElementById('hn-feat-day');
      var fy = document.getElementById('hn-feat-ym');
      var fa = document.getElementById('hn-feat');
      if (fimg) fimg.src = x.cover || DEFAULT_COVER;
      if (ft) ft.textContent = x.title;
      var dp = dateParts(x.date);
      if (fd) fd.textContent = dp.d || '';
      if (fy) fy.textContent = dp.y + '-' + dp.m;
      if (fa) {
        fa.href = hrefOf(x);
        if (x.external) { fa.target = '_blank'; fa.rel = 'noopener'; }
        else { fa.removeAttribute('target'); fa.removeAttribute('rel'); }
      }
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

    window.__loadData('data/news-index.js')
      .then(function () {
        dataAll = (window.NEWS_INDEX || []).filter(function (x) { return !x.external; });
        if (!dataAll.length) {
          listEl.innerHTML = '<li><span class="t">新闻数据加载失败，请稍后重试。</span></li>';
          return;
        }
        featured = dataAll.find(function (x) { return x.cover; }) || dataAll[0];
        fillFeature(featured);
        buildTabs();
        renderList(0);
      })
      .catch(function () {
        listEl.innerHTML = '<li><span class="t">新闻数据加载失败，请稍后重试。</span></li>';
      });
  }

  /* ---------- 合作伙伴：双行反向无缝滚动 ---------- */
  var mq1 = document.getElementById('mq1');
  var mq2 = document.getElementById('mq2');
  if (mq1 && mq2) {
    var names = ['hg', 'bjdx', 'bbwcqjy', 'ejy', 'yh', 'kd', 'zy', 'ca', 'hw', 'gdlz',
      'szsm', 'nd', 'ld', 'dx', 'hsdz', 'jsy', 'wps', 'tj', 'liyade', 'maxhub',
      'hk', 'dj', 'aqg', 'qm', 'yt'];

    function row(el, list) {
      var h = '';
      list.forEach(function (n) {
        h += '<span class="mq-item"><img src="assets/img/hzhb_' + n + '.png?v=75" alt=""></span>';
      });
      el.innerHTML = h + h; /* 复制一份以实现无缝滚动 */
    }

    row(mq1, names.slice(0, 13));
    row(mq2, names.slice(13));
  }
})();
