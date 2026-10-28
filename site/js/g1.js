/* G1: BMKG release totals (top) and M5+ (bottom), two aligned column panels. Spec 04 §5 G1. */
App.define('g1', function (ctx) {
  const { svg, fig } = ctx;
  const C = App.C;
  const d = ctx.data.f1;
  const years = d.years.map((r) => r.year);
  const row = (y) => d.years.find((r) => r.year === y);
  let x, yT, yB, bw, gTop, gBotAxes, gBars, topBars, topVals, botBars, botVals, alt, bracket, guess, arrowLabel, block;

  function draw(w, h) {
    const ml = 48, mr = 62, head = 22, xlab = 20, gap = 24, top = 4;
    const avail = h - top - 2 * head - 2 * xlab - gap - 2;
    const hTop = Math.max(90, avail * 0.7), hBot = Math.max(50, avail - hTop);
    const t0 = top + head, t1 = t0 + hTop;            // top panel plot area
    const b0 = t1 + xlab + gap + head, b1 = b0 + hBot; // bottom panel plot area
    x = d3.scaleBand().domain(years).range([ml, w - mr]).paddingInner(0.3).paddingOuter(0.15);
    bw = x.bandwidth();
    const vfs = Math.max(9.5, Math.min(12.5, x.step() / 3.5));   // value labels shrink on narrow screens
    yT = d3.scaleLinear().domain([0, 45000]).range([t1, t0]);
    yB = d3.scaleLinear().domain([0, 300]).range([b1, b0]);

    // top panel: all quakes (neutral)
    gTop = svg.append('g').attr('class', 'top');
    gTop.append('text').attr('class', 'panel-title').attr('x', 0).attr('y', top + 13).text('Semua gempa')
      .append('tspan').attr('class', 'axis-title').attr('dx', 10).style('font-weight', 600).attr('fill', C.muted).text('Gempa per tahun');
    App.yGrid(gTop, yT, ml, w - mr, [0, 10000, 20000, 30000, 40000]);
    years.forEach((yr) => gTop.append('text').attr('x', x(yr) + bw / 2).attr('y', t1 + 15).attr('text-anchor', 'middle')
      .style('font-size', '12px').attr('fill', C.muted).text(yr));
    // dashed reference at the 2020 level and the ×5,3 bracket right of 2025
    const v20 = row(2020).total, v25 = row(2025).total, bx = x(2025) + bw + 12;
    bracket = gTop.append('g').attr('class', 'bracket');
    bracket.append('line').attr('x1', x(2020)).attr('x2', bx).attr('y1', yT(v20)).attr('y2', yT(v20))
      .attr('stroke', '#9CA3AF').attr('stroke-width', 1.2).attr('stroke-dasharray', '3 3');
    bracket.append('path').attr('class', 'bk').attr('fill', 'none').attr('stroke', C.neutral).attr('stroke-width', 1.8)
      .attr('d', `M${bx - 5},${yT(v20)}H${bx}V${yT(v25)}H${bx - 5}`);
    bracket.append('text').attr('x', bx + 6).attr('y', (yT(v20) + yT(v25)) / 2).attr('dy', '0.35em')
      .style('font-size', '17px').style('font-weight', 800).attr('fill', C.neutral).text('×5,3');

    const gTopBars = gTop.append('g');
    topBars = gTopBars.selectAll('rect').data(d.years).join('rect')
      .attr('x', (r) => x(r.year)).attr('width', bw).attr('y', t1).attr('height', 0).attr('fill', C.neutral);
    topVals = gTop.append('g').selectAll('text').data(d.years).join('text').attr('class', 'val').style('font-size', vfs + 'px')
      .attr('x', (r) => x(r.year) + bw / 2).attr('y', (r) => yT(r.total) - 6).attr('text-anchor', 'middle')
      .attr('fill', C.text).style('opacity', 0).text((r) => App.fmt(r.total));
    bracket.raise();

    // 2024: second total (hollow marker with leader label)
    const r24 = row(2024), cx = x(2024) + bw / 2, cy = yT(r24.total_alt);
    alt = gTop.append('g').attr('class', 'alt').style('opacity', 0);
    const lx = x(2024) - 14, ly = yT(25000);
    const lab = App.label(alt, '7.358 (angka akhir tahun, 31 Des 2024)', lx, ly, { anchor: 'end', maxW: Math.max(110, lx - ml - 10), fill: C.neutral, valign: 'bottom' });
    // leader drawn twice: a white casing keeps it visible where it crosses the dark 2024 column
    const leader = `M${lx + 4},${ly - 4}L${cx - 7},${cy - 5}`;
    alt.append('path').attr('fill', 'none').attr('stroke', '#fff').attr('stroke-width', 3.5).attr('d', leader);
    alt.append('path').attr('fill', 'none').attr('stroke', C.neutral).attr('stroke-width', 1.2).attr('d', leader);
    alt.append('circle').attr('cx', cx).attr('cy', cy).attr('r', 6).attr('fill', '#fff').attr('stroke', C.neutral).attr('stroke-width', 2.2);
    lab.raise();

    // bottom panel: M5+ (strong)
    gBotAxes = svg.append('g').attr('class', 'bot-axes').style('opacity', 0);
    gBotAxes.append('text').attr('class', 'panel-title').attr('x', 0).attr('y', b0 - head + 13).text('Gempa M5+')
      .append('tspan').attr('class', 'axis-title').attr('dx', 10).style('font-weight', 600).attr('fill', C.muted).text('Gempa per tahun');
    App.yGrid(gBotAxes, yB, ml, w - mr, [0, 100, 200, 300]);
    years.forEach((yr) => gBotAxes.append('text').attr('x', x(yr) + bw / 2).attr('y', b1 + 15).attr('text-anchor', 'middle')
      .style('font-size', '12px').attr('fill', C.muted).text(yr));
    guess = gBotAxes.append('text').attr('x', (ml + w - mr) / 2).attr('y', (b0 + b1) / 2).attr('dy', '0.35em').attr('text-anchor', 'middle')
      .style('font-size', Math.min(44, hBot * 0.8) + 'px').style('font-weight', 800).attr('fill', '#9CA3AF').style('opacity', 0).text('?');
    gBars = svg.append('g').attr('class', 'bot-bars');
    botBars = gBars.selectAll('rect').data(d.years).join('rect')
      .attr('x', (r) => x(r.year)).attr('width', bw).attr('y', b1).attr('height', 0).attr('fill', C.strong);
    botVals = gBotAxes.append('g').selectAll('text').data(d.years).join('text').attr('class', 'val').style('font-size', vfs + 'px')
      .attr('x', (r) => x(r.year) + bw / 2).attr('y', (r) => yB(r.m5plus) - 5).attr('text-anchor', 'middle')
      .attr('fill', C.strong).style('opacity', 0).text((r) => App.fmt(r.m5plus));
    arrowLabel = gBotAxes.append('text').attr('x', w - mr).attr('y', b0 - head + 14).attr('text-anchor', 'end')
      .style('font-size', '15px').style('font-weight', 800).attr('fill', C.strong).style('opacity', 0).text('244 → 153');

    block = App.block(svg, w, h, { type: 'compare', tone: 'strong', rows: [{ label: '2020', value: d.m5_2020 }, { label: '2025', value: d.m5_2025 }] });
  }

  function state(s, t) {
    const answered = !!App.guess.g1;
    const S = s === 3 && answered ? 4 : s;   // once answered, the guess state shows the answer
    App.tr(gTop, t).style('opacity', 1);
    block.hide(0);
    // top columns
    App.tr(topBars, t, (r, i) => (S >= 1 && t ? i * 80 : 0))
      .attr('x', (r) => x(r.year)).attr('width', bw).attr('rx', 0)
      .attr('y', (r) => (S >= 1 || r.year === 2020 ? yT(r.total) : yT(0)))
      .attr('height', (r) => (S >= 1 || r.year === 2020 ? yT(0) - yT(r.total) : 0))
      .style('opacity', (r) => ((S === 2 || S === 3) && r.year !== 2024 ? 0.35 : 1));
    App.tr(topVals, t, (r, i) => (S >= 1 && t ? 200 + i * 80 : 0))
      .style('opacity', (r) => (S >= 1 || r.year === 2020 ? ((S === 2 || S === 3) && r.year !== 2024 ? 0.35 : 1) : 0));
    App.tr(bracket, t, S >= 1 && t ? 400 : 0).style('opacity', S >= 1 ? 1 : 0);
    App.tr(alt, t).style('opacity', S >= 2 ? 1 : 0);
    // bottom panel
    App.tr(gBotAxes, t).style('opacity', S >= 3 ? 1 : 0);
    App.tr(guess, t).style('opacity', S === 3 ? 1 : 0);
    App.tr(botBars, t, (r, i) => (S >= 4 && t ? i * 80 : 0))
      .attr('x', (r) => x(r.year)).attr('width', bw).attr('rx', 0).style('opacity', 1).attr('fill', C.strong)
      .attr('y', (r) => (S >= 4 ? yB(r.m5plus) : yB(0)))
      .attr('height', (r) => (S >= 4 ? yB(0) - yB(r.m5plus) : 0));
    App.tr(botVals, t, (r, i) => (S >= 4 && t ? 250 + i * 80 : 0)).style('opacity', S >= 4 ? 1 : 0);
    App.tr(arrowLabel, t, S >= 4 && t ? 500 : 0).style('opacity', S >= 4 ? 1 : 0);
  }

  // Morph: the 2020 and 2025 M5+ columns travel and turn into the two compare bars.
  function easy(on, t) {
    if (on) {
      const bars = block.geo.bars;
      App.tr(gTop, t * 0.4).style('opacity', 0);
      App.tr(gBotAxes, t * 0.4).style('opacity', 0);
      App.tr(botBars, t, t * 0.15)
        .style('opacity', (r) => (r.year === 2020 || r.year === 2025 ? 1 : 0))
        .attr('x', (r) => (r.year === 2020 ? bars[0].x : r.year === 2025 ? bars[1].x : x(r.year)))
        .attr('y', (r) => (r.year === 2020 ? bars[0].y : r.year === 2025 ? bars[1].y : yB(r.m5plus)))
        .attr('width', (r) => (r.year === 2020 ? bars[0].w : r.year === 2025 ? bars[1].w : bw))
        .attr('height', (r) => (r.year === 2020 ? bars[0].h : r.year === 2025 ? bars[1].h : yB(0) - yB(r.m5plus)))
        .attr('rx', (r) => (r.year === 2020 || r.year === 2025 ? bars[0].h / 2 : 0));
      block.show(t, t ? t * 0.85 : 0);
    } else {
      block.hide(t);
      state(fig.state, t);
    }
  }

  function tips() {
    const s = fig.state, answered = !!App.guess.g1;
    const S = s === 3 && answered ? 4 : s;
    const out = [];
    d.years.forEach((r) => {
      if (S >= 1 || r.year === 2020) out.push({ x: x(r.year) + bw / 2, y: yT(r.total), text: `${r.year}: ${App.fmt(r.total)} gempa` });
    });
    if (S >= 2) out.splice(5, 0, { x: x(2024) + bw / 2, y: yT(row(2024).total_alt), text: `2024: ${App.fmt(row(2024).total_alt)} gempa` });
    if (S >= 4) d.years.forEach((r) => out.push({ x: x(r.year) + bw / 2, y: yB(r.m5plus), text: `${r.year}: ${App.fmt(r.m5plus)} gempa` }));
    return out;
  }

  return { final: 4, draw, state, easy, tips };
});
