/* 首页整屏滚动（V293）
   用户指令：一次滚一屏，页面边缘有指示器。
   实现要点：
   1) 只接管桌面精确指针（>=900px 且 pointer:fine）；触屏保持原生滚动，指示器也不显示——
      手机上业务区一段就有 3000px 高，强行整屏翻会翻不动。
   2) 不做 CSS scroll-snap：业务区 1064px > 一屏 900px，mandatory snap 会把下半截锁死。
      这里自己算「停靠点」：每个区块的顶部；高于一屏的区块再补一个底部对齐点，
      保证 1064 高那块也能看全。
   3) 滚轮一次手势只走一格，动画 720ms，动画期间与结束后 320ms 内的滚轮全部吞掉，
      避免触控板惯性把一次滑动翻成两三屏。
   4) 右侧竖排圆点，点击跳转，悬停出名称；深色区块（首屏 / 发展历程）自动反白。 */
(function () {
  'use strict';

  var mq = window.matchMedia('(min-width:900px) and (pointer:fine)');
  var secs = [], labels = [], stops = [], rail = null, dots = [];
  var lock = false, acc = 0, lastWheel = 0, lockAt = 0, consumed = false, ticking = false;
  /* V296：DUR 动画时长，COOL 落位后的死区，IDLE 判定「同一次滑动」的静默阈值。
     阈值放宽到 260ms 是因为触控板惯性可以拖一秒多，原来 200ms 会把它当成新手势 ——
     一次用力滑就翻两屏。宁可第二次拨慢半拍，也不让它自己往下窜。 */
  var DUR = 680, MERGE = 90, COOL = 180, IDLE = 260, TH = 24;

  function y0(el) { return Math.round(el.getBoundingClientRect().top + window.pageYOffset); }
  function vh() { return window.innerHeight; }
  function maxY() { return Math.max(0, document.documentElement.scrollHeight - vh()); }

  /* V299：页脚自然高度实测后写进 --footh（CSS 用它算合作区高度 = 100vh − 页脚高）。
     页脚高度随宽度和内容换行变，写死数值在大屏/窄屏会错位，所以每次 resize/load 都重量一次。 */
  function setFootH() {
    var f = document.querySelector('footer');
    if (!f) return;
    document.body.style.setProperty('--footh', Math.round(f.offsetHeight) + 'px');
  }

  /* ---------- 停靠点 ---------- */
  function buildStops() {
    var v = vh(), max = maxY(), ys = [];
    secs.forEach(function (el) {
      var top = y0(el), h = el.offsetHeight;
      ys.push(top);
      if (h > v + 40) {
        for (var k = 1; k * (v - 60) < h - v; k++) ys.push(top + k * (v - 60));
        ys.push(top + h - v);
      }
    });
    /* V299：最后一屏顶对齐 —— 合作区顶对齐、页脚在它下面并允许露出屏幕外。
       所以不再补「贴底」停靠点：页脚本来就比剩下的空间高，为了让页脚底进屏幕
       就会把合作区往上顶、标题被页头压住 —— 那正是上一版的问题。
       合作区自己超过一屏时，上面的循环已经给了中间点和贴底点，不会漏内容。 */
    ys = ys.filter(function (y) { return y >= 0 && y <= max + 1; })
           .sort(function (a, b) { return a - b; });
    stops = [];
    ys.forEach(function (y) {
      if (!stops.length) stops.push(y);
      else if (y - stops[stops.length - 1] > MERGE) stops.push(y);
      else stops[stops.length - 1] = y;   /* 太近就取更靠下的那个，末屏才能贴底 */
    });
  }

  function nearest() {
    var y = window.pageYOffset, best = 0, d = Infinity;
    for (var i = 0; i < stops.length; i++) {
      var dd = Math.abs(stops[i] - y);
      if (dd < d) { d = dd; best = i; }
    }
    return best;
  }

  /* ---------- 动画 ---------- */
  function ease(p) { return p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2; }

  function jump(to) {
    if (lock) return;
    var from = window.pageYOffset;
    to = Math.max(0, Math.min(maxY(), Math.round(to)));
    if (Math.abs(to - from) < 2) return;
    lock = true;
    var t0 = performance.now();
    (function step(now) {
      var p = Math.min(1, (now - t0) / DUR);
      window.scrollTo(0, from + (to - from) * ease(p));
      if (p < 1) requestAnimationFrame(step);
      else { lock = false; lockAt = performance.now(); sync(); }
    })(t0);
  }

  function step(dir) {
    if (lock) return;
    var y = window.pageYOffset, i = nearest();
    /* 当前不在停靠点上（拖了滚动条、或动画被打断）：先吸附回最近一屏，不叠加方向 ——
       否则「位置偏了 + 方向」会一次跳过一整屏。 */
    if (Math.abs(stops[i] - y) > 140) return jump(stops[i]);
    i = Math.max(0, Math.min(stops.length - 1, i + dir));
    jump(stops[i]);
  }

  /* ---------- 指示器 ---------- */
  function isDark(el) {
    if (!el) return false;
    if (el.matches('header.hero, .hero, .hist, .dark, .sec.dark')) return true;
    var bg = getComputedStyle(el).backgroundColor || '';
    var m = bg.match(/[\d.]+/g);
    if (!m || m.length < 3) return false;
    var a = m.length > 3 ? parseFloat(m[3]) : 1;
    if (a < 0.5) return false;
    return (0.299 * m[0] + 0.587 * m[1] + 0.114 * m[2]) / 255 < 0.45;
  }

  function active() {
    var y = window.pageYOffset + vh() * 0.32, k = 0;
    secs.forEach(function (el, i) { if (y0(el) <= y) k = i; });
    return k;
  }

  function sync() {
    if (!rail) return;
    var k = active();
    dots.forEach(function (d, i) { d.classList.toggle('act', i === k); });
    rail.classList.toggle('on-dark', isDark(secs[k]));
  }

  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () { ticking = false; sync(); });
  }

  function buildRail() {
    rail = document.createElement('nav');
    rail.className = 'pg-rail';
    rail.setAttribute('aria-label', '页面导航');
    secs.forEach(function (el, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'pg-dot';
      b.setAttribute('aria-label', labels[i] || '第' + (i + 1) + '屏');
      b.innerHTML = '<i></i><span class="pg-lab">' + (labels[i] || '') + '</span>';
      b.addEventListener('click', function () {
        var top = y0(el);
        if (el.offsetHeight > vh() + 40) top = Math.min(top, y0(el) + el.offsetHeight - vh());
        jump(top);
      });
      rail.appendChild(b);
      dots.push(b);
    });
    document.body.appendChild(rail);
    sync();
  }

  /* ---------- 事件 ---------- */
  function onWheel(e) {
    if (e.ctrlKey) return;                       /* 触控板捏合缩放不拦 */
    if (Math.abs(e.deltaY) < 1) return;          /* 纯横向滚动 */
    e.preventDefault();
    var now = performance.now();
    var idle = now - lastWheel;                 /* 距上一个事件的静默时长 */
    lastWheel = now;
    /* 静默够久 = 一次新的滑动开始，重置「本手势已翻过」的锁 */
    if (idle >= IDLE) { consumed = false; acc = 0; }
    /* 动画中、落位后的 COOL、以及本次手势已经翻过一屏：一律吞掉 */
    if (consumed || lock || now - lockAt < COOL) { acc = 0; return; }
    acc += e.deltaY;
    if (Math.abs(acc) >= TH) {
      var d = acc > 0 ? 1 : -1;
      acc = 0; consumed = true;                 /* 一次手势只走一格，惯性再大也不叠加 */
      step(d);
    }
  }

  function onKey(e) {
    var t = e.target;
    if (t && t.closest && t.closest('input,textarea,select,[contenteditable]')) return;
    var k = e.key;
    var down = k === 'ArrowDown' || k === 'PageDown' || k === ' ';
    var up = k === 'ArrowUp' || k === 'PageUp';
    if (!down && !up && k !== 'Home' && k !== 'End') return;
    if ((k === ' ' || k === 'Enter') && t && t.closest && t.closest('button,a')) return;
    e.preventDefault();
    if (k === 'Home') return jump(0);
    if (k === 'End') return jump(maxY());
    step(down ? 1 : -1);
  }

  function enable() {
    /* V296：页脚与合作伙伴并成一屏（合作区高度 = 100vh - 页脚高），
       所以页脚不再是独立一屏，停靠点与指示器都只认 section。 */
      secs = [].slice.call(document.querySelectorAll('header.hero, section'))
      .filter(function (el) { return !el.closest('.apane') && el.offsetHeight > 120; });
    var fallback = ['首页', '业务领域', '新闻中心', '发展历程', '合作伙伴', '联系信息'];
    labels = secs.map(function (el) {
      var h = el.querySelector('h1,h2');
      return (h && h.textContent.trim()) || '';
    });
    labels[0] = '首页';
    labels = labels.map(function (t, i) { return t || fallback[i] || ''; });

    setFootH();
    buildStops();
    buildRail();
    window.addEventListener('wheel', onWheel, { passive: false });
    window.addEventListener('keydown', onKey);
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onResize);
    document.documentElement.classList.add('pg-on');
  }

  function disable() {
    window.removeEventListener('wheel', onWheel, { passive: false });
    window.removeEventListener('keydown', onKey);
    window.removeEventListener('scroll', onScroll);
    window.removeEventListener('resize', onResize);
    if (rail && rail.parentNode) rail.parentNode.removeChild(rail);
    rail = null; dots = []; stops = []; lock = false;
    document.documentElement.classList.remove('pg-on');
  }

  var rt;
  function onResize() {
    clearTimeout(rt);
    rt = setTimeout(function () {
          setFootH();
          if (mq.matches) buildStops();
      sync();
    }, 160);
  }

  function check() { mq.matches ? (rail || enable()) : disable(); }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', check);
  } else {
    check();
  }
  if (mq.addEventListener) mq.addEventListener('change', check);

  window.addEventListener('load', function () {
    if (!mq.matches) return;
      setFootH();
      buildStops();
    sync();
  });
})();
