/* ============================================================
   云服务数据源（V293）：新闻列表与正文改从云数据库读取
   - 只在正式域名下启用（publishableKey 有 Origin 校验，本地/预览必然失败）
   - SDK 按需加载，非正式域名一个字节都不拉
   - 任何一步失败（网络、超时、空结果）都 reject，由调用方回落到本地 data/*.js
   ============================================================ */
(function () {
  'use strict';

  var CFG = {
    endpoint: 'https://gxci-official-site.app.workbuddy.host',
    publishableKey: 'wbpk_8d30cwMwEXstyDsA06jT67_sLi2oIF07HRrrMRrQ8n6mOKuB9Dj28hV'
  };
  var LIVE_HOST = 'gxci-official-site.app.workbuddy.host';
  var SDK_SRC = 'js/vendor/workbuddy-cloud-sdk.js';
  /* V293：SDK 自托管。jsDelivr 在境内不稳，且正式站要求首屏不依赖第三方域名 */
  var TIMEOUT = 8000;

  var db = null;
  var sdkPromise = null;

  function isLive() {
    return location.hostname === LIVE_HOST;
  }

  function loadSdk() {
    if (window.WorkBuddyCloud) return Promise.resolve();
    if (!sdkPromise) {
      sdkPromise = new Promise(function (resolve, reject) {
        var s = document.createElement('script');
        s.src = SDK_SRC;
        s.async = true;
        s.onload = function () { resolve(); };
        s.onerror = function () { sdkPromise = null; reject(new Error('sdk load failed')); };
        document.head.appendChild(s);
      });
    }
    return sdkPromise;
  }

  function guard(p) {
    return new Promise(function (resolve, reject) {
      var t = setTimeout(function () { reject(new Error('cloud timeout')); }, TIMEOUT);
      p.then(function (v) { clearTimeout(t); resolve(v); },
             function (e) { clearTimeout(t); reject(e); });
    });
  }

  function getDb() {
    if (!isLive()) return Promise.reject(new Error('not live origin'));
    if (db) return Promise.resolve(db);
    return loadSdk().then(function () {
      db = window.WorkBuddyCloud.createWorkBuddyCloud({
        endpoint: CFG.endpoint,
        publishableKey: CFG.publishableKey
      }).database;
      return db;
    });
  }

  var INDEX_COLS = 'id,cat_id,cat,title,date,summary,cover,views,external,url';

  window.WBNews = {
    /* 列表：字段口径与 data/news-index.js 一致，调用方可直接替换 window.NEWS_INDEX */
    index: function () {
      return guard(getDb().then(function (d) {
        return d.from('news_articles').select(INDEX_COLS)
          .order('date', { ascending: false }).limit(500);
      }).then(function (res) {
        if (res.error) throw new Error(res.error.message);
        var rows = res.data || [];
        if (!rows.length) throw new Error('empty');
        return rows;
      }));
    },
    /* 正文：命不中或没有正文都 reject，回落到本地分片 */
    article: function (id) {
      if (!id) return Promise.reject(new Error('no id'));
      return guard(getDb().then(function (d) {
        return d.from('news_articles')
          .select('id,cat_id,cat,title,date,views,images,html,source,cover')
          .eq('id', id).maybeSingle();
      }).then(function (res) {
        if (res.error) throw new Error(res.error.message);
        if (!res.data || !res.data.html) throw new Error('not found');
        return res.data;
      }));
    }
  };
})();
