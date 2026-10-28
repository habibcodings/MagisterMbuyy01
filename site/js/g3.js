/* G3: magnitude distribution per year, 2014–2017 vs 2022–2025, with the "Hanya MLv" control. Spec 04 §5 G3. */
App.define('g3', function (ctx) {
  const { svg, fig } = ctx;
  const C = App.C;
  const d = ctx.data.f3;
  const control = document.getElementById('g3-control');
  const radios = Array.from(control.querySelectorAll('input'));
  // y range per mode: the MLv 2025 curve peaks at 1.023 per year, above the 0–700 axis of the "Semua" view
  const YMAX = { all: 700, mlv: 1100 };
  const TEXT = {
    all: { a: '2014–2017', b: '2022–2025', arrow: 'Puncak bergeser: M3,4 → M3,0' },
    mlv: { a: '2014–2017 (MLv)', b: '2025 (MLv)', arrow: 'Puncak bergeser: M3,4 → M2,7' }
  };
  let mode = 'all';
  let x, y, W, ml, mr, mt, mb, gBack, gGrid, gFront, tints, lineA, lineB, clipA, clipB, labA, labB, arrow, arrowText, rule, seeds, block;

  const series = (m) => (m === 'mlv' ? d.mlv : d.all);
  const lineGen = () => d3.line().x((p) => x(p.m)).y((p) => y(p.per_year));
  const valAt = (arr, m) => arr.find((p) => Math.abs(p.m - m) < 1e-6).per_year;
  const peak = (arr) => arr.reduce((a, b) => (b.per_year > a.per_year ? b : a));
  const halo = (sel) => sel.attr('stroke', '#fff').attr('stroke-width', 4).attr('paint-order', 'stroke');

  function draw(w, h) {
    W = w; ml = 44; mr = 14; mt = 22; mb = 40;
    x = d3.scaleLinear().domain([1, 6]).range([ml, w - mr]);
    y = d3.scaleLinear().domain([0, YMAX[mode]]).range([h - mb, mt]);
    const defs = svg.append('defs');
    clipA = defs.append('clipPath').attr('id', 'g3-clip-a').append('rect').attr('x', 0).attr('y', 0).attr('height', h).attr('width', 0);
    clipB = defs.append('clipPath').attr('id', 'g3-clip-b').append('rect').attr('x', 0).attr('y', 0).attr('height', h).attr('width', 0);
    defs.append('marker').attr('id', 'g3-arrowhead').attr('viewBox', '0 0 10 10').attr('refX', 8).attr('refY', 5)
      .attr('markerWidth', 7).attr('markerHeight', 7).attr('orient', 'auto-start-reverse')
      .append('path').attr('d', 'M0,0L10,5L0,10z').attr('fill', C.text);

    // back layer: tints, grid, axes
    gBack = svg.append('g');
    tints = gBack.append('g').style('opacity', 0);
    tints.append('rect').attr('x', x(1)).attr('width', x(4) - x(1)).attr('y', mt).attr('height', h - mb - mt).attr('fill', C.small35);
    tints.append('rect').attr('x', x(4)).attr('width', x(6) - x(4)).attr('y', mt).attr('height', h - mb - mt).attr('fill', C.strongTint);
    gGrid = gBack.append('g');
    drawGrid();
    App.axisTitle(gBack, 'Gempa per tahun', 0, 12);
    d3.range(1, 7).forEach((m) => gBack.append('text').attr('x', x(m)).attr('y', h - mb + 16).attr('text-anchor', 'middle')
      .style('font-size', '12px').attr('fill', C.muted).text(App.mag(m)));
    gBack.append('text').attr('x', (ml + w - mr) / 2).attr('y', h - 4).attr('text-anchor', 'middle')
      .style('font-size', '12px').style('font-weight', 700).attr('fill', C.label).text('Magnitudo');

    // lines (drawn left to right through a growing clip rect)
    lineA = svg.append('path').attr('fill', 'none').attr('stroke', C.muted).attr('stroke-width', 1.5).attr('stroke-dasharray', '5 4')
      .attr('clip-path', 'url(#g3-clip-a)');
    lineB = svg.append('path').attr('fill', 'none').attr('stroke', C.dark).attr('stroke-width', 2.5).attr('clip-path', 'url(#g3-clip-b)');

    // front layer: region labels, line labels, peak arrow, tooltip rule
    gFront = svg.append('g');
    const regions = gFront.append('g').attr('class', 'regions').style('opacity', 0);
    halo(App.label(regions, 'Di bawah M4: kini jauh lebih banyak yang “terdengar”', x(1) + 8, mt + 6, { maxW: Math.max(110, x(2.45) - x(1)), fill: C.label, size: 13 }));
    halo(App.label(regions, 'M4+: kedua garis berdekatan', x(4) + 8, y(330), { maxW: x(6) - x(4) - 14, fill: C.strong, size: 13, valign: 'bottom' }));
    tints.node().__regions = regions;
    rule = gFront.append('line').attr('y1', mt).attr('y2', h - mb).attr('stroke', C.text).attr('stroke-width', 1).style('opacity', 0);
    labA = halo(gFront.append('text').style('font-size', '13px').style('font-weight', 700).attr('fill', C.muted));
    labB = halo(gFront.append('text').style('font-size', '13px').style('font-weight', 800).attr('fill', C.dark));
    arrow = gFront.append('path').attr('fill', 'none').attr('stroke', C.text).attr('stroke-width', 1.4).attr('marker-end', 'url(#g3-arrowhead)');
    arrowText = halo(gFront.append('text').style('font-size', '13px').style('font-weight', 800).attr('fill', C.text));
    placeMode(0);

    // easy mode: compare block (per year at M3,0) and two seeds that grow into its bars
    block = App.block(svg, w, h, { type: 'compare', tone: 'small', rows: [{ label: '2014–2017', value: d.at_3_0[0] }, { label: '2022–2025', value: d.at_3_0[1] }] });
    seeds = svg.append('g').selectAll('rect').data([0, 1]).join('rect').attr('fill', C.small).style('opacity', 0);
  }

  function drawGrid() {
    gGrid.selectAll('*').remove();
    App.yGrid(gGrid, y, ml, W - mr, d3.range(0, YMAX[mode] + 1, 100));
  }

  // Lines, labels and the peak arrow for the current mode.
  function placeMode(t) {
    const s = series(mode), T = TEXT[mode];
    App.tr(lineA, t).attr('d', lineGen()(s.A));
    App.tr(lineB, t).attr('d', lineGen()(s.B));
    const pa = peak(s.A), pb = peak(s.B);
    // B label sits left of its rising side, below the region label in the top-left corner
    const rise = s.B.find((p) => p.m < pb.m && p.per_year >= 0.6 * pb.per_year) || pb;
    App.tr(labB, t).attr('x', x(rise.m) - 8).attr('y', y(rise.per_year)).attr('dy', '0.35em').attr('text-anchor', 'end');
    labB.text(T.b);
    // A label below its own curve on the descending side, where the other curve is well above it
    App.tr(labA, t).attr('x', x(3.6)).attr('y', y(valAt(s.A, 3.6)) + 18).attr('text-anchor', 'middle');
    labA.text(T.a);
    const x0 = x(pa.m) + 4, y0 = y(pa.per_year) - 6, x1 = x(pb.m) + 7, y1 = y(pb.per_year) + 2;
    App.tr(arrow, t).attr('d', `M${x0},${y0}Q${x(pa.m + 0.45)},${(y0 + y1) / 2} ${x1},${y1}`);
    App.tr(arrowText, t).attr('x', x(pa.m + 0.4)).attr('y', (y0 + y1) / 2 - 4);
    arrowText.text(T.arrow);
  }

  function setMode(m, t) {
    if (m === mode) return;
    mode = m;
    radios.forEach((r) => { r.checked = r.value === m; });
    y.domain([0, YMAX[m]]);
    drawGrid();
    gGrid.style('opacity', 0);
    App.tr(gGrid, t).style('opacity', 1);
    placeMode(t);
  }

  radios.forEach((r) => r.addEventListener('change', () => { if (r.checked) setMode(r.value, App.dur(500)); }));

  function state(s, t) {
    if (s < 3) setMode('all', t);
    App.tr(gBack, t).style('opacity', 1);
    App.tr(gFront, t).style('opacity', 1);
    block.hide(0);
    lineA.style('opacity', 1);
    lineB.style('opacity', 1);
    App.tr(clipA, t ? 600 : 0).attr('width', W);
    App.tr(clipB, t ? 600 : 0).attr('width', s >= 1 ? W : 0);
    App.tr(labB, t, s >= 1 && t ? 400 : 0).style('opacity', s >= 1 ? 1 : 0);
    App.tr(arrow, t, s >= 1 && t ? 500 : 0).style('opacity', s >= 1 ? 1 : 0);
    App.tr(arrowText, t, s >= 1 && t ? 500 : 0).style('opacity', s >= 1 ? 1 : 0);
    App.tr(tints, t).style('opacity', s >= 2 ? 1 : 0);
    App.tr(tints.node().__regions, t).style('opacity', s >= 2 ? 1 : 0);
    control.classList.toggle('is-off', s < 3);
    radios.forEach((r) => { r.disabled = s < 3; });
  }

  // Morph: both curves collapse onto their M3,0 points, which grow into the two compare bars.
  function easy(on, t) {
    const s = series(mode);
    const targets = [s.A, s.B].map((arr) => ({ x: x(3), y: y(valAt(arr, 3)) }));
    const bars = block.geo.bars;
    function collapse(path, arr, tgt, from, to, dur) {
      const pts = arr.map((p) => [x(p.m), y(p.per_year)]);
      const gen = (k) => 'M' + pts.map(([px, py]) => `${px + (tgt.x - px) * k},${py + (tgt.y - py) * k}`).join('L');
      path.interrupt().attr('d', gen(from));
      if (dur) path.transition().duration(dur).ease(d3.easeCubicInOut).attrTween('d', () => (u) => gen(from + (to - from) * u));
      else path.attr('d', gen(to));
    }
    if (on) {
      App.tr(gBack, t * 0.4).style('opacity', 0);
      App.tr(gFront, t * 0.4).style('opacity', 0);
      collapse(lineA, s.A, targets[0], 0, 1, t * 0.6);
      collapse(lineB, s.B, targets[1], 0, 1, t * 0.6);
      App.tr(lineA, t * 0.25, t * 0.6).style('opacity', 0);
      App.tr(lineB, t * 0.25, t * 0.6).style('opacity', 0);
      seeds.interrupt().attr('x', (i) => targets[i].x - 4).attr('y', (i) => targets[i].y - 4).attr('width', 8).attr('height', 8).attr('rx', 4)
        .style('opacity', t ? 0 : 1);
      App.tr(seeds, t * 0.5, t * 0.5).style('opacity', 1)
        .attr('x', (i) => bars[i].x).attr('y', (i) => bars[i].y).attr('width', (i) => bars[i].w).attr('height', (i) => bars[i].h).attr('rx', bars[0].h / 2);
      block.show(t, t);
    } else {
      block.hide(t);
      App.tr(seeds, t * 0.5).attr('x', (i) => targets[i].x - 4).attr('y', (i) => targets[i].y - 4).attr('width', 8).attr('height', 8).style('opacity', 0);
      state(fig.state, 0);
      if (t) {
        gBack.style('opacity', 0); gFront.style('opacity', 0);
        App.tr(gBack, t * 0.6, t * 0.4).style('opacity', 1);
        App.tr(gFront, t * 0.6, t * 0.4).style('opacity', 1);
        collapse(lineA, series(mode).A, targets[0], 1, 0, t * 0.7);
        collapse(lineB, series(mode).B, targets[1], 1, 0, t * 0.7);
      }
    }
  }

  function tips() {
    const s = series(mode), T = TEXT[mode];
    const showB = fig.state >= 1;
    return s.A.map((p, i) => {
      const b = s.B[i];
      return {
        x: x(p.m), y: y(Math.max(p.per_year, showB ? b.per_year : 0)), xOnly: true,
        text: `M${App.mag(p.m)} · ${App.dec(p.per_year)} per tahun (${T.a}) · ${App.dec(b.per_year)} per tahun (${T.b})`
      };
    });
  }

  function highlight(dd) {
    if (!dd) { rule.style('opacity', 0); return; }
    rule.attr('x1', dd.x).attr('x2', dd.x).style('opacity', 0.5);
  }

  return { final: 3, draw, state, easy, tips, highlight };
});
