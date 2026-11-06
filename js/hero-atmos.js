/* V343 首页首屏：底部点阵波浪（Canvas 2D）+ 底部压深
   网格由 CSS `.hero-grid` 负责画，这里只画下半屏的点阵：
   点的大小、亮度、起伏幅度全部由「离屏底的距离」驱动 —— 屏底大而实、
   往上渐小渐隐；相位里叠一层低频调制，波峰间距不均匀，读起来像自然水面。
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
  var TOP = 0.50;      /* 点阵起始高度：只铺下半屏 */
  var BOTTOM = 0.42;   /* 底部压雾起点 */

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
    var step = Math.max(30, Math.min(42, Math.round(w / 46)));
    var y0 = h * TOP;
    var span = h - y0;
    var cols = Math.ceil(w / step) + 1;
    var rows = Math.ceil(span / step) + 1;
    var r, c, x, y, baseY, g, ph, mod, wave, amp, a, rad;
    for (r = 0; r < rows; r++) {
      baseY = y0 + r * step;
      if (baseY > h + step) break;
      g = Math.min(1, (baseY - y0) / span);   /* 0 = 点阵顶部，1 = 屏底 */
      for (c = 0; c < cols; c++) {
        x = c * step;
        /* 结构要点：相位主要随「行」推进（y 方向波长短），整行的点同亮同暗，
           才会形成一条条横向波带；x 方向只给很小的系数 + 一层低频弯折，
           带子就成了缓慢起伏的波浪线而不是笔直的扫描线。 */
        mod = 1.3 * Math.sin(x * 0.0058 + t * 0.012);
        ph = x * 0.0022 + baseY * 0.0244 + t * 0.030 + mod;
        wave = Math.sin(ph);
        amp = 0.5 + 0.5 * wave;
        /* 点随波上下浮动（底部 ±16px），波峰波谷才有实体感 */
        y = baseY + wave * (6 + 10 * g);
        /* 大小与亮度都由深度驱动：屏底大而实，向上渐小渐隐，最上一行几乎看不见 */
        var glow = 0.03 + 0.97 * Math.pow(g, 1.55);
        a = (0.10 + 0.85 * Math.pow(amp, 1.7)) * glow;
        /* 系数 5.0→3.6：峰值半径 6.5→4.9（-25%），底数 0.7 不动，
           所以只是最大的点收小，小点的尺寸几乎不变 */
        rad = 0.7 + 3.6 * Math.pow(g, 0.82) * (0.58 + 0.58 * amp);
        ctx.fillStyle = AQ[Math.max(0, Math.min(24, Math.round(a * 200)))];
        /* 只给「大且亮」的点补柔光，波峰连成亮带；小点不补，省一半绘制量 */
        if (rad > 2.2 && a > 0.30) {
          ctx.globalAlpha = 0.26;
          ctx.beginPath(); ctx.arc(x, y, rad * 1.9, 0, 6.2832); ctx.fill();
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
