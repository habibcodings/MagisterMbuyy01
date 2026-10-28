/* G4: median phase readings for M4,0–4,9 quakes, with the IQR ribbon. Spec 04 §5 G4. */
App.define('g4', function (ctx) {
  const { svg, fig } = ctx;
  const C = App.C;
  const d = ctx.data.f4;
  // y range: the upper quartile reaches 75 (2024), so the axis runs to 80 instead of 60 to avoid clipping the ribbon
  const YMAX = 80;
  let x, y, W, gBack, gFront, gLine, clip, ribbon, line, pts, emph, periodLabels, seeds, block;
  const halo = (sel) => sel.attr('stroke', '#fff').attr('stroke-width', 4).attr('paint-order', 'stroke');

  function draw(w, h) {
    W = w;
    const ml = 36, mr = 14, mt = 22, mb = 24;
    x = d3.scaleLinear().domain([2008.5, 2025.5]).range([ml, w - mr]);
    y = d3.scaleLinear().domain([0, YMAX]).range([h - mb, mt]);
    const wide = w >= 520;
    clip = svg.append('defs').append('clipPath').attr('id', 'g4-clip').append('rect').attr('x', 0).attr('y', 0).attr('height', h).attr('width', 0);

    gBack = svg.append('g');
    const bands = [[2014, 2017, `2014–2017: median ${App.fmt(d.median_A)}`], [2022, 2025, `2022–2025: median ${App.fmt(d.median_B)}`]];
    bands.forEach(([a, b]) => gBack.append('rect').attr('x', x(a - 0.45)).attr('width', x(b + 0.45) - x(a - 0.45))
      .attr('y', mt).attr('height', h - mb - mt).attr('fill', C.neutral8));
    App.yGrid(gBack, y, ml, w - mr, [0, 20, 40, 60, 80]);
    App.axisTitle(gBack, 'Bacaan fase (median)', 0, 12);
    d.years.forEach((r, i) => {
      if (!wide && i % 2) return;
      gBack.append('text').attr('x', x(r.year)).attr('y', h - mb + 15).attr('text-anchor', 'middle')
        .style('font-size', '12px').attr('fill', C.muted).text(r.year);
    });

    gLine = svg.append('g').attr('clip-path', 'url(#g4-clip)');
    ribbon = gLine.append('path').attr('fill', C.neutral).attr('fill-opacity', 0.15)
      .attr('d', d3.area().x((r) => x(r.year)).y0((r) => y(r.q1)).y1((r) => y(r.q3))(d.years));
    line = gLine.append('path').attr('fill', 'none').attr('stroke', C.neutral).attr('stroke-width', 2.5)
      .attr('d', d3.line().x((r) => x(r.year)).y((r) => y(r.median))(d.years));
    emph = svg.append('path').attr('fill', 'none').attr('stroke', C.neutral).attr('stroke-width', 6).attr('stroke-linecap', 'round').style('opacity', 0)
      .attr('d', d3.line().x((r) => x(r.year)).y((r) => y(r.median))(d.years.filter((r) => r.year >= 2019 && r.year <= 2022)));
    pts = gLine.append('g').selectAll('circle').data(d.years).join('circle')
      .attr('cx', (r) => x(r.year)).attr('cy', (r) => y(r.median)).attr('r', 3.5).attr('fill', C.neutral);

    gFront = svg.append('g');
    // ribbon label with a leader into the ribbon (2010)
    const r10 = d.years.find((r) => r.year === 2010);
    const lx = x(2009) - 6, ly = y(44);
    const lab = halo(App.label(gFront, 'Separuh gempa berada di dalam pita ini', lx, ly, { maxW: Math.max(120, x(2013.4) - lx), fill: C.neutral, size: 13, valign: 'bottom' }));
    gFront.append('path').attr('fill', 'none').attr('stroke', C.neutral).attr('stroke-width', 1.2)
      .attr('d', `M${x(2010)},${ly + 4}V${y((r10.q1 + r10.q3) / 2)}`);
    lab.raise();
    periodLabels = gFront.append('g').style('opacity', 0);
    bands.forEach(([a, b, text]) => halo(App.label(periodLabels, text, x((a + b) / 2), y(1), {
      anchor: 'middle', valign: 'bottom', maxW: Math.max(70, x(b + 0.45) - x(a - 0.45) - 6), fill: C.neutral, size: 13, weight: 800
    })));

    block = App.block(svg, w, h, { type: 'compare', tone: 'neutral', rows: [{ label: '2014–2017', value: d.median_A }, { label: '2022–2025', value: d.median_B }] });
    seeds = svg.append('g').selectAll('rect').data([0, 1]).join('rect').attr('fill', C.neutral).style('opacity', 0);
  }

  function state(s, t) {
    App.tr(gBack, t).style('opacity', 1);
    App.tr(gFront, t).style('opacity', 1);
    block.hide(0);
    gLine.style('opacity', 1);
    line.style('opacity', 1); ribbon.style('opacity', 1); pts.style('opacity', 1);
    const prev = +clip.attr('width');
    const wTarget = s >= 1 ? W : x(2019.3);
    App.tr(clip, t ? 700 : 0).attr('width', wTarget);
    // emphasize the 2019–2022 jump for one beat when it is first drawn
    emph.interrupt().style('opacity', 0);
    if (s === 1 && t && prev < W - 1) {
      emph.style('opacity', 0).transition().delay(500).duration(250).style('opacity', 0.9)
        .transition().delay(700).duration(500).style('opacity', 0);
    }
    App.tr(periodLabels, t).style('opacity', s >= 2 ? 1 : 0);
  }

  // Morph: the line contracts onto its two period medians, which become the compare bars.
  function easy(on, t) {
    const A = { x: x(2015.5), y: y(d.median_A) }, B = { x: x(2023.5), y: y(d.median_B) };
    const pts0 = d.years.map((r) => [x(r.year), y(r.median)]);
    const tgt = d.years.map((r) => (r.year <= 2018 ? A : B));
    const gen = (k) => 'M' + pts0.map(([px, py], i) => `${px + (tgt[i].x - px) * k},${py + (tgt[i].y - py) * k}`).join('L');
    const bars = block.geo.bars, starts = [A, B];
    const run = (from, to, dur) => {
      line.interrupt().attr('d', gen(from));
      if (dur) line.transition().duration(dur).ease(d3.easeCubicInOut).attrTween('d', () => (u) => gen(from + (to - from) * u));
      else line.attr('d', gen(to));
    };
    if (on) {
      clip.interrupt().attr('width', W);
      App.tr(gBack, t * 0.4).style('opacity', 0);
      App.tr(gFront, t * 0.4).style('opacity', 0);
      App.tr(ribbon, t * 0.4).style('opacity', 0);
      App.tr(pts, t * 0.3).style('opacity', 0);
      run(0, 1, t * 0.6);
      App.tr(line, t * 0.25, t * 0.6).style('opacity', 0);
      seeds.interrupt().attr('x', (i) => starts[i].x - 4).attr('y', (i) => starts[i].y - 4).attr('width', 8).attr('height', 8).attr('rx', 4)
        .style('opacity', t ? 0 : 1);
      App.tr(seeds, t * 0.5, t * 0.5).style('opacity', 1)
        .attr('x', (i) => bars[i].x).attr('y', (i) => bars[i].y).attr('width', (i) => bars[i].w).attr('height', (i) => bars[i].h).attr('rx', bars[0].h / 2);
      block.show(t, t);
    } else {
      block.hide(t);
      App.tr(seeds, t * 0.5).attr('x', (i) => starts[i].x - 4).attr('y', (i) => starts[i].y - 4).attr('width', 8).attr('height', 8).style('opacity', 0);
      state(fig.state, 0);
      if (t) {
        [gBack, gFront, ribbon, pts].forEach((sel) => { sel.style('opacity', 0); App.tr(sel, t * 0.6, t * 0.4).style('opacity', 1); });
        run(1, 0, t * 0.7);
      } else {
        run(0, 0, 0);
      }
    }
  }

  function tips() {
    return d.years.filter((r) => fig.state >= 1 || r.year <= 2019).map((r) => ({
      x: x(r.year), y: y(r.q3),
      text: `${r.year} · median ${App.fmt(r.median)} bacaan · separuh gempa: ${App.fmt(r.q1)}–${App.fmt(r.q3)}`
    }));
  }

  return { final: 2, draw, state, easy, tips };
});
