/* V342 首页首屏：点阵波浪（Canvas 2D）+ 底部压深
   网格由 CSS `.hero-grid` 负责画，这里只画从 30% 高度到底部的点阵：
   每个点按两重行波上下浮动、波峰更亮更大，整片读起来是「点阵在起伏」。
   - 亮度按深度递增（顶部极淡、底部明显），底部再铺一层渐变雾盖住画面杂色
   - 只在视口内、标签页可见时跑；prefers-reduced-motion 只画一帧静态波
   - 无外部依赖、无内联脚本 */
(function () {
  'use strict';
  var cv = document.getElementById('hero-dots');
  if (!cv || !cv.getContext) return;
  var reduce = !!(window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  var hero = cv.closest('.hero') || cv.parentElement;
  var ctx = cv.getContext('2d');
  var w = 0, h = 0, raf = 0, running = false, visible = true, t = 0, fog = null;
  var TOP = 0.30;      /* 点阵起始高度 */
  var BOTTOM = 0.44;   /* 底部压雾起点 */

  /* 透明度量化成 25 档复用字符串，避免每帧给上千点拼 rgba() */
  var AQ = [];
  for (var q = 0; q <= 24; q++) AQ.push('rgba(255,255,255,' + (q / 200).toFixed(4) + ')');

  function fogPaint() {
    if (!ctx.createLinearGradient) { fog = null; return; }
    fog = ctx.createLinearGradient(0, h * BOTTOM, 0, h);
    fog.addColorStop(0, 'rgba(8,18,54,0)');
    fog.addColorStop(0.52, 'rgba(8,18,54,.34)');
    fog.addColorStop(1, 'rgba(7,15,46,.80)');
  }

  function size() {
    var r = cv.getBoundingClientRect();
    w = Math.max(1, Math.round(r.width));
    h = Math.max(1, Math.round(r.height));
    var dpr = Math.min(2, window.devicePixelRatio || 1);
    cv.width = Math.round(w * dpr);
    cv.height = Math.round(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    fogPaint();
  }

  function draw() {
    ctx.clearRect(0, 0, w, h);
    if (fog) {
      ctx.fillStyle = fog;
      ctx.fillRect(0, h * BOTTOM, w, h - h * BOTTOM);
    }
    var step = Math.max(28, Math.min(40, Math.round(w / 45)));
    var y0 = h * TOP;
    var span = h - y0;
    var cols = Math.ceil(w / step) + 1;
    var rows = Math.ceil(span / step) + 1;
    var r, c, x, y, baseY, depth, ph, wave, amp, a, rad;
    for (r = 0; r < rows; r++) {
      baseY = y0 + r * step;
      if (baseY > h + step) break;
      depth = Math.min(1, (baseY - y0) / span);
      for (c = 0; c < cols; c++) {
        x = c * step;
        /* 单一方向的短波长正弦（一屏约 4 个周期）：每行都能跟上一条起伏曲线，
           相邻行相位错开 → 整片呈斜向流动的波纹。波长放长到 800px 时只剩一条
           渐变带、看不出「波浪」，别改回去 */
        ph = x * 0.018 + baseY * 0.010 + t * 0.026;
        wave = Math.sin(ph);
        amp = 0.5 + 0.5 * wave;
        /* 点仍钉在网格上，只给 11px（小于半个间距）的起伏，网格结构才没散 */
        y = baseY + wave * 11;
        a = (0.10 + 0.72 * Math.pow(amp, 1.8)) * (0.26 + 0.74 * depth);
        rad = (0.6 + 2.5 * Math.pow(amp, 1.5)) * (0.7 + 0.3 * depth);
        ctx.fillStyle = AQ[Math.max(0, Math.min(24, Math.round(a * 200)))];
        /* 波峰加一圈柔光，亮带才会连成片而不是孤立亮点 */
        if (a > 0.30) {
          ctx.globalAlpha = 0.30;
          ctx.beginPath(); ctx.arc(x, y, rad * 2.1, 0, 6.2832); ctx.fill();
          ctx.globalAlpha = 1;
        }
        ctx.beginPath(); ctx.arc(x, y, rad, 0, 6.2832); ctx.fill();
      }
    }
  }

  function step() {
    t++;
    draw();
    raf = window.requestAnimationFrame(step);
  }

  function sync() {
    var should = visible && !document.hidden && !reduce;
    if (should && !running) { running = true; raf = window.requestAnimationFrame(step); }
    else if (!should && running) { running = false; window.cancelAnimationFrame(raf); }
  }

  size(); draw(); sync();

  var rt;
  window.addEventListener('resize', function () {
    clearTimeout(rt);
    rt = setTimeout(function () { size(); draw(); }, 180);
  });
  document.addEventListener('visibilitychange', sync);
  if (window.IntersectionObserver) {
    new IntersectionObserver(function (es) {
      visible = es[0].isIntersecting;
      sync();
    }, { threshold: 0 }).observe(hero);
  }
})();
