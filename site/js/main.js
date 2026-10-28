/* Page controller: data loading, figure lifecycle, scroll steps, progress, tooltips, guesses, print.
   Every visible string lives in index.html (verbatim from 05_page_copy.md); this file only formats numbers. */
(function () {
  'use strict';

  const nf = new Intl.NumberFormat('id-ID');
  const nf1 = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
  const nfMax1 = new Intl.NumberFormat('id-ID', { maximumFractionDigits: 1 });
  const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'];
  const reduceMQ = window.matchMedia('(prefers-reduced-motion: reduce)');
  const ctx2d = document.createElement('canvas').getContext('2d');
  const FIG_IDS = ['g1', 'g2', 'g3', 'g4', 'g5', 'g6'];

  const App = window.App = {
    data: {},
    modules: {},
    figs: {},
    guess: { g1: null, g2: null },
    printing: false,
    MONTHS,
    // data colors (04 spec §3); never the UI pink
    C: {
      strong: '#C2410C', small: '#B8BEC6', smallText: '#6B7280', neutral: '#475569',
      strong20: '#F3D9CE', strongTint: '#F9ECE7', strong45: '#E4AA92', small35: '#E6E8EB',
      neutral8: '#F0F1F3', grid: '#E5E7EB', muted: '#6B7280', dark: '#1F2937', text: '#374151', label: '#4B5563'
    },
    fmt: (v) => nf.format(v),
    mag: (v) => nf1.format(v),
    dec: (v) => nfMax1.format(v),
    month: (ym) => MONTHS[+ym.slice(5, 7) - 1] + ' ' + ym.slice(0, 4),
    get reduced() { return reduceMQ.matches || App.printing; },
    dur: (ms) => (App.reduced ? 0 : ms),
    define(id, factory) { App.modules[id] = factory; }
  };

  /* ---------- drawing helpers shared by the figure modules ---------- */

  // Interrupt running transitions; return a transition (t > 0) or the plain selection (t = 0).
  App.tr = function (sel, t, delay) {
    sel.interrupt();
    if (!t) return sel;
    const x = sel.transition().duration(t).ease(d3.easeCubicOut);
    return delay ? x.delay(delay) : x;
  };

  App.measure = function (text, size, weight) {
    ctx2d.font = `${weight || 700} ${size || 13.6}px Nunito, "Segoe UI", system-ui, sans-serif`;
    return ctx2d.measureText(text).width;
  };

  App.wrapLines = function (text, maxW, size, weight) {
    const words = String(text).split(/\s+/);
    const lines = [];
    let line = '';
    words.forEach((w) => {
      const next = line ? line + ' ' + w : w;
      if (line && App.measure(next, size, weight) > maxW) { lines.push(line); line = w; } else { line = next; }
    });
    if (line) lines.push(line);
    return lines;
  };

  // Multi-line SVG text. opts: size, weight, anchor, lh, fill, cls, maxW, valign ('top'|'bottom'|'middle')
  App.label = function (g, text, x, y, opts) {
    const o = Object.assign({ size: 13.6, weight: 700, anchor: 'start', lh: 1.25, fill: App.C.text, cls: 'ann', valign: 'top' }, opts);
    const lines = o.maxW ? App.wrapLines(text, o.maxW, o.size, o.weight) : [String(text)];
    const lh = o.size * o.lh;
    let y0 = y + o.size * 0.8;
    if (o.valign === 'bottom') y0 = y - (lines.length - 1) * lh - o.size * 0.2;
    if (o.valign === 'middle') y0 = y - ((lines.length - 1) * lh) / 2 + o.size * 0.32;
    const t = g.append('text').attr('class', o.cls).attr('text-anchor', o.anchor)
      .style('font-size', o.size + 'px').style('font-weight', o.weight).attr('fill', o.fill);
    lines.forEach((ln, i) => t.append('tspan').attr('x', x).attr('y', y0 + i * lh).text(ln));
    t.node().__lines = lines.length;
    t.node().__width = Math.max(...lines.map((l) => App.measure(l, o.size, o.weight)));
    return t;
  };

  // Horizontal gridlines with tick labels on the left.
  App.yGrid = function (g, y, x0, x1, ticks, fmt) {
    const gg = g.append('g').attr('class', 'ygrid');
    ticks.forEach((v) => {
      gg.append('line').attr('x1', x0).attr('x2', x1).attr('y1', y(v)).attr('y2', y(v))
        .attr('stroke', v === 0 ? '#9CA3AF' : App.C.grid).attr('stroke-width', 1).attr('shape-rendering', 'crispEdges');
      gg.append('text').attr('x', x0 - 8).attr('y', y(v)).attr('dy', '0.32em').attr('text-anchor', 'end')
        .style('font-size', '12px').attr('fill', App.C.muted).text((fmt || App.fmt)(v));
    });
    return gg;
  };

  App.axisTitle = function (g, text, x, y, rotate) {
    return g.append('text').attr('class', 'axis-title').attr('text-anchor', rotate ? 'middle' : 'start')
      .attr('transform', `translate(${x},${y})${rotate ? ' rotate(-90)' : ''}`)
      .style('font-size', '12px').style('font-weight', 700).attr('fill', App.C.label).text(text);
  };

  // Deterministic pseudo-random numbers (easy-mode dot scatter must look the same every time).
  App.rng = function (seed) {
    let s = seed >>> 0;
    return () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  };

  /* ---------- figure lifecycle ---------- */

  function makeFigure(id) {
    const plot = document.getElementById(id + '-plot');
    const section = plot.closest('section');
    const svg = d3.select(plot).append('svg').attr('role', 'img').attr('focusable', 'false');
    if (id === 'gx') svg.attr('aria-labelledby', 'gx-title gx-sub');
    else svg.attr('aria-labelledby', id + '-alt').attr('aria-describedby', id + '-easy');
    const fig = { id, n: +(section.dataset.n || 0), section, plot, svg, state: 0, easy: false, w: 0, h: 0 };
    fig.mod = App.modules[id]({ svg, plot, fig, data: App.data });
    fig.final = fig.mod.final || 0;
    fig.draw = function () {
      const r = plot.getBoundingClientRect();
      const w = Math.round(r.width), h = Math.round(r.height);
      if (w < 40 || h < 40) return;
      fig.w = w; fig.h = h;
      svg.attr('viewBox', `0 0 ${w} ${h}`);
      svg.selectAll('*').interrupt();
      svg.selectAll('*').remove();
      fig.mod.draw(w, h);
      fig.mod.state(fig.easy ? fig.state : fig.state, 0);
      if (fig.easy) fig.mod.easy(true, 0);
      if (fig.afterDraw) fig.afterDraw();
    };
    // Move to a scroll state. Idempotent: the module sets every mark for the given state.
    fig.go = function (s, instant) {
      fig.state = s;
      if (fig.easy || !fig.w) return;
      fig.mod.state(s, instant ? 0 : App.dur(550));
      if (fig.afterState) fig.afterState(s);
    };
    let last = '';
    new ResizeObserver(() => {
      const r = plot.getBoundingClientRect();
      const key = Math.round(r.width) + 'x' + Math.round(r.height);
      if (key === last || App.printing) return;
      last = key;
      requestAnimationFrame(fig.draw);
    }).observe(plot);
    return fig;
  }

  /* ---------- scroll steps (Scrollama, with an IntersectionObserver fallback) ---------- */

  const scrollers = [];
  App.resizeScrollers = function () { scrollers.forEach((s) => s.resize && s.resize()); };

  function setupSteps(fig) {
    const steps = Array.from(fig.section.querySelectorAll('.step'));
    const enter = (el) => {
      if (fig.easy || App.printing) return;
      steps.forEach((s) => s.classList.toggle('is-active', s === el));
      const i = +el.dataset.step;
      fig.go(i);
      if (fig.onStep) fig.onStep(i);
    };
    // Safety net for jumps (fast flings, End key, progress links, reload mid-page) that skip a step's trigger:
    // after scrolling settles, apply the last step whose midpoint is above the 60% line.
    fig.syncStep = function () {
      if (fig.easy || App.printing) return;
      const box = fig.section.getBoundingClientRect();
      if (box.bottom < 0 || box.top > window.innerHeight) return;
      const line = window.innerHeight * 0.6;
      let idx = 0;
      steps.forEach((s, i) => { const r = s.getBoundingClientRect(); if (r.top + r.height / 2 <= line) idx = i; });
      if (idx !== fig.state || !steps[idx].classList.contains('is-active')) enter(steps[idx]);
    };
    if (window.scrollama) {
      const sc = window.scrollama();
      sc.setup({ step: steps, offset: 0.6 }).onStepEnter((r) => enter(r.element));
      scrollers.push(sc);
    } else {
      // fallback: a trigger line at 60% of the viewport
      const io = new IntersectionObserver((entries) => {
        entries.forEach((e) => { if (e.isIntersecting) enter(e.target); });
      }, { rootMargin: '-60% 0px -40% 0px' });
      steps.forEach((s) => io.observe(s));
      scrollers.push({ resize() {} });
    }
  }

  /* ---------- tooltips: hover, tap and keyboard (one scrubber per chart) ---------- */

  function setupTips(fig) {
    const scrub = document.createElement('div');
    scrub.className = 'scrubber';
    scrub.tabIndex = 0;
    scrub.setAttribute('role', 'slider');
    scrub.setAttribute('aria-labelledby', fig.id + '-title');
    scrub.setAttribute('aria-valuemin', '1');
    scrub.setAttribute('aria-valuemax', '1');
    scrub.setAttribute('aria-valuenow', '1');
    const tip = document.createElement('div');
    tip.className = 'tip';
    tip.hidden = true;
    tip.setAttribute('aria-hidden', 'true');
    fig.plot.append(scrub, tip);
    let idx = -1;

    const items = () => (fig.easy || !fig.mod.tips ? [] : fig.mod.tips());
    function show(i) {
      const it = items();
      if (!it.length) { hide(); return; }
      idx = Math.max(0, Math.min(it.length - 1, i));
      const d = it[idx];
      tip.textContent = d.text;
      tip.style.left = Math.max(70, Math.min(fig.w - 70, d.x)) + 'px';
      tip.style.top = d.y + 'px';
      tip.classList.toggle('below', d.y < 64);
      tip.hidden = false;
      scrub.setAttribute('aria-valuemax', String(it.length));
      scrub.setAttribute('aria-valuenow', String(idx + 1));
      scrub.setAttribute('aria-valuetext', d.text);
      if (fig.mod.highlight) fig.mod.highlight(d);
    }
    function hide() {
      tip.hidden = true;
      if (fig.mod.highlight) fig.mod.highlight(null);
    }
    function nearest(e) {
      const r = fig.plot.getBoundingClientRect();
      const px = e.clientX - r.left, py = e.clientY - r.top;
      const it = items();
      let best = -1, bd = Infinity;
      it.forEach((d, i) => {
        const dx = px - d.x, dy = d.xOnly ? 0 : (py - d.y) * 0.6;
        const dd = dx * dx + dy * dy;
        if (dd < bd) { bd = dd; best = i; }
      });
      return best;
    }
    scrub.addEventListener('pointermove', (e) => { if (e.pointerType === 'mouse') { const i = nearest(e); if (i >= 0) show(i); } });
    scrub.addEventListener('pointerleave', (e) => { if (e.pointerType === 'mouse') hide(); });
    scrub.addEventListener('pointerdown', (e) => { if (e.pointerType !== 'mouse') { const i = nearest(e); if (i >= 0) show(i); } });
    document.addEventListener('pointerdown', (e) => { if (!fig.plot.contains(e.target)) hide(); });
    scrub.addEventListener('focus', () => show(idx < 0 ? 0 : idx));
    scrub.addEventListener('blur', hide);
    scrub.addEventListener('keydown', (e) => {
      const n = items().length;
      const step = { ArrowRight: 1, ArrowUp: 1, ArrowLeft: -1, ArrowDown: -1, PageUp: 10, PageDown: -10 }[e.key];
      if (step) { show((idx < 0 ? 0 : idx) + step); e.preventDefault(); }
      else if (e.key === 'Home') { show(0); e.preventDefault(); }
      else if (e.key === 'End') { show(n - 1); e.preventDefault(); }
      else if (e.key === 'Escape') hide();
    });
    fig.tipsSync = function () {
      scrub.hidden = fig.easy;
      if (!tip.hidden) hide();
      idx = Math.min(idx, items().length - 1);
    };
  }

  /* ---------- guesses (G1 buttons, G2 slider); never block scrolling ---------- */

  function setupGuessG1() {
    const fig = App.figs.g1;
    const sec = fig.section;
    const choices = Array.from(sec.querySelectorAll('.btn-choice'));
    const skip = sec.querySelector('.step-guess .btn-skip');
    const revealStep = sec.querySelector('.step-reveal');
    const fb = revealStep.querySelector('.feedback');
    function reveal(kind) {
      if (App.guess.g1) return;
      App.guess.g1 = kind;
      choices.forEach((b) => { b.setAttribute('aria-disabled', 'true'); b.disabled = false; b.setAttribute('aria-pressed', String(b.dataset.answer === kind)); });
      skip.setAttribute('aria-disabled', 'true');
      fb.textContent = kind === 'turun' ? fb.dataset.turun : kind === 'skipped' ? fb.dataset.skipped : fb.dataset.other;
      revealStep.classList.add('is-revealed');
      fig.go(4);
    }
    choices.forEach((b) => b.addEventListener('click', () => { if (!App.guess.g1) reveal(b.dataset.answer); }));
    skip.addEventListener('click', () => { if (!App.guess.g1) reveal('skipped'); });
    fig.onStep = (i) => { if (i >= 4 && !App.guess.g1) reveal('skipped'); };
  }

  function setupGuessG2() {
    const fig = App.figs.g2;
    const sec = fig.section;
    const slider = sec.querySelector('#g2-slider');
    const out = sec.querySelector('#g2-out');
    const answer = sec.querySelector('#g2-answer');
    const skip = sec.querySelector('.step-guess .btn-skip');
    const fb = sec.querySelector('.step-guess .feedback');
    const sync = () => { out.value = App.fmt(+slider.value); out.textContent = App.fmt(+slider.value); };
    slider.addEventListener('input', sync);
    slider.addEventListener('keydown', (e) => {
      const d = { PageUp: 10, PageDown: -10 }[e.key];
      if (d) { slider.value = Math.max(0, Math.min(100, +slider.value + d)); sync(); e.preventDefault(); }
    });
    function reveal(kind) {
      if (App.guess.g2) return;
      App.guess.g2 = kind;
      fb.textContent = kind === 'skipped' ? fb.dataset.skipped : fb.dataset.answered.replace('{x}', App.fmt(+slider.value));
      answer.setAttribute('aria-disabled', 'true');
      skip.setAttribute('aria-disabled', 'true');
    }
    answer.addEventListener('click', () => reveal('answered'));
    skip.addEventListener('click', () => reveal('skipped'));
    fig.onStep = (i) => { if (i >= 1 && !App.guess.g2) reveal('skipped'); };
    sync();
  }

  /* ---------- progress bar: Setup · Konflik · Resolusi ---------- */

  function setupProgress() {
    const segs = Array.from(document.querySelectorAll('.progress .seg'));
    const fills = segs.map((s) => s.querySelector('.seg-fill'));
    const top = (el) => el.getBoundingClientRect().top + window.scrollY;
    function bounds() {
      const vh = window.innerHeight;
      const konflikEl = visible(document.getElementById('g1-step-4')) || document.getElementById('g1');
      const a = top(konflikEl) - vh * 0.6;
      const b = top(document.getElementById('g5')) - vh * 0.6;
      const end = document.documentElement.scrollHeight - vh;
      return [[0, a], [a, b], [b, end]];
    }
    let ticking = false;
    function update() {
      ticking = false;
      const y = window.scrollY;
      const bs = bounds();
      let current = 0;
      bs.forEach(([s, e], i) => {
        const f = Math.max(0, Math.min(1, (y - s) / Math.max(1, e - s)));
        fills[i].style.transform = `scaleX(${f})`;
        if (y >= s) current = i;
      });
      segs.forEach((s, i) => { if (i === current) s.setAttribute('aria-current', 'step'); else s.removeAttribute('aria-current'); });
    }
    const req = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
    window.addEventListener('scroll', req, { passive: true });
    window.addEventListener('resize', req);
    App.updateProgress = req;
    segs.forEach((s) => s.addEventListener('click', (e) => {
      const id = s.getAttribute('href').slice(1);
      let target = document.getElementById(id);
      if (!visible(target)) target = target.closest('section');
      e.preventDefault();
      if (id === 'hero') window.scrollTo({ top: 0, behavior: App.reduced ? 'auto' : 'smooth' });
      else target.scrollIntoView({ behavior: App.reduced ? 'auto' : 'smooth', block: 'start' });
    }));
    update();
  }

  function visible(el) { return el && el.offsetParent !== null ? el : null; }

  /* ---------- header height (sticky offsets) ---------- */

  function trackHeader() {
    const header = document.querySelector('.site-header');
    const set = () => document.documentElement.style.setProperty('--header-h', header.offsetHeight + 'px');
    new ResizeObserver(set).observe(header);
    set();
  }

  /* ---------- hero decoration: monthly M4+ line at 15% opacity, drawn once ---------- */

  function heroLine() {
    const svg = d3.select('.hero-line');
    const node = svg.node();
    const draw = () => {
      const w = node.clientWidth, h = node.clientHeight;
      if (!w || !h) return;
      svg.attr('viewBox', `0 0 ${w} ${h}`).selectAll('*').remove();
      const months = App.data.f5.months;
      const x = d3.scaleLinear().domain([0, months.length - 1]).range([0, w]);
      const y = d3.scaleLinear().domain([0, 400]).range([h, 0]);
      const line = d3.line().defined((d) => d.value !== null).x((d, i) => x(i)).y((d) => y(d.value)).curve(d3.curveMonotoneX);
      const p = svg.append('path').attr('d', line(months)).attr('fill', 'none').attr('stroke', '#3F1D38').attr('stroke-width', 1.5);
      if (!App.reduced) {
        const len = p.node().getTotalLength();
        p.attr('stroke-dasharray', `${len} ${len}`).attr('stroke-dashoffset', len)
          .transition().duration(6000).ease(d3.easeCubicOut).attr('stroke-dashoffset', 0);
      }
    };
    draw();
    let last = node.clientWidth;
    window.addEventListener('resize', () => { if (Math.abs(node.clientWidth - last) > 40) { last = node.clientWidth; draw(); } });
  }

  /* ---------- print: every figure in its final state, no easy blocks ---------- */

  function setupPrint() {
    let saved = null;
    const g2fb = () => document.querySelector('#g2 .step-guess .feedback');
    function before() {
      if (saved) return;
      App.printing = true;
      saved = { g2fb: g2fb().textContent };
      Object.values(App.figs).forEach((fig) => {
        fig._print = { state: fig.state, easy: fig.easy };
        if (fig.easy) fig.mod.easy(false, 0);
        fig.easy = false;
        fig.mod.state(fig.final, 0);
      });
      if (!App.guess.g2) g2fb().textContent = g2fb().dataset.skipped;
    }
    function after() {
      if (!saved) return;
      g2fb().textContent = saved.g2fb;
      Object.values(App.figs).forEach((fig) => {
        fig.easy = fig._print.easy;
        fig.mod.state(fig._print.state, 0);
        if (fig.easy) fig.mod.easy(true, 0);
      });
      saved = null;
      App.printing = false;
    }
    window.addEventListener('beforeprint', before);
    window.addEventListener('afterprint', after);
    const mq = window.matchMedia('print');
    if (mq.addEventListener) mq.addEventListener('change', (e) => (e.matches ? before() : after()));
  }

  /* ---------- start ---------- */

  App.start = async function () {
    document.documentElement.classList.add('js');
    trackHeader();
    const names = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'fx'];
    const loaded = await Promise.all(names.map((n) => fetch(`data/${n}.json`).then((r) => {
      if (!r.ok) throw new Error(`data/${n}.json: HTTP ${r.status}`);
      return r.json();
    })));
    names.forEach((n, i) => { App.data[n] = loaded[i]; });
    if (document.fonts) {
      await Promise.race([document.fonts.load('700 16px Nunito').then(() => document.fonts.ready), new Promise((r) => setTimeout(r, 2500))]);
    }
    FIG_IDS.concat('gx').forEach((id) => { App.figs[id] = makeFigure(id); });
    Object.values(App.figs).forEach((fig) => fig.draw());
    FIG_IDS.forEach((id) => { setupSteps(App.figs[id]); setupTips(App.figs[id]); });
    setupGuessG1();
    setupGuessG2();
    setupProgress();
    setupPrint();
    heroLine();
    App.easy.init();
    App.tool.init();
    window.addEventListener('resize', App.resizeScrollers);
    let settle = 0;
    const syncAll = () => FIG_IDS.forEach((id) => App.figs[id].syncStep());
    window.addEventListener('scroll', () => { clearTimeout(settle); settle = setTimeout(syncAll, 140); }, { passive: true });
    syncAll();
    if (document.fonts) document.fonts.addEventListener('loadingdone', () => Object.values(App.figs).forEach((f) => f.draw()));
  };
})();
