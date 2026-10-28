/* Easy mode ("Versi mudah"): per-section toggles, the global toggle with its mixed state, and the
   block components (number / compare / dots) that figures morph into. Spec 04 §6. */
(function () {
  'use strict';
  const App = window.App;
  const SECTIONS = ['hero', 'g1', 'g2', 'jembatan', 'g3', 'g4', 'g5', 'g6'];
  const STORE_KEY = 'vdl-gempa-versi-mudah';
  const TONE = { strong: '#C2410C', small: '#B8BEC6', neutral: '#475569' };
  const TONE_TEXT = { strong: '#C2410C', small: '#6B7280', neutral: '#475569' };

  /* ---------- block components, drawn inside the figure's SVG ---------- */

  // spec: { type: 'compare'|'dots'|'number', tone, rows: [{label, value}], value, highlight, caption }
  App.block = function (svg, w, h, spec) {
    const g = svg.append('g').attr('class', 'block').style('opacity', 0).style('pointer-events', 'none');
    const color = TONE[spec.tone], textColor = TONE_TEXT[spec.tone];
    const geo = {};
    const parts = [];

    if (spec.type === 'compare') {
      const cw = Math.min(w - 24, 560);
      const x0 = (w - cw) / 2;
      const maxV = d3.max(spec.rows, (r) => r.value);
      const vSize = Math.max(22, Math.min(30, h * 0.07));
      const valW = d3.max(spec.rows, (r) => App.measure(App.fmt(r.value), vSize, 800)) + 14;
      const trackW = cw - valW;
      const bh = Math.max(20, Math.min(30, h * 0.075));
      const labelH = 17, rowH = labelH + 8 + bh, gap = Math.max(26, h * 0.09);
      const top = (h - (2 * rowH + gap)) / 2;
      geo.bars = [];
      spec.rows.forEach((r, i) => {
        const ry = top + i * (rowH + gap);
        const by = ry + labelH + 8;
        const bw = Math.max(bh, (trackW * r.value) / maxV);
        g.append('text').attr('x', x0).attr('y', ry + 13).style('font-size', '15px').style('font-weight', 700)
          .attr('fill', App.C.text).text(r.label);
        g.append('rect').attr('x', x0).attr('y', by).attr('width', trackW).attr('height', bh).attr('rx', bh / 2).attr('fill', App.C.neutral8);
        const bar = g.append('rect').attr('class', 'block-bar').attr('x', x0).attr('y', by).attr('width', bw).attr('height', bh)
          .attr('rx', bh / 2).attr('fill', color);
        g.append('text').attr('class', 'block-value').attr('x', x0 + trackW + 12).attr('y', by + bh / 2).attr('dy', '0.35em')
          .style('font-size', vSize + 'px').style('font-weight', 800).attr('fill', textColor).text(App.fmt(r.value));
        geo.bars.push({ x: x0, y: by, w: bw, h: bh });
        parts.push({ bar, bw });
      });
    }

    if (spec.type === 'dots') {
      const cell = Math.min((w - 24) / 20, (h * 0.66) / 5, 34);
      const gw = cell * 20;
      const x0 = (w - gw) / 2;
      const top = (h - (cell * 5 + 44)) / 2;
      geo.r = cell * 0.36;
      geo.dots = d3.range(100).map((i) => ({ x: x0 + cell * ((i % 20) + 0.5), y: top + cell * (Math.floor(i / 20) + 0.5) }));
      g.append('text').attr('x', w / 2).attr('y', top + cell * 5 + 32).attr('text-anchor', 'middle')
        .style('font-size', '20px').style('font-weight', 800).attr('fill', textColor).text(spec.caption);
    }

    if (spec.type === 'number') {
      const size = Math.max(64, Math.min(112, h * 0.3));
      const cy = h * 0.46;
      const num = g.append('text').attr('class', 'block-number').attr('x', w / 2).attr('y', cy).attr('text-anchor', 'middle')
        .style('font-size', size + 'px').style('font-weight', 800).attr('fill', textColor).text(App.fmt(spec.value));
      const n = spec.value, gapX = 24;
      const dots = g.append('g');
      d3.range(n).forEach((i) => dots.append('circle').attr('class', 'block-dot')
        .attr('cx', w / 2 + (i - (n - 1) / 2) * gapX).attr('cy', cy + 40).attr('r', 7).attr('fill', color));
      geo.center = { x: w / 2, y: cy - size * 0.35 };
      parts.push({ num, value: spec.value, dots });
    }

    return {
      g,
      geo,
      // grow: bars grow from zero (crossfade fallback); count: number counts up from 0
      show(t, delay, opts) {
        const o = opts || {};
        App.tr(g, t ? 250 : 0, delay).style('opacity', 1);
        parts.forEach((p) => {
          if (p.bar && o.grow) { p.bar.attr('width', 0); App.tr(p.bar, t ? 350 : 0, (delay || 0) + 100).attr('width', p.bw); }
          if (p.num) {
            if (t) {
              p.num.text(App.fmt(0));
              p.num.transition().delay((delay || 0) + 100).duration(700).ease(d3.easeCubicOut)
                .textTween(() => (k) => App.fmt(Math.round(p.value * k)));
              p.dots.selectAll('circle').attr('r', 0).transition().delay((_, i) => (delay || 0) + 500 + i * 90).duration(250).attr('r', 7);
            } else {
              p.num.interrupt().text(App.fmt(p.value));
              p.dots.selectAll('circle').interrupt().attr('r', 7);
            }
          }
        });
      },
      hide(t) { App.tr(g, t ? 200 : 0).style('opacity', 0); }
    };
  };

  /* ---------- toggles ---------- */

  const on = {};
  SECTIONS.forEach((id) => { on[id] = false; });
  const announcer = () => document.getElementById('announcer');
  const headerH = () => document.querySelector('.site-header').offsetHeight;

  function readingAnchor() {
    const line = headerH() + (window.innerHeight - headerH()) * 0.3;
    const secs = document.querySelectorAll('main > section');
    for (const sec of secs) {
      if (sec.getBoundingClientRect().bottom > line) return sec.querySelector('.fig-head') || sec;
    }
    return null;
  }

  function apply(id, value, t) {
    on[id] = value;
    const sec = document.getElementById(id);
    const btn = sec.querySelector('.toggle-section');
    if (btn) btn.setAttribute('aria-pressed', String(value));
    if (id === 'hero' || id === 'jembatan') {
      sec.querySelectorAll('.easy-only').forEach((el) => { el.hidden = !value; });
      sec.querySelectorAll('.normal-only').forEach((el) => { el.hidden = value; });
      return;
    }
    const fig = App.figs[id];
    sec.classList.toggle('is-easy', value);
    sec.querySelector('.easy-card').hidden = !value;
    fig.easy = value;
    if (value) fig.svg.attr('aria-labelledby', id + '-easy').attr('aria-describedby', null);
    else fig.svg.attr('aria-labelledby', id + '-alt').attr('aria-describedby', id + '-easy');
    if (fig.w) fig.mod.easy(value, t);
    if (fig.tipsSync) fig.tipsSync();
  }

  // Change sections while keeping the reader's place on screen.
  function change(ids, value, anchorEl, instant) {
    const todo = ids.filter((id) => on[id] !== value);
    if (!todo.length) return;
    const anchor = anchorEl || readingAnchor();
    const before = anchor ? anchor.getBoundingClientRect().top : 0;
    const t = instant ? 0 : App.dur(650);
    todo.forEach((id) => apply(id, value, t));
    if (anchor) {
      const want = Math.max(before, headerH() + 12);
      window.scrollBy(0, anchor.getBoundingClientRect().top - want);
    }
    App.resizeScrollers();
    if (App.updateProgress) App.updateProgress();
    syncGlobal();
  }

  function syncGlobal() {
    const vals = SECTIONS.map((id) => on[id]);
    const state = vals.every(Boolean) ? 'true' : vals.some(Boolean) ? 'mixed' : 'false';
    document.getElementById('easy-global').setAttribute('aria-pressed', state);
  }

  function store(value) {
    try { window.localStorage.setItem(STORE_KEY, value ? '1' : '0'); } catch (e) { /* storage unavailable */ }
  }

  App.easy = {
    isOn: (id) => on[id],
    init() {
      document.querySelectorAll('.toggle-section').forEach((btn) => {
        const sec = btn.closest('section');
        btn.addEventListener('click', () => {
          const value = !on[sec.id];
          change([sec.id], value, btn);
          const n = sec.dataset.n;
          if (n) {
            const tpl = value ? 'Gambar {n} sekarang dalam versi mudah' : 'Gambar {n} sekarang dalam versi grafik';
            announcer().textContent = tpl.replace('{n}', n);
          }
        });
      });
      const global = document.getElementById('easy-global');
      global.addEventListener('click', () => {
        const value = !SECTIONS.every((id) => on[id]);
        change(SECTIONS, value, null);
        store(value);
      });
      let saved = null;
      try { saved = window.localStorage.getItem(STORE_KEY); } catch (e) { saved = null; }
      if (saved === '1') change(SECTIONS, true, null, true);
      syncGlobal();
    }
  };
})();
