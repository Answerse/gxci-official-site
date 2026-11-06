/* V341 首页首屏氛围层：底部密集粒子 / 点阵（Canvas 2D）
   用户要求：更明显、集中在屏幕底部、顺带压住图片下方的杂乱元素。
   - 约 82% 粒子落在下半屏，缓慢上飘，越靠下越大越亮
   - 每帧先铺一层底部渐变雾，压住画面杂色，粒子与短线再叠颗粒感
   - 只在视口内、标签页可见时跑；prefers-reduced-motion 直接不启动
   - 无外部依赖、无内联脚本 */
(function () {
  'use strict';
  var cv = document.getElementById('hero-dots');
  if (!cv || !cv.getContext) return;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var hero = cv.closest('.hero') || cv.parentElement;
  var ctx = cv.getContext('2d');
  var w = 0, h = 0, pts = [], raf = 0, running = false, visible = true, t = 0, fog = null;
  var BOTTOM = 0.46;       /* 底部雾与密集区起点 */
  var LINK2 = 120 * 120;   /* 连线阈值（平方） */

  function make() {
    var n = Math.max(150, Math.min(250, Math.round(w / 7)));
    pts = [];
    for (var i = 0; i < n; i++) {
      var deep = Math.random() < 0.86;
      var y = deep ? h * (BOTTOM + Math.random() * (1 - BOTTOM)) : Math.random() * h;
      var near = 0.7 + 0.6 * (y / h);
      pts.push({
        x: Math.random() * w,
        y: y,
        r: (0.9 + Math.random() * 1.5) * near,
        a: (0.30 + Math.random() * 0.50) * (0.6 + 0.4 * (y / h)),
        vy: -(0.14 + Math.random() * 0.42),
        ph: Math.random() * Math.PI * 2,
        sp: 0.003 + Math.random() * 0.005
      });
    }
  }

  function fogPaint() {
    if (!ctx.createLinearGradient) { fog = null; return; }
    fog = ctx.createLinearGradient(0, h * BOTTOM, 0, h);
    fog.addColorStop(0, 'rgba(8,18,54,0)');
    fog.addColorStop(0.5, 'rgba(8,18,54,.42)');
    fog.addColorStop(1, 'rgba(7,15,46,.84)');
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
    make();
  }

  function draw() {
    ctx.clearRect(0, 0, w, h);
    if (fog) {
      ctx.fillStyle = fog;
      ctx.fillRect(0, h * BOTTOM, w, h - h * BOTTOM);
    }
    var cut = h * BOTTOM;
    var i, j, p, q, dx, dy, d2;
    /* 只在底部密集区连极淡短线，读起来是点阵，不抢画面 */
    for (i = 0; i < pts.length; i++) {
      p = pts[i];
      if (p.y < cut) continue;
      for (j = i + 1; j < pts.length; j++) {
        q = pts[j];
        if (q.y < cut) continue;
        dx = p.x - q.x; dy = p.y - q.y; d2 = dx * dx + dy * dy;
        if (d2 < LINK2) {
          ctx.strokeStyle = 'rgba(255,255,255,' + (0.10 * (1 - d2 / LINK2)).toFixed(3) + ')';
          ctx.lineWidth = 0.7;
          ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y); ctx.stroke();
        }
      }
    }
    /* 每个点画两层：外圈柔光 + 实芯，点才「亮得出来」而不是细沙。
       亮度按高度衰减 —— 飘到底部以上迅速变淡，整体密度才真的落在下半屏。 */
    for (i = 0; i < pts.length; i++) {
      p = pts[i];
      var tw = 0.72 + 0.28 * Math.sin(t * 0.025 + p.ph);
      var vis = p.y >= cut ? 1 : Math.max(0.08, (p.y / cut) * (p.y / cut));
      var a1 = p.a * tw * vis;
      ctx.fillStyle = 'rgba(255,255,255,' + (a1 * 0.24).toFixed(3) + ')';
      ctx.beginPath(); ctx.arc(p.x, p.y, p.r * 2.4, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = 'rgba(255,255,255,' + a1.toFixed(3) + ')';
      ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fill();
    }
  }

  function step() {
    t++;
    for (var i = 0; i < pts.length; i++) {
      var p = pts[i];
      p.y += p.vy;
      p.x += Math.sin(t * p.sp + p.ph) * 0.10;
      if (p.y < -6) { p.y = h + 6; p.x = Math.random() * w; }
      if (p.x < -6) p.x = w + 6; else if (p.x > w + 6) p.x = -6;
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
