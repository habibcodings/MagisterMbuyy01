"""Recompute every catalog number cited in the final brief, storyboard, figure text and Q&A notes.

Writes reports/number_check.md. Counting rules: docs/storyboard.md §2 (via src.clean).
BMKG release figures (F1, main message) come from press reports and are not in the dataset;
only their arithmetic is checked. Facts only; no judgement on the claims.

Usage (from the repo root, after src.download):
    python -m src.number_check
"""
from pathlib import Path

import pandas as pd

from src import clean

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "number_check.md"
A, B, C, P0 = range(2014, 2018), range(2022, 2026), range(2021, 2025), range(2009, 2013)
ALL_YEARS = range(2009, 2026)

# BMKG release figures as typed in docs/storyboard.md §3 F1 (sources: storyboard §6)
RELEASE_TOTAL = {2020: 8264, 2021: 10570, 2022: 10792, 2023: 10789, 2024: 7358, 2025: 43439}
RELEASE_TOTAL_2024_JAN = 29869
RELEASE_M5 = {2020: 244, 2021: 244, 2022: 205, 2023: 219, 2024: 186, 2025: 153}

rows: list[dict] = []


def chk(doc, item, cited_text, cited, got, decimals=0, approx=False, how=""):
    if got is None:
        v = "n.a."
    elif round(got, decimals) == cited:
        v = "match"
    elif approx and cited and abs(got - cited) / abs(cited) <= 0.02:
        v = "close"
    else:
        v = "differs"
    shown = "" if got is None else f"{got:,.{max(decimals, 1) if isinstance(got, float) and not float(got).is_integer() else 0}f}"
    rows.append({"doc": doc, "item": item, "cited": cited_text, "recomputed": shown, "verdict": v, "how": how})


def note(doc, item, cited_text, recomputed, verdict, how=""):
    rows.append({"doc": doc, "item": item, "cited": cited_text, "recomputed": recomputed, "verdict": verdict, "how": how})


