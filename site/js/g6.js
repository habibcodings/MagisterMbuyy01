/* G6: yearly M4+ as a dot strip, with the range band, median and the 2026 pace. Spec 04 §5 G6. */
App.define('g6', function (ctx) {
  const { svg, fig } = ctx;
  const C = App.C;
  const d = ctx.data.f6;
  const R = 7;
  let x, cy, gBack, gRange, dots, pos, diamond, diamondLabel, block;
  const halo = (sel) => sel.attr('stroke', '#fff').attr('stroke-width', 4).attr('paint-order', 'stroke');

  // Vertical jitter only where dots would overlap: try 0, then ±(2R+1), ±2(2R+1) …
  function beeswarm(vals) {
    const placed = [];
    return vals.map((v) => {
      const px = x(v);
      let k = 0, off = 0;
      for (;;) {
        off = k === 0 ? 0 : (k % 2 ? 1 : -1) * Math.ceil(k / 2) * (2 * R + 1);
        if (!placed.some((p) => Math.abs(p.x - px) < 2 * R + 1 && Math.abs(p.off - off) < 2 * R + 1)) break;
        k++;
      }
      placed.push({ x: px, off });
      return { x: px, y: cy + off };
    });
  }

  function draw(w, h) {
    const ml = 18, mr = 18;
    x = d3.scaleLinear().domain([1600, 3200]).range([ml, w - mr]);
    cy = Math.round(h * 0.5);
    const bandH = 64, axisY = h - 40;

    gBack = svg.append('g');
    d3.range(1600, 3201, 200).forEach((v) => {
      gBack.append('line').attr('x1', x(v)).attr('x2', x(v)).attr('y1', 26).attr('y2', axisY)
        .attr('stroke', C.grid).attr('shape-rendering', 'crispEdges');
      gBack.append('text').attr('x', x(v)).attr('y', axisY + 15).attr('text-anchor', 'middle')
        .style('font-size', '12px').attr('fill', C.muted).text(App.fmt(v));
    });
    gBack.append('text').attr('x', (ml + w - mr) / 2).attr('y', axisY + 33).attr('text-anchor', 'middle')
      .style('font-size', '12px').style('font-weight', 700).attr('fill', C.label).text('Gempa M4+ per tahun');

    gRange = svg.append('g').style('opacity', 0);
    const mn = d.min.value, mx = d.max.value;
    gRange.append('rect').attr('x', x(mn)).attr('width', x(mx) - x(mn)).attr('y', cy - bandH / 2).attr('height', bandH).attr('rx', 10).attr('fill', C.small35);
    App.label(gRange, 'Rentang 2009–2025', x(mx) - 10, cy + bandH / 2 - 6, { anchor: 'end', valign: 'bottom', fill: C.label, size: 12 });
    gRange.append('line').attr('x1', x(d.median)).attr('x2', x(d.median)).attr('y1', cy - bandH / 2 - 8).attr('y2', cy + bandH / 2 + 8)
      .attr('stroke', C.muted).attr('stroke-width', 2);
    const medW = Math.min(w - 20, 340);
    const medX = Math.max(10 + medW / 2, Math.min(w - 10 - medW / 2, x(d.median)));
    halo(App.label(gRange, 'Median: 2.159 per tahun ≈ 6 gempa M4+ setiap hari', medX, cy + bandH / 2 + 12, { anchor: 'middle', maxW: medW, fill: C.text, size: 13 }));

    pos = beeswarm(d.years.map((r) => r.m4plus));
    dots = svg.append('g').selectAll('circle').data(d.years).join('circle')
      .attr('cx', (r, i) => pos[i].x).attr('cy', (r, i) => pos[i].y).attr('r', 0).attr('fill', C.strong45);

    // labels for the extremes (shown with the band)
    const iMin = d.years.findIndex((r) => r.year === d.min.year), iMax = d.years.findIndex((r) => r.year === d.max.year);
    // extremes are labelled just above the band, the 2026 pace one tier higher
    halo(App.label(gRange, '2013: 1.755', pos[iMin].x - R, cy - bandH / 2 - 6, { fill: C.text, size: 13, valign: 'bottom' }));
    halo(App.label(gRange, '2019: 3.042', pos[iMax].x + R, cy - bandH / 2 - 6, { anchor: 'end', fill: C.text, size: 13, valign: 'bottom' }));

    // 2026 diamond and label
    const dx = x(d.pace_2026), s = 9;
    diamond = svg.append('path').attr('d', `M${dx},${cy - s}L${dx + s},${cy}L${dx},${cy + s}L${dx - s},${cy}Z`)
      .attr('fill', C.strong).attr('stroke', '#fff').attr('stroke-width', 1.5);
    const lw = App.measure('2026 (s.d. 14 Agu): ±2.430', 14, 800);
    const lx = Math.max(8 + lw / 2, Math.min(w - 8 - lw / 2, dx));
    diamondLabel = svg.append('g');
    halo(App.label(diamondLabel, '2026 (s.d. 14 Agu): ±2.430', lx, cy - bandH / 2 - 32, { anchor: 'middle', fill: C.strong, size: 14, weight: 800, valign: 'bottom' }));
    diamondLabel.append('path').attr('fill', 'none').attr('stroke', C.strong).attr('stroke-width', 1.2)
      .attr('d', `M${dx},${cy - bandH / 2 - 28}V${cy - s - 3}`);

    block = App.block(svg, w, h, { type: 'number', tone: 'strong', value: 6 });
  }

  function state(s, t) {
    App.tr(gBack, t).style('opacity', 1);
    block.hide(0);
    App.tr(dots, t, (_, i) => (t ? i * 25 : 0)).attr('cx', (r, i) => pos[i].x).attr('cy', (r, i) => pos[i].y).attr('r', R).style('opacity', 1);
    App.tr(gRange, t).style('opacity', s >= 1 ? 1 : 0);
    const dropFrom = `translate(0,${-40})`;
    if (s >= 2) {
      const shown = diamond.style('opacity') === '1' && !diamond.attr('transform');
      diamond.interrupt();
      if (t && !shown) {
        diamond.style('opacity', 0).attr('transform', dropFrom)
          .transition().duration(650).ease(d3.easeBounceOut).style('opacity', 1).attr('transform', 'translate(0,0)')
          .on('end', () => diamond.attr('transform', null));
      } else {
        diamond.style('opacity', 1).attr('transform', null);
      }
    } else {
      App.tr(diamond, t).style('opacity', 0).attr('transform', dropFrom);
    }
    App.tr(diamondLabel, t, s >= 2 && t ? 350 : 0).style('opacity', s >= 2 ? 1 : 0);
  }

  // Morph: the dots gather to the centre and fade; a large 6 counts up with a row of six dots.
  function easy(on, t) {
    const c = block.geo.center;
    if (on) {
      App.tr(gBack, t * 0.4).style('opacity', 0);
      App.tr(gRange, t * 0.4).style('opacity', 0);
      App.tr(diamond, t * 0.4).style('opacity', 0);
      App.tr(diamondLabel, t * 0.4).style('opacity', 0);
      App.tr(dots, t * 0.6).attr('cx', c.x).attr('cy', c.y).attr('r', 3).style('opacity', 0);
      block.show(t, t ? t * 0.5 : 0);
    } else {
      block.hide(t);
      state(fig.state, t);
    }
  }

  function tips() {
    return d.years.map((r, i) => ({ x: pos[i].x, y: pos[i].y - R, text: `${r.year}: ${App.fmt(r.m4plus)} gempa M4+` }));
  }

  return { final: 2, draw, state, easy, tips };
});
