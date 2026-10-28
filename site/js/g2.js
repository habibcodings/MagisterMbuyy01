/* G2: catalog quakes per year, stacked with M4+ at the base. Spec 04 §5 G2. */
App.define('g2', function (ctx) {
  const { svg, fig } = ctx;
  const C = App.C;
  const d = ctx.data.f2;
  const years = d.years.map((r) => r.year);
  let x, y, bw, gChart, m4Bars, belowBars, seams, band, bandTop, segLabels, label25, block, dots, starts;

  function draw(w, h) {
    const wide = w >= 560;
    const ml = 50, mr = wide ? 96 : 10, mt = 34, mb = 22;
    x = d3.scaleBand().domain(years).range([ml, w - mr]).paddingInner(0.25).paddingOuter(0.2);
    bw = x.bandwidth();
    y = d3.scaleLinear().domain([0, 20000]).range([h - mb, mt]);
    const step = x.step();

    gChart = svg.append('g').attr('class', 'chart');
    App.axisTitle(gChart, 'Gempa per tahun', 0, 12);
    // period bands
    [[2014, 2017, '2014–2017'], [2022, 2025, '2022–2025']].forEach(([a, b, lab]) => {
      const x0 = x(a) - step * 0.12, x1 = x(b) + bw + step * 0.12;
      gChart.append('rect').attr('x', x0).attr('y', mt).attr('width', x1 - x0).attr('height', h - mb - mt).attr('fill', C.neutral8);
      gChart.append('text').attr('x', (x0 + x1) / 2).attr('y', mt - 6).attr('text-anchor', 'middle')
        .style('font-size', '12px').style('font-weight', 700).attr('fill', C.label).text(lab);
    });
    App.yGrid(gChart, y, ml, w - mr, [0, 5000, 10000, 15000, 20000]);
    years.forEach((yr, i) => {
      if (step < 38 && i % 2) return;
      gChart.append('text').attr('x', x(yr) + bw / 2).attr('y', h - mb + 15).attr('text-anchor', 'middle')
        .style('font-size', '12px').attr('fill', C.muted).text(yr);
    });
    // M4+ range band (behind the columns, visible in the gaps) with boundary lines on top
    const mn = d.m4plus_min.value, mx = d.m4plus_max.value;
    band = gChart.append('g').style('opacity', 0);
    band.append('rect').attr('x', ml).attr('width', w - mr - ml).attr('y', y(mx)).attr('height', y(mn) - y(mx)).attr('fill', C.strong20);

    m4Bars = gChart.append('g').selectAll('rect').data(d.years).join('rect').attr('x', (r) => x(r.year)).attr('width', bw);
    belowBars = gChart.append('g').selectAll('rect').data(d.years).join('rect').attr('x', (r) => x(r.year)).attr('width', bw);
    seams = gChart.append('g').selectAll('line').data(d.years).join('line')
      .attr('x1', (r) => x(r.year)).attr('x2', (r) => x(r.year) + bw).attr('y1', (r) => y(r.m4plus)).attr('y2', (r) => y(r.m4plus))
      .attr('stroke', '#fff').attr('stroke-width', 1);

    bandTop = gChart.append('g').style('opacity', 0);
    [mn, mx].forEach((v) => bandTop.append('line').attr('x1', ml).attr('x2', w - mr).attr('y1', y(v)).attr('y2', y(v))
      .attr('stroke', C.strong).attr('stroke-width', 1.2).attr('stroke-dasharray', '4 3'));
    App.label(bandTop, 'M4+: 1.755–3.042 per tahun sejak 2009', ml + 4, y(mx) - 6, { valign: 'bottom', fill: C.strong, maxW: w - mr - ml - 8 })
      .attr('stroke', '#fff').attr('stroke-width', 4).attr('paint-order', 'stroke');

    // direct segment labels
    segLabels = gChart.append('g').style('opacity', 0);
    const r25 = d.years[d.years.length - 1];
    const sx = wide ? x(2025) + bw + 8 : ml + 4;
    const yM4 = wide ? y(r25.m4plus / 2) : y(15500), yBelow = wide ? y(r25.m4plus + r25.below4 / 2) : y(13000);
    App.label(segLabels, 'M4+', sx, yM4, { valign: 'middle', fill: C.strong }).attr('stroke', '#fff').attr('stroke-width', 4).attr('paint-order', 'stroke');
    App.label(segLabels, 'Di bawah M4', sx, yBelow, { valign: 'middle', fill: C.smallText }).attr('stroke', '#fff').attr('stroke-width', 4).attr('paint-order', 'stroke');

    // 2025 label with a leader line
    label25 = gChart.append('g').style('opacity', 0);
    const lx = x(2025) - 10, ly = y(19000);
    const lab = App.label(label25, '2025: total tertinggi (18.357), tetapi M4+ termasuk yang terendah (1.895)', lx, ly,
      { anchor: 'end', maxW: Math.max(150, (w - mr - ml) * 0.5), fill: C.text })
      .attr('stroke', '#fff').attr('stroke-width', 4).attr('paint-order', 'stroke');
    label25.append('path').attr('fill', 'none').attr('stroke', C.text).attr('stroke-width', 1.2)
      .attr('d', `M${lx + 3},${ly + 9}L${x(2025) - 1},${y(r25.total) + 6}`);
    lab.raise();

    // easy mode: 100 dots that start inside the 2022–2025 columns
    block = App.block(svg, w, h, { type: 'dots', tone: 'strong', caption: '3 dari 100' });
    const rnd = App.rng(2022);
    const pool = d.years.filter((r) => r.year >= 2022);
    starts = d3.range(100).map(() => {
      const r = pool[Math.floor(rnd() * pool.length)];
      return { x: x(r.year) + rnd() * bw, y: y(r.total) + rnd() * (y(0) - y(r.total)) };
    });
    dots = svg.append('g').attr('class', 'dots').selectAll('circle').data(d3.range(100)).join('circle')
      .attr('cx', (i) => starts[i].x).attr('cy', (i) => starts[i].y).attr('r', 0)
      .attr('fill', (i) => (i < 3 ? C.strong : C.small));
  }

  function state(s, t) {
    App.tr(gChart, t).style('opacity', 1);
    block.hide(0);
    const split = s >= 2;
    App.tr(m4Bars, t).attr('y', (r) => y(r.m4plus)).attr('height', (r) => y(0) - y(r.m4plus))
      .attr('fill', split ? C.strong : C.neutral).style('opacity', s === 0 ? 0.3 : 1);
    App.tr(belowBars, t).attr('y', (r) => y(r.total)).attr('height', (r) => y(r.m4plus) - y(r.total))
      .attr('fill', split ? C.small : C.neutral).style('opacity', s === 0 ? 0.3 : 1);
    App.tr(seams, t).style('opacity', split ? 1 : 0);
    App.tr(segLabels, t).style('opacity', split ? 1 : 0);
    App.tr(band, t).style('opacity', s >= 3 ? 1 : 0);
    App.tr(bandTop, t).style('opacity', s >= 3 ? 1 : 0);
    App.tr(label25, t).style('opacity', s >= 4 ? 1 : 0);
  }

  // Morph: 100 dots leave the 2022–2025 columns and settle into a 20 × 5 grid; 3 are strong.
  function easy(on, t) {
    const g = block.geo;
    if (on) {
      App.tr(gChart, t * 0.4).style('opacity', 0);
      dots.interrupt().attr('cx', (i) => starts[i].x).attr('cy', (i) => starts[i].y);
      if (t) {
        dots.attr('r', 2.5).transition().delay((i) => 150 + i * 4).duration(t).ease(d3.easeCubicOut)
          .attr('cx', (i) => g.dots[i].x).attr('cy', (i) => g.dots[i].y).attr('r', g.r);
      } else {
        dots.attr('cx', (i) => g.dots[i].x).attr('cy', (i) => g.dots[i].y).attr('r', g.r);
      }
      block.show(t, t ? t + 500 : 0);
    } else {
      block.hide(t);
      App.tr(dots, t, (i) => i * 2).attr('cx', (i) => starts[i].x).attr('cy', (i) => starts[i].y).attr('r', 0);
      state(fig.state, t);
    }
  }

  function tips() {
    return d.years.map((r) => ({
      x: x(r.year) + bw / 2, y: y(r.total),
      text: `${r.year} · total ${App.fmt(r.total)} · M4+ ${App.fmt(r.m4plus)} · di bawah M4 ${App.fmt(r.below4)}` + (r.scaled ? ' (disetarakan setahun penuh)' : '')
    }));
  }

  return { final: 4, draw, state, easy, tips };
});