def main() -> None:
    days = clean.read_days()
    cat = clean.read_catalog()
    box_all = cat[clean.in_box(cat)]
    ev = clean.analysis_events()
    lo, hi = ev[ev.mag1 < 4], ev[ev.mag1 >= 4]
    yc = lambda s, yrs: clean.yearly_counts(s, days, yrs)
    per = lambda s, yrs: float(yc(s, yrs).mean())  # mean of (scaled) yearly counts
    S2 = "§2 rules: rounded magnitude, no-magnitude excluded, incomplete years scaled"

    # ---------------- release arithmetic (not in the dataset)
    chk("brief/main message", "BMKG total 2020 → 2025, ratio", "×5,3 / \"lima kali lipat\"", 5.3,
        RELEASE_TOTAL[2025] / RELEASE_TOTAL[2020], 1, how="43.439 ÷ 8.264 (release figures, arithmetic only)")
    note("brief/main message", "BMKG M5+ 2020 → 2025", "244 → 153", "release figures", "n.a.", "press reports (storyboard §6); not in the dataset")

    # ---------------- catalog vs announced
    for y in range(2020, 2025):
        n = int((box_all.year == y).sum())
        chk("storyboard §5 / qa", f"catalog {y} (box) vs BMKG year-end {RELEASE_TOTAL[y]:,}", "within 5%", 1,
            1.0 if abs(n / RELEASE_TOTAL[y] - 1) < 0.05 else 0.0, how=f"catalog {n:,}; difference {(n / RELEASE_TOTAL[y] - 1) * 100:+.1f}% "
            "(counts include events without magnitude)")
    n25 = int((box_all.year == 2025).sum())
    chk("storyboard §5 / qa", "catalog 2025 as share of 43.439", "43%", 43, n25 / RELEASE_TOTAL[2025] * 100,
        how=f"catalog {n25:,} (box, incl. no-magnitude); {int((ev.year == 2025).sum()):,} with magnitude = "
            f"{(ev.year == 2025).sum() / RELEASE_TOTAL[2025] * 100:.1f}%")

    # ---------------- F2 / brief claim 1
    nomag = int(box_all.magnitude.isna().sum())
    chk("figure-text F2", "events without magnitude", "923", 923, nomag)
    chk("figure-text F2", "…as share of box events", "0,6%", 0.6, nomag / len(box_all) * 100, 1)
    gap_years = [y for y in ALL_YEARS if clean.valid_days(days).get(y, 0) < clean.days_in_year(y)]
    note("figure-text F2", "incomplete years scaled", "2009, 2010, 2013, 2018", ", ".join(map(str, gap_years)),
         "match" if gap_years == [2009, 2010, 2013, 2018] else "differs", "years with any `broken` day")
    share = (per(lo, B) - per(lo, A)) / (per(ev, B) - per(ev, A)) * 100
    chk("brief claim 1 / F2 title", "share of the rise below M4 (2014–17 → 2022–25)", "97%", 97, share, how=S2)
    chk("brief claim 1", "M4+ change (2014–17 → 2022–25)", "+10%", 10, (per(hi, B) / per(hi, A) - 1) * 100, how=S2)
    yh = yc(hi, ALL_YEARS)
    chk("F2 band / F6", "M4+ minimum 2009–2025", "1.755 (2013)", 1755, float(yh.min()), how=f"year {yh.idxmin()}")
    chk("F2 band / F6", "M4+ maximum 2009–2025", "3.042 (2019)", 3042, float(yh.max()), how=f"year {yh.idxmax()}")
    t25 = int((ev.year == 2025).sum())
    tot_y = yc(ev, ALL_YEARS)
    chk("figure-text F2", "2025 total (with magnitude)", "18.357, \"total tertinggi\"", 18357, t25,
        how=f"highest year: {tot_y.idxmax()}")
    chk("figure-text F2", "2025 M4+", "1.895, \"termasuk yang terendah\"", 1895, float(yh[2025]),
        how=f"rank {int(yh.rank().loc[2025])} lowest of {len(yh)} years")

    # ---------------- F3 / brief claim 2
    mode = lambda s: float(s.mag1.value_counts().idxmax())
    chk("brief claim 2 / F3", "most common magnitude 2014–2017", "M3,4", 3.4, mode(ev[ev.year.isin(A)]), 1)
    chk("brief claim 2 / F3", "most common magnitude 2022–2025", "M3,0", 3.0, mode(ev[ev.year.isin(B)]), 1)
    bins_b = ev[ev.year.isin(B)].mag1.value_counts() / 4
    chk("storyboard F3", "highest per-year bin (y-axis 0–700)", "≤ 700", 1, 1.0 if bins_b.max() <= 700 else 0.0,
        how=f"max bin {bins_b.max():.1f} ({bins_b.idxmax():.1f})")
    for lbl, sel, yrs, cited in [("above M6,0, 2014–2017", ev.mag1 > 6.0, A, 5), ("above M6,0, 2022–2025", ev.mag1 > 6.0, B, 13),
                                 ("below M1,0, 2022–2025", ev.mag1 < 1.0, B, 3)]:
        chk("figure-text F3", f"events per year {lbl}", f"±{cited}", cited, per(ev[sel], yrs), approx=True)
    mlv = ev[ev.mag_type == "MLv"]
    chk("brief claim 2 / F3", "MLv only: most common magnitude 2014–2017", "M3,4", 3.4, mode(mlv[mlv.year.isin(A)]), 1)
    chk("brief claim 2 / F3", "MLv only: most common magnitude 2025", "M2,7", 2.7, mode(mlv[mlv.year == 2025]), 1)

    # ---------------- F4
    m45 = ev[(ev.mag1 >= 4.0) & (ev.mag1 <= 4.9)]
    med = lambda s, yrs: float(s[s.year.isin(yrs)].phasecount.median())
    chk("brief claim 2 / F4", "median phase readings M4,0–4,9, 2014–2017", "20", 20, med(m45, A))
    chk("brief claim 2 / F4", "median phase readings M4,0–4,9, 2022–2025", "44", 44, med(m45, B))
    chk("qa", "median phase readings, 2019", "22", 22, med(m45, [2019]))
    chk("qa", "median phase readings, 2022", "44", 44, med(m45, [2022]))
    m45v = m45[m45.mag_type == "MLv"]
    chk("figure-text F4", "MLv only: median phase readings 2014–2017", "18", 18, med(m45v, A))
    chk("figure-text F4", "MLv only: median phase readings 2025", "42", 42, med(m45v, [2025]))

    # ---------------- F5
    mc = clean.monthly_counts(hi, days, "2008-11", "2026-07")
    drawn = mc[~mc.gap]
    chk("storyboard F5", "months drawn", "210", 210, len(drawn))
    chk("storyboard F5", "partial months scaled", "10", 10, int(drawn.partial.sum()))
    gaps = [m.strftime("%Y-%m") for m in mc[mc.gap].index]
    note("storyboard F5", "gap months (< 15 days of data)", "Sep 2009, Jul–Agu 2013", ", ".join(gaps),
         "match" if gaps == ["2009-09", "2013-07", "2013-08"] else "differs")
    m_med = float(drawn["count"].median())
    chk("storyboard F5", "median month", "179 (label \"±180\")", 179, m_med)
    thr = 1.75 * m_med
    top = drawn["count"].sort_values(ascending=False)
    labelled = sorted(m.strftime("%Y-%m") for m in top[top >= thr].index)
    cited_months = ["2010-10", "2018-08", "2019-07", "2019-11", "2023-01", "2026-06"]
    note("storyboard F5", f"months ≥ 1,75 × median (≥ {thr:.2f})", ", ".join(cited_months),
         ", ".join(f"{m} ({top[pd.Period(m, 'M')]:.0f})" for m in labelled), "match" if labelled == cited_months else "differs")
    below = top[top < thr]
    chk("storyboard F5", "next highest month", "307", 307, float(below.iloc[0]), how=f"{below.index[0]}")
    chk("storyboard F5", "Palu, Sep 2018", "305", 305, float(top[pd.Period("2018-09", "M")]))
    patterns = {"2010-10": "Sumatra", "2018-08": "Sumbawa|Lombok", "2019-07": "Halmahera|Molucca",
                "2019-11": "Molucca", "2023-01": "Molucca|Talaud", "2026-06": "Mindanao|Philippine"}
    for m in cited_months:
        sub = hi[hi.ym == pd.Period(m, "M")]
        excess = top[pd.Period(m, "M")] - m_med
        named = int(sub.location.str.contains(patterns[m], case=False, na=False).sum())
        top3 = "; ".join(f"{k} ({v})" for k, v in sub.location.value_counts().head(3).items())
        note("storyboard F5", f"{m}: label rule \"≥ half of the excess\"", f"/{patterns[m]}/ labels",
             f"{named} of excess {excess:.0f} ({named / excess * 100:.0f}%); top: {top3}",
             "match" if named >= excess / 2 else "differs", "location-label proxy for the named sequence")

    # ---------------- F6 / decisions
    chk("F6", "median year M4+ 2009–2025", "2.159", 2159, float(yh.median()))
    chk("F6 / brief §4", "median per day", "≈6", 6, float(yh.median()) / 365, approx=True)
    chk("brief §4 / checklist", "baseline M4+ a year", "±2.150 / \"sekitar 2.150\"", 2150, float(yh.median()), approx=True,
        how="median of 2009–2025 (F6 label says 2.159)")
    chk("brief claim 3 / F6", "2026 pace (to 14 Aug)", "±2.430", 2430, clean.pace(hi, days, 2026), approx=True,
        how=f"{int((hi.year == 2026).sum()):,} events × 365 ÷ {int(clean.valid_days(days)[2026])} days")

    # ---------------- F-X
    sen = pd.read_csv(clean.RAW / "katalog_sensor.tsv", sep="\t", dtype=str, keep_default_na=False)
    for c in ["latitude", "longitude"]:
        sen[c] = pd.to_numeric(sen[c], errors="coerce")
    sen["eff"] = pd.to_datetime(sen.datetime, format="ISO8601")
    chk("storyboard F-X", "rows with fractional seconds", "50", 50, int(sen.datetime.str.contains(r"\.", regex=True).sum()))
    first = sen[clean.in_box(sen)].groupby("code").eff.min()
    placeholder = first.dt.strftime("%m-%d").eq("01-01") & first.dt.year.isin([1970, 1980])
    chk("storyboard F-X", "placeholder-dated codes (1970/1980-01-01)", "35", 35, int(placeholder.sum()))
    real = first[~placeholder]
    by = lambda y: int((real <= pd.Timestamp(f"{y}-12-31 23:59:59")).sum())
    chk("figure-text F-X", "codes by 2017", "369", 369, by(2017))
    chk("figure-text F-X", "codes by 2025", "1.314", 1314, by(2025))
    chk("figure-text F-X", "ratio", "×3,6", 3.6, by(2025) / by(2017), 1)
    chk("storyboard F-X", "dates on 1 January", "≈60%", 60, (real.dt.strftime("%m-%d") == "01-01").mean() * 100, approx=True)

    # ---------------- Q&A robustness
    chk("qa", "share of rise below M4, 2021–24 vs 2014–17", "91%", 91, (per(lo, C) - per(lo, A)) / (per(ev, C) - per(ev, A)) * 100)
    chk("qa", "M4+ change, 2021–24 vs 2014–17", "+20%", 20, (per(hi, C) / per(hi, A) - 1) * 100)
    chk("qa", "total change, 2021–24 vs 2014–17", "+76%", 76, (per(ev, C) / per(ev, A) - 1) * 100)
    chk("qa", "total change, 2009–12 → 2022–25", "+125%", 125, (per(ev, B) / per(ev, P0) - 1) * 100, approx=True)
    chk("qa", "M4+ per year, 2009–2012", "2.309", 2309, per(hi, P0), approx=True)
    chk("qa", "M4+ per year, 2022–2025", "2.145", 2145, per(hi, B))
    chk("qa", "M4+ change, 2009–12 → 2022–25", "−7%", -7, (per(hi, B) / per(hi, P0) - 1) * 100)
    for t, cited in [(5, (327, 173, 189)), (6, (21, 5.5, 16.5))]:
        s = ev[ev.mag1 >= t]
        for yrs, c in zip((P0, A, B), cited):
            chk("qa", f"M{t}+ per year, {yrs.start}–{yrs.stop - 1}", f"{c}".replace(".", ","), c, per(s, yrs),
                1 if isinstance(c, float) else 0, approx=True)
    chk("qa", "catalog M5+ 2021 (vs BMKG 244)", "about 200", 200, float(((ev.year == 2021) & (ev.mag1 >= 5)).sum()),
        approx=True, how=f"rounded ≥ 5,0; unrounded > 5: {int(((ev.year == 2021) & (ev.magnitude > 5)).sum())}")
    for t, a, b, cited in [("MLv", A, [2025], (4785, 17241, 1216, 1393, 3.4, 2.7, 18, 42)),
                           ("M", range(2010, 2013), range(2020, 2023), (4682, 9027, 1868, 2141, 3.4, 3.1, 16, 35))]:
        s = ev[ev.mag_type == t]
        s45 = s[(s.mag1 >= 4.0) & (s.mag1 <= 4.9)]
        got = (per(s, a), per(s, b), per(s[s.mag1 >= 4], a), per(s[s.mag1 >= 4], b),
               mode(s[s.year.isin(a)]), mode(s[s.year.isin(b)]), med(s45, a), med(s45, b))
        names = ("events/yr", "events/yr", "M4+/yr", "M4+/yr", "most common M", "most common M", "median phase", "median phase")
        for i, (nm, g, c) in enumerate(zip(names, got, cited)):
            period = f"{a.start}–{a.stop - 1}" if i % 2 == 0 and isinstance(a, range) else (f"{b[0]}" if not isinstance(b, range) and i % 2 else
                     (f"{b.start}–{b.stop - 1}" if i % 2 else f"{a[0]}"))
            chk("qa within-type", f"{t}: {nm}, {period}", f"{c}".replace(".", ","), c, g, 1 if isinstance(c, float) else 0, approx=True)
    for y, cited in [(2012, (3.5, 3.5)), (2019, (3.5, 3.4)), (2023, (3.3, 3.3)), (2024, (3.4, 3.2))]:
        m_m = float(ev[(ev.year == y) & (ev.mag_type == "M")].mag1.median())
        m_v = float(ev[(ev.year == y) & (ev.mag_type == "MLv")].mag1.median())
        note("qa", f"{y}: median magnitude, M vs MLv", f"{cited[0]} vs {cited[1]}".replace(".", ","), f"M {m_m:.1f} vs MLv {m_v:.1f}",
             "match" if (round(m_m, 1), round(m_v, 1)) == cited else "differs", "read as (M, MLv); the notes do not state the order")
    fm = cat[clean.in_box(cat) & cat.magnitude.notna()].copy()
    fm["magFM"] = pd.to_numeric(fm.magFM.replace("", None), errors="coerce")
    fm = fm[(fm.magTypeFM == "Mw") & fm.magFM.notna()]
    for yrs, c_d, c_n in [(A, 0.04, 147), (B, 0.16, 1265)]:
        d = fm[fm.year.isin(yrs)]
        diff = d.magnitude - d.magFM
        chk("qa", f"catalog magnitude − Mw, {yrs.start}–{yrs.stop - 1}: n", f"{c_n:,}", c_n, len(d), how="`magTypeFM` = Mw")
        chk("qa", f"catalog magnitude − Mw, {yrs.start}–{yrs.stop - 1}", f"+{c_d}".replace(".", ","), c_d, float(diff.median()), 2,
            how=f"median (mean is {diff.mean():+.2f}; the notes do not say which)")

    # ---------------- docs/easy-version.md (explain-easier blocks)
    E = "easy-version"
    rise = per(ev, B) - per(ev, A)
    chk(E, "Gambar 1: 'lima kali lebih banyak' (releases 2025 ÷ 2020)", "≈5", 5, RELEASE_TOTAL[2025] / RELEASE_TOTAL[2020], approx=True, how="43.439 ÷ 8.264; release arithmetic")
    chk(E, "Gambar 2: of every 100 added quakes, M4+", "3", 3, (per(hi, B) - per(hi, A)) / rise * 100, how=S2)
    chk(E, "Gambar 2: of every 100 added quakes, below M4", "97", 97, (per(lo, B) - per(lo, A)) / rise * 100, how=S2)
    tenth = lambda yrs, t: float(((ev[ev.year.isin(yrs)].mag1 * 10).round() == t).sum() / len(yrs))
    chk(E, "Gambar 3: quakes per year at M3,0, 2014–2017", "212", 212, tenth(A, 30))
    chk(E, "Gambar 3: quakes per year at M3,0, 2022–2025", "618", 618, tenth(B, 30))
    chk(E, "Gambar 3: 'hampir tiga kali'", "<3, ≈3", 3, tenth(B, 30) / tenth(A, 30), approx=True, how="ratio 2022–25 ÷ 2014–17")
    note(E, "Gambar 3: M4,5 'hampir tidak berubah'", "(no number)", f"{tenth(A, 45):.0f} → {tenth(B, 45):.0f} per year", "n.a.", "context for the sentence")
    chk(E, "Gambar 4: median phase readings 2014–2017 → 2022–2025", "20 → 44", 44, med(m45, B), how=f"2014–2017: {med(m45, A):.0f}")
    chk(E, "Gambar 5: typical month (median)", "179", 179, m_med)
    chk(E, "Gambar 5: Nov 2019", "397", 397, float(top[pd.Period("2019-11", "M")]))
    chk(E, "Gambar 5: 'lebih dari dua kali bulan biasa'", "> 2", 1, 1.0 if float(top[pd.Period("2019-11", "M")]) / m_med > 2 else 0.0,
        how=f"ratio {float(top[pd.Period('2019-11', 'M')]) / m_med:.2f}")
    chk(E, "Gambar 6: M4+ per day", "≈6", 6, float(yh.median()) / 365, approx=True, how="median 2009–2025 ÷ 365")
    pace26 = clean.pace(hi, days, 2026)
    chk(E, "Gambar 6: 2026 'masih di kisaran yang sama'", "inside the range", 1, 1.0 if yh.min() <= pace26 <= yh.max() else 0.0,
        how=f"pace {pace26:,.0f} in {yh.min():,.0f}–{yh.max():,.0f}")

    df = pd.DataFrame(rows)
    counts = df.verdict.value_counts().to_dict()
    lines = [
        "# Number check: final documents vs. the rebuilt catalog",
        "",
        "Generated by `src/number_check.py` for the final `docs/brief.md`, `docs/storyboard.md`, `docs/figure-text.md`, "
        "`docs/qa-notes.md` and `docs/easy-version.md` (2026-10-28). Catalog: `data/raw/katalog_gempa_v2.tsv` (SHA-256 `7c92b9e9…dd77a7`); counting rules "
        "from storyboard §2. Verdicts: **match** = equal at the cited precision; **close** = a \"±/≈/about\" value within 2%; "
        "**differs** = outside that; **n.a.** = not checkable from the dataset.",
        "",
        "Summary: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) + ".",
        "",
        "| doc | item | cited | recomputed | verdict | how |",
        "|---|---|---|---|---|---|",
    ] + [f"| {r.doc} | {r.item} | {r.cited} | {r.recomputed} | **{r.verdict}** | {r.how} |" for r in df.itertuples()]
    REPORT.write_text("\n".join(lines) + "\n")
    print(f"wrote {REPORT.relative_to(ROOT)}: {counts}")


if __name__ == "__main__":
    main()
