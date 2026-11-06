/* V339 首页首屏氛围层：轻量粒子 / 点阵（Canvas 2D）
   - 只在 #hero-dots 存在时启动；尺寸由 CSS 决定，这里只按实际像素设缓冲
   - 离屏、后台标签、prefers-reduced-motion 自动停，满屏滚动时不白耗 CPU
   - 无外部依赖、无内联脚本；点很淡，只做氛围，不抢标题与反白页头 */
(function () {
  'use strict';
  var cv = document.getElementById('hero-dots');
  if (!cv || !cv.getContext) return;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var hero = cv.closest('.hero') || cv.parentElement;
  var ctx = cv.getContext('2d');
  var w = 0, h = 0, pts = [], raf = 0, running = false, visible = true, t = 0;

  function make() {
    var n = Math.max(28, Math.min(84, Math.round(w * h / 20000)));
    pts = [];
    for (var i = 0; i < n; i++) {
      pts.push({
        x: Math.random() * w,
        y: Math.random() * h,
        r: 0.6 + Math.random() * 1.1,
        a: 0.14 + Math.random() * 0.30,
        vy: -(0.045 + Math.random() * 0.13),
        ph: Math.random() * Math.PI * 2,
        sp: 0.003 + Math.random() * 0.005
      });
    }
  }

  function size() {
    var r = cv.getBoundingClientRect();
    w = Math.max(1, Math.round(r.width));
    h = Math.max(1, Math.round(r.height));
    var dpr = Math.min(2, window.devicePixelRatio || 1);
    cv.width = Math.round(w * dpr);
    cv.height = Math.round(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    make();
  }

  function draw() {
    ctx.clearRect(0, 0, w, h);
    var i, j, p, q, dx, dy, d2, max = 17000;
    /* 只在很近的两个点之间连一条极淡的线，读起来是「点阵」而不是流星雨 */
    for (i = 0; i < pts.length; i++) {
      p = pts[i];
      for (j = i + 1; j < pts.length; j++) {
        q = pts[j];
        dx = p.x - q.x; dy = p.y - q.y; d2 = dx * dx + dy * dy;
        if (d2 < max) {
          ctx.strokeStyle = 'rgba(255,255,255,' + (0.055 * (1 - d2 / max)).toFixed(3) + ')';
          ctx.lineWidth = 0.6;
          ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y); ctx.stroke();
        }
      }
    }
    for (i = 0; i < pts.length; i++) {
      p = pts[i];
      ctx.fillStyle = 'rgba(255,255,255,' + (p.a * (0.75 + 0.25 * Math.sin(t * 0.02 + p.ph))).toFixed(3) + ')';
      ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fill();
    }
  }

  function step() {
    t++;
    for (var i = 0; i < pts.length; i++) {
      var p = pts[i];
      p.y += p.vy;
      p.x += Math.sin(t * p.sp + p.ph) * 0.09;
      if (p.y < -4) { p.y = h + 4; p.x = Math.random() * w; }
      if (p.x < -4) p.x = w + 4; else if (p.x > w + 4) p.x = -4;
    }
    draw();
    raf = window.requestAnimationFrame(step);
  }

  function sync() {
    var should = visible && !document.hidden;
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
