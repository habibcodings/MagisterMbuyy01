/* GX (appendix, discarded): cumulative BMKG station codes, 2008–2025. Static: no states, no easy mode. */
App.define('gx', function (ctx) {
  const { svg } = ctx;
  const C = App.C;
  const d = ctx.data.fx;

  function draw(w, h) {
    const ml = 46, mr = 64, mt = 24, mb = 24, wide = w >= 520;
    const x = d3.scaleLinear().domain([2008, 2025]).range([ml, w - mr]);
    const y = d3.scaleLinear().domain([0, 1400]).range([h - mb, mt]);
    App.yGrid(svg, y, ml, w - mr, [0, 200, 400, 600, 800, 1000, 1200, 1400]);
    App.axisTitle(svg, 'Kode stasiun (kumulatif)', 0, 12);
    d3.range(2008, 2026, wide ? 2 : 4).forEach((yr) => svg.append('text').attr('x', x(yr)).attr('y', h - mb + 15).attr('text-anchor', 'middle')
      .style('font-size', '12px').attr('fill', C.muted).text(yr));
    svg.append('path').attr('fill', 'none').attr('stroke', C.neutral).attr('stroke-width', 2.2)
      .attr('d', d3.line().curve(d3.curveStepAfter).x((r) => x(r.year)).y((r) => y(r.codes))(d.years));
    const p17 = d.years.find((r) => r.year === 2017), p25 = d.years.find((r) => r.year === 2025);
    [p17, p25].forEach((p) => svg.append('circle').attr('cx', x(p.year)).attr('cy', y(p.codes)).attr('r', 4.5).attr('fill', C.neutral));
    const halo = (sel) => sel.attr('stroke', '#fff').attr('stroke-width', 4).attr('paint-order', 'stroke');
    halo(App.label(svg, '2017: 369', x(2017) - 6, y(p17.codes) - 10, { anchor: 'end', valign: 'bottom', fill: C.neutral }));
    halo(App.label(svg, '2025: 1.314', x(2025) - 6, y(p25.codes) - 10, { anchor: 'end', valign: 'bottom', fill: C.neutral }));
    // ×3,6 bracket from the 2017 level to the 2025 level, right of the line
    const bx = x(2025) + 14;
    svg.append('line').attr('x1', x(2017)).attr('x2', bx).attr('y1', y(p17.codes)).attr('y2', y(p17.codes))
      .attr('stroke', '#9CA3AF').attr('stroke-width', 1.2).attr('stroke-dasharray', '3 3');
    svg.append('path').attr('fill', 'none').attr('stroke', C.neutral).attr('stroke-width', 1.8)
      .attr('d', `M${bx - 5},${y(p17.codes)}H${bx}V${y(p25.codes)}H${bx - 5}`);
    svg.append('text').attr('x', bx + 6).attr('y', (y(p17.codes) + y(p25.codes)) / 2).attr('dy', '0.35em')
      .style('font-size', '17px').style('font-weight', 800).attr('fill', C.neutral).text('×3,6');
  }

  return { final: 0, draw, state() {}, easy() {} };
});
