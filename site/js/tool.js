/* "Cek judulmu": suggests the headline verb from BMKG release numbers. Text only, no chart, no network.
   The three cases and every output string follow 05_page_copy.md §10. */
(function () {
  'use strict';
  const App = window.App;
  const RANGE_MAX = 244;   // highest annual M5+ in BMKG releases 2020–2025 (range 153–244)
  const AVOID = 'Hindari “makin sering”. Tulis “lebih banyak gempa yang tercatat”.';

  // year is printed as is (no thousands separator); counts use the Indonesian format
  function decide(o) {
    const f = App.fmt;
    const out = { range: null, felt: null, extra: null };
    if (o.now < o.last) {
      out.case = 'A';
      out.finding = `Gempa M5+ turun dari ${f(o.last)} menjadi ${f(o.now)}.`;
      out.advice = AVOID;
      out.headline = `BMKG Catat ${f(o.total)} Gempa Sepanjang ${o.year}, Gempa M5+ Justru Turun`;
    } else if (o.now === o.last) {
      out.case = 'B';
      out.finding = `Gempa M5+ sama dengan tahun lalu (${f(o.now)}).`;
      out.advice = AVOID;
      out.headline = `BMKG Catat ${f(o.total)} Gempa Sepanjang ${o.year}; Gempa M5+ Tidak Bertambah`;
    } else {
      const pct = f(Math.round((Math.abs(o.now - o.last) / o.last) * 100));
      out.case = 'C';
      out.finding = `Gempa M5+ naik dari ${f(o.last)} menjadi ${f(o.now)} (+${pct}%).`;
      out.range = o.now <= RANGE_MAX
        ? 'Masih dalam rentang 2020–2025 (153–244).'
        : 'Ini di atas rentang 2020–2025 (153–244). Cari rangkaian gempa yang menyebabkannya dan sebut namanya.';
      out.advice = 'Kata “naik” tepat untuk gempa M5+, bukan untuk total.';
      out.headline = `BMKG Catat ${f(o.total)} Gempa Sepanjang ${o.year}, Gempa M5+ Naik ${pct}%`;
    }
    if (o.felt !== null && o.felt !== undefined) out.felt = `Gempa dirasakan: ${f(o.felt)}. Cantumkan di samping total.`;
    if (o.year === 2024) out.extra = 'Catatan: BMKG juga merilis angka 7.358 untuk 2024 (31 Des 2024).';
    return out;
  }

  function fromYear(year) {
    const rows = App.data.f1.years;
    const r = rows.find((x) => x.year === year), prev = rows.find((x) => x.year === year - 1);
    return { year, total: r.total, now: r.m5plus, last: prev.m5plus, felt: r.felt };
  }

  const num = (s) => (s.trim() === '' ? null : parseInt(s.replace(/\./g, ''), 10));

  App.tool = {
    decide,
    fromYear,
    init() {
      const tabs = Array.from(document.querySelectorAll('#cek-judul [role="tab"]'));
      const panels = tabs.map((t) => document.getElementById(t.getAttribute('aria-controls')));
      const out = document.getElementById('tool-out');
      const q = (c) => out.querySelector(c);
      const copyBtn = q('.btn-copy');

      function select(i, focus) {
        tabs.forEach((t, j) => {
          t.setAttribute('aria-selected', String(i === j));
          t.tabIndex = i === j ? 0 : -1;
          panels[j].hidden = i !== j;
        });
        out.hidden = true;
        if (focus) tabs[i].focus();
      }
      tabs.forEach((t, i) => {
        t.addEventListener('click', () => select(i));
        t.addEventListener('keydown', (e) => {
          const k = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
          if (k) { select((i + k + tabs.length) % tabs.length, true); e.preventDefault(); }
          if (e.key === 'Home') { select(0, true); e.preventDefault(); }
          if (e.key === 'End') { select(tabs.length - 1, true); e.preventDefault(); }
        });
      });

      function render(res) {
        q('.out-finding').textContent = res.finding;
        q('.out-range').textContent = res.range || '';
        q('.out-range').hidden = !res.range;
        q('.out-advice').textContent = res.advice;
        q('.out-headline').textContent = res.headline;
        q('.out-felt').textContent = res.felt || '';
        q('.out-felt').hidden = !res.felt;
        q('.out-extra').textContent = res.extra || '';
        q('.out-extra').hidden = !res.extra;
        copyBtn.textContent = copyBtn.dataset.label;
        out.hidden = false;
      }

      document.getElementById('panel-tahun').addEventListener('submit', (e) => {
        e.preventDefault();
        render(decide(fromYear(+document.getElementById('t-year').value)));
      });
      const form = document.getElementById('panel-baru');
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        if (!form.reportValidity()) return;
        const v = (id) => num(document.getElementById(id).value);
        render(decide({ year: v('n-year'), total: v('n-total'), now: v('n-now'), last: v('n-last'), felt: v('n-felt') }));
      });

      copyBtn.addEventListener('click', async () => {
        const text = q('.out-headline').textContent;
        let ok = false;
        try { await navigator.clipboard.writeText(text); ok = true; } catch (err) { ok = false; }
        if (!ok) {
          const range = document.createRange();
          range.selectNodeContents(q('.out-headline'));
          const sel = window.getSelection();
          sel.removeAllRanges();
          sel.addRange(range);
          try { ok = document.execCommand('copy'); } catch (err) { ok = false; }
        }
        if (ok) {
          copyBtn.textContent = copyBtn.dataset.done;
          setTimeout(() => { copyBtn.textContent = copyBtn.dataset.label; }, 2000);
        }
      });
    }
  };
})();
