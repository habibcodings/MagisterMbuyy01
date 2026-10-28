/* G5: monthly M4+ with gaps, median line, six labelled spikes that open a card. Spec 04 §5 G5. */
App.define('g5', function (ctx) {
  const { svg, plot, fig } = ctx;
  const C = App.C;
  const d = ctx.data.f5;
  const months = d.months.filter((m) => m.month <= d.last_month);
  const date = (ym) => new Date(+ym.slice(0, 4), +ym.slice(5, 7) - 1, 1);
  const halo = (sel) => sel.attr('stroke', '#fff').attr('stroke-width', 4).attr('paint-order', 'stroke');
  let x, y, W, gBack, gTitle, gLine, clip, medLine, medLabel, spikeG, spikeDots, spikeLabels, seed, block, buttons = [], card = null, openIdx = -1;

  function draw(w, h) {
    W = w;
    const ml = 36, mr = 12, mb = 24, wide = w >= 560;
    x = d3.scaleTime().domain([date(months[0].month), date(d.last_month)]).range([ml, w - mr]);

    // spike labels sit in tiers above the plot; place them first to know the top margin.
    // Narrow screens use short labels (place + year); the full name is in the spike card.
    const fs = wide ? 12.5 : 11.5, lh = fs * 1.2, tierH = lh * 2 + 6, gap = 6;
    const lo = 4, hi = w - 4;
    const labels = d.spikes.map((s) => {
      const l1 = wide ? s.label : s.label.split(/ & |, /)[0];
      const l2 = wide ? App.month(s.month) : s.month.slice(0, 4);
      const lw = Math.max(App.measure(l1, fs, 800), App.measure(l2, fs, 600)) + 6;
      return { s, l1, l2, lw, cx: x(date(s.month)) };
    });
    const maxTiers = wide ? 3 : 2;
    const tiers = d3.range(maxTiers).map(() => []);
    labels.forEach((L, i) => {
      const left = L.cx - L.lw / 2;
      let tier = wide ? tiers.findIndex((t) => !t.some((o) => left < o.cx + o.lw / 2 + gap && left + L.lw > o.cx - o.lw / 2 - gap)) : i % 2;
      if (tier < 0) tier = maxTiers - 1;
      L.tier = tier;
      tiers[tier].push(L);
    });
    // within a tier, push overlapping labels apart and keep them inside the chart
    tiers.forEach((t) => {
      t.sort((a, b) => a.cx - b.cx);
      t.forEach((L) => { L.left = Math.max(lo, Math.min(hi - L.lw, L.cx - L.lw / 2)); });
      for (let i = 1; i < t.length; i++) t[i].left = Math.max(t[i].left, t[i - 1].left + t[i - 1].lw + gap);
      if (t.length) t[t.length - 1].left = Math.min(t[t.length - 1].left, hi - t[t.length - 1].lw);
      for (let i = t.length - 2; i >= 0; i--) t[i].left = Math.min(t[i].left, t[i + 1].left - t[i].lw - gap);
    });
    const nT = d3.max(labels, (L) => L.tier) + 1;
    const mt = nT * tierH + 10;
    y = d3.scaleLinear().domain([0, 400]).range([h - mb, mt]);

    gBack = svg.append('g');
    App.yGrid(gBack, y, ml, w - mr, [0, 100, 200, 300, 400]);
    const yrs = d3.range(2010, 2027, wide ? 2 : 4);
    yrs.forEach((yr) => gBack.append('text').attr('x', x(new Date(yr, 0, 1))).attr('y', h - mb + 15).attr('text-anchor', 'middle')
      .style('font-size', '12px').attr('fill', C.muted).text(yr));

    clip = svg.append('defs').append('clipPath').attr('id', 'g5-clip').append('rect').attr('x', 0).attr('y', 0).attr('height', h).attr('width', 0);
    gLine = svg.append('g').attr('clip-path', 'url(#g5-clip)');
    gLine.append('path').attr('fill', 'none').attr('stroke', C.strong).attr('stroke-width', 1.75).attr('stroke-linejoin', 'round')
      .attr('d', d3.line().defined((m) => m.value !== null).x((m) => x(date(m.month))).y((m) => y(m.value))(months));

    medLine = svg.append('line');
    medLabel = halo(App.label(svg.append('g'), 'Bulan biasa: ±180 gempa M4+', ml + 4, y(d.median) - 6, { valign: 'bottom', fill: C.label, size: 13 }));

    spikeG = svg.append('g');
    spikeLabels = labels.map((L) => {
      const g = spikeG.append('g').style('opacity', 0);
      const top = L.tier * tierH + 2;
      const sy = y(L.s.value);
      g.append('path').attr('fill', 'none').attr('stroke', C.text).attr('stroke-width', 1)
        .attr('d', `M${L.left + L.lw / 2},${top + lh * 2 + 2}L${L.cx},${sy - 7}`);
      const t = halo(g.append('text').attr('text-anchor', 'middle').attr('fill', C.text));
      t.append('tspan').attr('x', L.left + L.lw / 2).attr('y', top + fs).style('font-size', fs + 'px').style('font-weight', 800).text(L.l1);
      t.append('tspan').attr('x', L.left + L.lw / 2).attr('y', top + fs + lh).style('font-size', fs + 'px').style('font-weight', 600).attr('fill', C.label).text(L.l2);
      return g;
    });
    spikeDots = spikeG.selectAll('circle').data(d.spikes).join('circle')
      .attr('cx', (s) => x(date(s.month))).attr('cy', (s) => y(s.value)).attr('r', 0)
      .attr('fill', C.strong).attr('stroke', '#fff').attr('stroke-width', 2);

    // axis title above the spike leader lines, with a halo where a leader crosses it
    gTitle = svg.append('g');
    App.axisTitle(gTitle, 'Gempa M4+ per bulan', 0, 12).attr('transform', `translate(${ml - 30},${mt - 6})`)
      .attr('stroke', '#fff').attr('stroke-width', 4).attr('paint-order', 'stroke');

    block = App.block(svg, w, h, { type: 'compare', tone: 'strong', rows: [{ label: 'Bulan biasa', value: Math.round(d.median) }, { label: 'Nov 2019 (Laut Maluku)', value: d.spikes.find((s) => s.month === '2019-11').value }] });
    seed = svg.append('rect').attr('fill', C.strong).style('opacity', 0);
    makeButtons();
  }

  /* ---------- spike buttons and cards (HTML over the SVG) ---------- */

  function makeButtons() {
    closeCard();
    buttons.forEach((b) => b.remove());
    buttons = d.spikes.map((s, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'spike-btn';
      b.style.left = x(date(s.month)) + 'px';
      b.style.top = y(s.value) + 'px';
      b.setAttribute('aria-label', `${s.label} · ${App.month(s.month)}`);
      b.setAttribute('aria-expanded', 'false');
      b.hidden = true;
      b.addEventListener('click', (e) => { e.stopPropagation(); if (openIdx === i) closeCard(); else openCard(i); });
      plot.appendChild(b);
      return b;
    });
  }

  function openCard(i) {
    closeCard();
    const s = d.spikes[i];
    const b = buttons[i];
    card = document.createElement('div');
    card.className = 'spike-card';
    card.id = 'g5-card';
    card.textContent = `${s.label} · ${App.month(s.month)} · ${App.fmt(s.value)} gempa M4+, ${App.mag(s.value / Math.round(d.median))}× bulan biasa`;
    plot.appendChild(card);
    const cw = card.offsetWidth, ch = card.offsetHeight;
    const bx = parseFloat(b.style.left), by = parseFloat(b.style.top);
    card.style.left = Math.max(4, Math.min(W - cw - 4, bx - cw / 2)) + 'px';
    card.style.top = (by + 18 + ch < plot.clientHeight ? by + 18 : by - ch - 18) + 'px';
    b.setAttribute('aria-expanded', 'true');
    b.setAttribute('aria-describedby', 'g5-card');
    openIdx = i;
  }

  function closeCard() {
    if (card) card.remove();
    card = null;
    if (openIdx >= 0 && buttons[openIdx]) { buttons[openIdx].setAttribute('aria-expanded', 'false'); buttons[openIdx].removeAttribute('aria-describedby'); }
    openIdx = -1;
  }

  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && card) { const b = buttons[openIdx]; closeCard(); if (b) b.focus(); } });
  document.addEventListener('pointerdown', (e) => { if (card && !card.contains(e.target) && !e.target.classList.contains('spike-btn')) closeCard(); });

  function setButtons(active, pulse) {
    buttons.forEach((b) => {
      b.hidden = !active;
      b.classList.remove('pulse');
      if (active && pulse) { void b.offsetWidth; b.classList.add('pulse'); }
    });
    if (!active) closeCard();
  }

  /* ---------- states ---------- */

  function state(s, t) {
    App.tr(gBack, t).style('opacity', 1);
    App.tr(gTitle, t).style('opacity', 1);
    block.hide(0);
    seed.interrupt().style('opacity', 0);
    gLine.style('opacity', 1);
    App.tr(clip, t ? 800 : 0).attr('width', W);
    App.tr(medLine, t)
      .attr('x1', x.range()[0]).attr('x2', x.range()[1]).attr('y1', y(d.median)).attr('y2', y(d.median))
      .attr('stroke', C.muted).attr('stroke-width', 1.5).attr('stroke-dasharray', '5 4').attr('stroke-linecap', 'butt')
      .style('opacity', s >= 1 ? 1 : 0);
    App.tr(medLabel, t).style('opacity', s >= 1 ? 1 : 0);
    App.tr(spikeDots, t, (_, i) => (s >= 2 && t ? i * 120 : 0)).attr('r', s >= 2 ? 5.5 : 0).style('opacity', 1);
    spikeLabels.forEach((g, i) => App.tr(g, t, s >= 2 && t ? i * 120 : 0).style('opacity', s >= 2 ? 1 : 0));
    setButtons(s >= 3 && !fig.easy, s >= 3 && t > 0);
  }

  // Morph: everything fades except the median line and the Nov 2019 point, which become the two bars.
  function easy(on, t) {
    const bars = block.geo.bars;
    const nov = d.spikes.find((sp) => sp.month === '2019-11');
    const p = { x: x(date(nov.month)), y: y(nov.value) };
    if (on) {
      setButtons(false);
      App.tr(gBack, t * 0.4).style('opacity', 0);
      App.tr(gTitle, t * 0.4).style('opacity', 0);
      App.tr(gLine, t * 0.4).style('opacity', 0);
      App.tr(medLabel, t * 0.3).style('opacity', 0);
      App.tr(spikeG.selectAll('g'), t * 0.3).style('opacity', 0);
      App.tr(spikeDots, t * 0.3).style('opacity', 0);
      const b0 = bars[0];
      medLine.interrupt().attr('stroke-dasharray', null).style('opacity', 1);
      App.tr(medLine, t, t * 0.15)
        .attr('x1', b0.x + b0.h / 2).attr('x2', b0.x + b0.w - b0.h / 2).attr('y1', b0.y + b0.h / 2).attr('y2', b0.y + b0.h / 2)
        .attr('stroke-width', b0.h).attr('stroke-linecap', 'round').attr('stroke', C.strong);
      seed.interrupt().attr('x', p.x - 5).attr('y', p.y - 5).attr('width', 10).attr('height', 10).attr('rx', 5).style('opacity', 1);
      App.tr(seed, t, t * 0.15).attr('x', bars[1].x).attr('y', bars[1].y).attr('width', bars[1].w).attr('height', bars[1].h).attr('rx', bars[1].h / 2);
      block.show(t, t ? t * 0.9 : 0);
    } else {
      block.hide(t);
      App.tr(seed, t * 0.6).attr('x', p.x - 5).attr('y', p.y - 5).attr('width', 10).attr('height', 10).attr('rx', 5).style('opacity', 0);
      App.tr(gLine, t, t * 0.3).style('opacity', 1);
      state(fig.state, t);
    }
  }

  function tips() {
    return months.filter((m) => m.value !== null).map((m) => ({
      x: x(date(m.month)), y: y(m.value), xOnly: true,
      text: `${App.month(m.month)} · ${App.fmt(m.value)} gempa M4+` + (m.scaled ? ' (disetarakan sebulan penuh)' : '')
    }));
  }

  return { final: 3, draw, state, easy, tips };
});
