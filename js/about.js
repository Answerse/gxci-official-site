/* ============================================================
   关于我们：发展历程（纵向时间轴）
   年份与条目口径来自宣传册（20261013 版），与首页一致；
   配图摘自 40 周年纪念册大事记（仅收录与条目对应的照片）
   ============================================================ */
(function () {
  'use strict';

var HIST = [
    { y: '2026', items: [
      { t: '自研产业互联网平台“桂农易通”正式上线。' },
      { t: '自研“桂资通”国有资产数字化监管与运营底座，支撑自治区国资委上线广西国有企业房产类资产登记管理系统。' },
      { t: '联合清华大学、广西大学申报的陈皮多组学 + AI 智能溯源分级项目，获自治区科技厅“2026 协同行动计划”首批立项。' }
    ] },
    { y: '2025', items: [
      { t: '自研广西桑蚕茧丝绸产业服务平台“茧易通”在河池上线，助力广西国控集团斩获广西智慧农业（数字乡村）创新大赛三等奖。', img: 'assets/img/hist/hist-2025a.jpg?v=75', cap: '茧易通平台正式上线' },
      { t: '自研陈皮产业服务平台“浦北陈皮通”在钦州浦北上线。', img: 'assets/img/hist/hist-2025b.jpg?v=75', cap: '浦北陈皮通签约上线' }
    ] },
    { y: '2023', items: [
      { t: '参与规划建设的广西阳光采购服务平台标准化开评标场地投入使用。', img: 'assets/img/hist/hist-2023.jpg?v=75', cap: '阳光采购服务平台开评标场地' }
    ] },
    { y: '2022', items: [
      { t: '承建的宏桂集团信息化建设数字化运营平台一期项目 21 个子系统全部上线运行。' }
    ] },
    { y: '2021', items: [
      { t: '获认定为自治区高新技术企业。', img: 'assets/img/hist/hist-2021.jpg?v=75', cap: '高新技术企业备案认定' }
    ] },
    { y: '2020', items: [
      { t: '恢复运营并完成混改。' },
      { t: '启动宏桂集团信息化规划咨询项目。', img: 'assets/img/hist/hist-2020.jpg?v=75', cap: '信息化规划咨询项目启动' }
    ] },
    { y: '2019', items: [
      { t: '北部湾交易集团增资并控股广西计算机公司。' }
    ] },
    { y: '2018', items: [
      { t: '由全民所有制企业改制为有限责任公司，更名为广西计算机有限责任公司。', img: 'assets/img/hist/hist-2018.jpg?v=75', cap: '公司制改制' }
    ] },
    { y: '2017', items: [
      { t: '经广西壮族自治区人民政府批准，由自治区工业和信息化委员会划转至广西宏桂资本运营集团有限公司。', img: 'assets/img/hist/hist-2017.jpg?v=75', cap: '划转至宏桂集团' }
    ] },
    { y: '2016', items: [
      { t: '推动全区及 14 个地市公共资源交易中心、社保局落地电子认证服务。' }
    ] },
    { y: '2008', items: [
      { t: '推动构建全区统一电子认证体系，全面促进数字证书在电子政务、电子商务等领域的应用。' }
    ] },
    { y: '2003', items: [
      { t: '注册成立广西数字证书认证中心（简称广西CA）。' },
      { t: '以自有人员班底支撑广西CA建设，实行一套人马、两块牌子模式，统筹开展相关运营工作。' }
    ] },
    { y: '2002', items: [
      { t: '由筹备组主要负责人杜文宏、黄山华发起并推动，自治区信息产业局发文，批准成立广西数字证书认证中心。' }
    ] },
    { y: '1990', items: [
      { t: '经广西壮族自治区计划委员会批复同意，更名为广西壮族自治区计算机公司。', img: 'assets/img/hist/hist-1990.jpg?v=75', cap: '更名批复材料' }
    ] },
    { y: '1986', items: [
      { t: '广西壮族自治区计算机技术服务公司成立。', img: 'assets/img/hist/hist-1986.jpg?v=75', cap: '公司成立' },
      { t: '主营计算机及外设、办公自动化设备、机房配件，承接计算机工程与技术服务。' }
    ] }
  ];

  var list = document.getElementById('hist-list');
  if (!list) return;

  list.innerHTML = HIST.map(function (h) {
    var es = h.items.map(function (e) {
      var fig = e.img
        ? '<figure class="hist-fig"><img src="' + e.img + '" alt="' + (e.cap || '') + '" loading="lazy">'
          + (e.cap ? '<figcaption>' + e.cap + '</figcaption>' : '') + '</figure>'
        : '';
      return '<div class="hist-e' + (e.img ? ' has-fig' : '') + '"><p>' + e.t + '</p>' + fig + '</div>';
    }).join('');
    return '<section class="hist-y rv">'
      + '<h4 class="hist-yr">' + h.y + '</h4>'
      + '<span class="hist-axis" aria-hidden="true"><i></i></span>'
      + '<div class="hist-es">' + es + '</div>'
      + '</section>';
  }).join('');

  /* 滚动加载动效：每年一节进入视口后依次点亮节点、条目上浮 */
  var ys = list.querySelectorAll('.hist-y');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.18, rootMargin: '0px 0px -6% 0px' });
    ys.forEach(function (el) { io.observe(el); });
  } else {
    ys.forEach(function (el) { el.classList.add('in'); });
  }
})();
