"""Story figures: one function per figure in docs/storyboard.md.

All visible text is taken verbatim from docs/figure-text.md; colors from storyboard §2.
Each function writes figures/<name>.png and returns the path. Output is deterministic
(bundled DejaVu Sans font, fixed size and DPI, no timestamp metadata).
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
from matplotlib.ticker import FixedLocator, FuncFormatter  # noqa: E402

from src import clean  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
RAW = ROOT / "data" / "raw"

# --- palette (storyboard §2) ---------------------------------------------------
ORANGE = "#C2410C"      # stronger quakes: M5+ in releases, M4+ in the catalog
GREY = "#B8BEC6"        # smaller quakes (fills only)
GREY_TEXT = "#6B7280"   # grey-category text, axes, notes
SLATE = "#475569"       # totals not split by size
INK = "#1F2937"         # titles and annotations
GRID = "#E5E7EB"
BG = "#FFFFFF"
TINT = {"orange10": "#F9ECE7", "orange20": "#F3D9CE", "orange45": "#E4AA92", "grey35": "#E6E8EB", "slate8": "#F0F1F3"}

# --- layout (technical hygiene) -------------------------------------------------
WIDTH_IN, DPI = 7.0, 220
FONT = "DejaVu Sans"
SIZE = {"title": 14.5, "subtitle": 11, "panel": 11, "label": 10.5, "tick": 10, "note": 8.6}
SAVE_KW = {"dpi": DPI, "facecolor": BG, "metadata": {"Software": None}}

plt.rcParams.update({
    "font.family": FONT, "font.size": SIZE["tick"], "text.color": INK,
    "axes.edgecolor": GREY_TEXT, "axes.labelcolor": GREY_TEXT, "axes.linewidth": 0.8,
    "xtick.color": GREY_TEXT, "ytick.color": GREY_TEXT, "xtick.labelsize": SIZE["tick"], "ytick.labelsize": SIZE["tick"],
    "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": BG, "axes.facecolor": BG,
    "svg.hashsalt": "vdl-midterm",
})


def id_int(x: float) -> str:
    """Indonesian thousands separator: 10000 -> '10.000'."""
    return f"{x:,.0f}".replace(",", ".")


ID_INT = FuncFormatter(lambda x, _: id_int(x))
ID_DEC1 = FuncFormatter(lambda x, _: f"{x:.1f}".replace(".", ","))

# Shared source line for F2–F6 (figure-text.md)
SOURCE_CATALOG = ("Sumber: Katalog gempa BMKG (RepoGempa), dihimpun A. K. Vigiliant, Kaggle, doi:10.34740/kaggle/ds/1934565; "
                  "diunduh 28 Oktober 2026. Wilayah 11° LS–6° LU, 94°–142° BT. Olahan: Hanjani & Azizah.")
PERIODS = [(2014, 2017), (2022, 2025)]


def catalog():
    """(days, events) under storyboard §2 counting rules."""
    return clean.read_days(), clean.analysis_events()


def frame(height: float, text: dict, left: float = 0.125, right: float = 0.97, gap_top: float = 0.035,
          gap_bottom: float = 0.075):
    """Figure with header and footer; returns (fig, axes) filling the space between them."""
    fig = plt.figure(figsize=(WIDTH_IN, height))
    top = header(fig, text["title"], text["subtitle"])
    bottom = footer(fig, text.get("note"), text["source"])
    ax = fig.add_axes([left, bottom + gap_bottom, right - left, top - bottom - gap_bottom - gap_top])
    ax.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    return fig, ax


def fit_wrap(fig, text: str, fontsize: float, weight: str = "normal", max_frac: float = 0.955) -> str:
    """Greedy word wrap so each line fits within `max_frac` of the figure width (measured, not counted)."""
    renderer = fig.canvas.get_renderer()
    limit = fig.get_size_inches()[0] * fig.dpi * max_frac
    probe = fig.text(0, 0, "", fontsize=fontsize, fontweight=weight)
    out = []
    for para in text.split("\n"):
        line = ""
        for word in para.split(" "):
            trial = f"{line} {word}".strip()
            probe.set_text(trial)
            if line and probe.get_window_extent(renderer).width > limit:
                out.append(line)
                line = word
            else:
                line = trial
        out.append(line)
    probe.remove()
    return "\n".join(out)


def header(fig, title: str, subtitle: str, top: float = 0.985) -> float:
    """Title and subtitle at the top-left of the figure; returns the y where content can start."""
    t = fit_wrap(fig, title, SIZE["title"], "bold")
    s = fit_wrap(fig, subtitle, SIZE["subtitle"])
    n_t, n_s = t.count("\n") + 1, s.count("\n") + 1
    h_in = fig.get_size_inches()[1]
    line = lambda pt: pt * 1.32 / 72 / h_in  # line height as a figure fraction
    fig.text(0.02, top, t, ha="left", va="top", fontsize=SIZE["title"], fontweight="bold", color=INK)
    y_sub = top - n_t * line(SIZE["title"]) - 0.006
    fig.text(0.02, y_sub, s, ha="left", va="top", fontsize=SIZE["subtitle"], color=GREY_TEXT)
    return y_sub - n_s * line(SIZE["subtitle"]) - 0.01


def footer(fig, note: str | None, source: str, bottom: float = 0.012) -> float:
    """Note line(s) and source line at the bottom-left; returns the y above them."""
    parts = []
    if note:
        parts.append(fit_wrap(fig, "Catatan: " + note, SIZE["note"]))
    parts.append(fit_wrap(fig, source, SIZE["note"]))
    text = "\n".join(parts)
    fig.text(0.02, bottom, text, ha="left", va="bottom", fontsize=SIZE["note"], color=GREY_TEXT, linespacing=1.35)
    n = text.count("\n") + 1
    return bottom + n * SIZE["note"] * 1.35 / 72 / fig.get_size_inches()[1] + 0.012


def save(fig, name: str) -> Path:
    FIGURES.mkdir(parents=True, exist_ok=True)
    path = FIGURES / f"{name}.png"
    fig.savefig(path, **SAVE_KW)
    plt.close(fig)
    return path


# =============================================================================
# F1 — the number reporters print (BMKG release figures)
# =============================================================================
F1_TEXT = {
    "title": "Total gempa yang diumumkan BMKG naik lima kali lipat, tetapi gempa M5+ menurut BMKG sendiri justru turun",
    "subtitle": "Angka tahunan dalam rilis BMKG, 2020–2025",
    "panel_top": "Semua gempa",
    "panel_bottom": "Gempa M5+",
    "y": "Gempa per tahun",
    "marker_2024": "7.358 (angka akhir tahun, 31 Des 2024)",
    "bracket": "×5,3",
    "bottom_label": "244 → 153",
    "note": "BMKG mengumumkan dua angka untuk 2024: 7.358 (Direktur Gempabumi dan Tsunami, 31 Des 2024) dan 29.869 "
            "(Kepala BMKG, 17 Jan 2025); jumlah M5+ 2024 (186) berasal dari rilis 31 Des 2024. Batas M5 ditulis "
            "“di atas M5” atau “M≥5”, tergantung rilis. Gempa dirasakan: 754 (2020) dan 973 (2025).",
    "source": "Sumber: Rilis tahunan BMKG, dikutip CNN Indonesia (30 Des 2021), Antara, IDX Channel (31 Des 2024), "
              "Okezone (17 Jan 2025) dan kumparan (2 Jan 2026). Olahan: Hanjani & Azizah.",
}


def f1_release_figures() -> pd.DataFrame:
    """BMKG release figures (typed from press reports; source numbers refer to storyboard §6)."""
    rel = pd.read_csv(RAW / "bmkg_releases.csv")
    second = pd.read_csv(RAW / "bmkg_releases_second_2024.csv")
    rel["total_shown"] = rel.total
    rel.loc[rel.year == 2024, "total_shown"] = int(second.total.iloc[0])  # 2024 column shows 29.869
    return rel


def f1() -> Path:
    t = F1_TEXT
    rel = f1_release_figures()
    years = rel.year.tolist()
    x = range(len(years))

    fig = plt.figure(figsize=(WIDTH_IN, 6.6))
    content_top = header(fig, t["title"], t["subtitle"])
    content_bottom = footer(fig, t["note"], t["source"])
    # top panel about three times the bottom one; panel titles sit inside the gap above each axis
    gs = fig.add_gridspec(2, 1, height_ratios=[3, 1], hspace=0.42,
                          left=0.12, right=0.97, top=content_top - 0.045, bottom=content_bottom + 0.045)
    ax_t, ax_b = fig.add_subplot(gs[0]), fig.add_subplot(gs[1], sharex=None)
    bar_w = 0.62

    # --- top panel: all quakes (slate)
    ax_t.bar(x, rel.total_shown, width=bar_w, color=SLATE, zorder=2)
    for i, v in zip(x, rel.total_shown):
        ax_t.text(i, v + 900, id_int(v), ha="center", va="bottom", fontsize=SIZE["label"], color=INK)
    i24 = years.index(2024)
    v_end = int(rel.loc[rel.year == 2024, "total"].iloc[0])
    # hollow slate marker; a white ring keeps its slate outline visible on the slate column
    ax_t.plot([i24], [v_end], marker="o", markersize=13, markerfacecolor=BG, markeredgecolor=BG, zorder=4)
    ax_t.plot([i24], [v_end], marker="o", markersize=9, markerfacecolor=BG, markeredgecolor=SLATE,
              markeredgewidth=1.8, zorder=5)
    ax_t.annotate(t["marker_2024"], xy=(i24, v_end), xytext=(i24 - 0.5, 21500),
                  ha="right", va="center", fontsize=SIZE["label"] - 0.5, color=INK,
                  arrowprops={"arrowstyle": "-", "color": INK, "lw": 0.9, "relpos": (1, 0.5),
                              "shrinkA": 3, "shrinkB": 7})
    # ×5,3 bracket from 2020 to 2025
    y_br = 53000
    i0, i1 = 0, len(years) - 1
    ax_t.plot([i0, i0, i1, i1], [y_br - 2200, y_br, y_br, y_br - 2200], color=INK, lw=1.1, zorder=3)
    ax_t.text((i0 + i1) / 2, y_br + 900, t["bracket"], ha="center", va="bottom", fontsize=SIZE["label"] + 1.5,
              fontweight="bold", color=INK)
    ax_t.set_ylim(0, 60000)
    ax_t.set_title(t["panel_top"], loc="left", fontsize=SIZE["panel"], fontweight="bold", color=INK, pad=6)

    # --- bottom panel: M5+ (orange)
    ax_b.bar(x, rel.m5, width=bar_w, color=ORANGE, zorder=2)
    for i, v in zip(x, rel.m5):
        ax_b.text(i, v + 8, id_int(v), ha="center", va="bottom", fontsize=SIZE["label"], color=INK)
    ax_b.text(i1 + 0.42, 318, t["bottom_label"], ha="right", va="center", fontsize=SIZE["label"] + 1.5,
              fontweight="bold", color=ORANGE)
    ax_b.set_ylim(0, 340)
    ax_b.set_title(t["panel_bottom"], loc="left", fontsize=SIZE["panel"], fontweight="bold", color=INK, pad=6)

    for ax in (ax_t, ax_b):
        ax.set_xticks(list(x), [str(y) for y in years])
        ax.set_xlim(-0.6, len(years) - 0.4)
        ax.yaxis.set_major_formatter(ID_INT)
        ax.set_ylabel(t["y"], fontsize=SIZE["tick"])
        ax.grid(axis="y", color=GRID, lw=0.8, zorder=0)
        ax.tick_params(axis="x", length=0)
    ax_t.set_yticks([0, 15000, 30000, 45000])
    ax_b.set_yticks([0, 100, 200, 300])
    ax_t.tick_params(axis="x", labelbottom=False)
    return save(fig, "f1_rilis_bmkg")


# =============================================================================
# F2 — the same pattern in the public catalog, since 2009
# =============================================================================
F2_TEXT = {
    "title": "Di katalog publik BMKG, 97% kenaikan adalah gempa di bawah M4; gempa M4+ nyaris tidak berubah",
    "subtitle": "Gempa per tahun menurut magnitudo, katalog RepoGempa, 2009–2025",
    "y": "Gempa per tahun",
    "seg_hi": "M4+",
    "seg_lo": "Di bawah M4",
    "band": "M4+: 1.755–3.042 per tahun sejak 2009",
    "label_2025": "2025: total tertinggi (18.357), tetapi M4+ termasuk yang terendah (1.895)",
    "note": "Magnitudo dibulatkan ke satu desimal seperti yang diumumkan BMKG; M4+ berarti M4,0 ke atas. Tahun dengan data "
            "tidak lengkap (2009, 2010, 2013, 2018) disetarakan ke satu tahun penuh. 923 gempa tanpa magnitudo (0,6%) tidak dihitung.",
    "source": SOURCE_CATALOG,
}


def f2() -> Path:
    t = F2_TEXT
    days, ev = catalog()
    years = list(range(2009, 2026))
    hi = clean.yearly_counts(ev[ev.mag1 >= 4], days, years)
    lo = clean.yearly_counts(ev[ev.mag1 < 4], days, years)
    x = np.arange(len(years))

    fig, ax = frame(6.3, t, right=0.76)
    for a, b in PERIODS:
        i0, i1 = years.index(a), years.index(b)
        ax.axvspan(i0 - 0.5, i1 + 0.5, color=TINT["slate8"], lw=0, zorder=0.5)
        ax.text((i0 + i1) / 2, 21300, f"{a}–{b}", ha="center", va="top", fontsize=SIZE["label"], color=GREY_TEXT)
    ax.axhspan(1755, 3042, color=TINT["orange20"], lw=0, zorder=1)
    ax.bar(x, hi, width=0.72, color=ORANGE, edgecolor=BG, linewidth=1, zorder=2)
    ax.bar(x, lo, bottom=hi, width=0.72, color=GREY, edgecolor=BG, linewidth=1, zorder=2)

    last = len(years) - 1
    tr = ax.get_yaxis_transform()  # x in axes fraction, y in data
    ax.text(1.02, hi.iloc[-1] / 2, t["seg_hi"], transform=tr, ha="left", va="center",
            fontsize=SIZE["label"], fontweight="bold", color=ORANGE, clip_on=False)
    ax.text(1.02, hi.iloc[-1] + lo.iloc[-1] / 2, t["seg_lo"], transform=tr, ha="left", va="center",
            fontsize=SIZE["label"], fontweight="bold", color=GREY_TEXT, clip_on=False)
    band_lines = t["band"].replace(" per tahun", "\nper tahun", 1)  # line break only; wording unchanged
    ax.text(1.02, (1755 + 3042) / 2 + 700, band_lines, transform=tr,
            ha="left", va="center", fontsize=SIZE["label"] - 1, color=ORANGE, clip_on=False, linespacing=1.15)
    total25 = hi.iloc[-1] + lo.iloc[-1]
    ax.annotate(fit_wrap(fig, t["label_2025"], SIZE["label"], max_frac=0.42), xy=(last - 0.38, total25),
                xytext=(last - 1.1, total25 - 400), ha="right", va="center", fontsize=SIZE["label"], color=INK,
                arrowprops={"arrowstyle": "-", "color": INK, "lw": 0.9, "relpos": (1, 0.5), "shrinkA": 3, "shrinkB": 2})

    ax.set_xlim(-0.6, last + 0.6)
    ax.set_ylim(0, 21500)
    ax.set_xticks(x[::2], [str(y) for y in years[::2]])
    ax.xaxis.set_minor_locator(FixedLocator(x))
    ax.tick_params(axis="x", which="both", length=3, color=GREY_TEXT)
    ax.yaxis.set_major_locator(FixedLocator([0, 5000, 10000, 15000, 20000]))
    ax.yaxis.set_major_formatter(ID_INT)
    ax.set_ylabel(t["y"])
    return save(fig, "f2_katalog_kelas_magnitudo")


# =============================================================================
# F3 — the fingerprint of detection
# =============================================================================
F3_TEXT = {
    "title": "Jaringan kini menangkap gempa yang lebih kecil, sementara gempa M4+ nyaris tidak bertambah",
    "subtitle": "Jumlah gempa per tahun di setiap magnitudo, 2014–2017 dibanding 2022–2025",
    "x": "Magnitudo",
    "y": "Gempa per tahun",
    "line_a": "2014–2017",
    "line_b": "2022–2025",
    "arrow": "Puncak bergeser: M3,4 → M3,0",
    "region_left": "Di bawah M4: kini jauh lebih banyak yang “terdengar”",
    "region_right": "M4+: kedua garis berdekatan",
    "note": "Magnitudo dibulatkan ke 0,1. Dengan satu jenis magnitudo saja (MLv), puncak bergeser dari M3,4 (2014–2017) ke "
            "M2,7 (2025). Gempa di atas M6,0 (±5 per tahun pada 2014–2017, ±13 pada 2022–2025) dan di bawah M1,0 (±3 per "
            "tahun pada 2022–2025) tidak digambar.",
    "source": SOURCE_CATALOG,
}


def f3_bins(ev: pd.DataFrame, years: range) -> pd.Series:
    """Events per year in each 0,1 magnitude bin from M1,0 to M6,0 (period of complete years)."""
    tenths = (ev[ev.year.isin(years)].mag1 * 10).round().astype(int)
    counts = tenths.value_counts() / len(years)
    grid = np.arange(10, 61)
    return pd.Series(counts.reindex(grid, fill_value=0).values, index=grid / 10)


def f3() -> Path:
    t = F3_TEXT
    _, ev = catalog()
    (a0, a1), (b0, b1) = PERIODS
    ya, yb = f3_bins(ev, range(a0, a1 + 1)), f3_bins(ev, range(b0, b1 + 1))

    fig, ax = frame(5.9, t)
    ax.axvspan(1.0, 3.95, color=TINT["grey35"], lw=0, zorder=0.5)
    ax.axvspan(3.95, 6.0, color=TINT["orange10"], lw=0, zorder=0.5)
    ax.plot(ya.index, ya.values, ls=(0, (4, 2.5)), color=GREY_TEXT, lw=1.7, zorder=3)
    ax.plot(yb.index, yb.values, color=INK, lw=2.6, zorder=4)

    pa, pb = ya.idxmax(), yb.idxmax()
    ax.annotate("", xy=(pb + 0.03, yb[pb] - 18), xytext=(pa, ya[pa] + 22),
                arrowprops={"arrowstyle": "-|>", "color": INK, "lw": 1.2, "mutation_scale": 12,
                            "connectionstyle": "arc3,rad=-0.25"}, zorder=5)
    ax.text(pa + 0.14, 560, t["arrow"], ha="left", va="center", fontsize=SIZE["label"], color=INK, zorder=6)
    ax.text(2.38, 470, t["line_b"], ha="right", va="center", fontsize=SIZE["label"], fontweight="bold", color=INK)
    ax.text(pa - 0.25, ya[pa] + 6, t["line_a"], ha="right", va="bottom", fontsize=SIZE["label"], fontweight="bold",
            color=GREY_TEXT)
    ax.text(1.08, 690, fit_wrap(fig, t["region_left"], SIZE["label"], max_frac=0.36), ha="left", va="top",
            fontsize=SIZE["label"], color=GREY_TEXT, linespacing=1.2)
    ax.text(5.92, 690, fit_wrap(fig, t["region_right"], SIZE["label"], max_frac=0.24), ha="right", va="top",
            fontsize=SIZE["label"], color=ORANGE, linespacing=1.2)

    ax.set_xlim(1.0, 6.0)
    ax.set_ylim(0, 700)
    ax.xaxis.set_major_locator(FixedLocator([1, 2, 3, 4, 5, 6]))
    ax.xaxis.set_major_formatter(ID_DEC1)
    ax.yaxis.set_major_locator(FixedLocator([0, 100, 200, 300, 400, 500, 600, 700]))
    ax.yaxis.set_major_formatter(ID_INT)
    ax.set_xlabel(t["x"])
    ax.set_ylabel(t["y"])
    return save(fig, "f3_distribusi_magnitudo")


# =============================================================================
# F4 — more ears per quake
# =============================================================================
F4_TEXT = {
    "title": "Gempa berukuran sama kini terekam oleh dua kali lebih banyak bacaan seismik",
    "subtitle": "Median jumlah bacaan fase untuk gempa M4,0–M4,9, per tahun, 2009–2025",
    "y": "Bacaan fase (median)",
    "period_a": "2014–2017: median 20",
    "period_b": "2022–2025: median 44",
    "ribbon": "Separuh gempa berada di dalam pita ini",
    "note": "Bacaan fase adalah kedatangan gelombang seismik di stasiun yang dipakai untuk menentukan lokasi gempa. Dengan satu "
            "jenis magnitudo saja (MLv): 18 (2014–2017) → 42 (2025). Perubahan sistem pengolahan juga dapat menambah jumlah bacaan.",
    "source": SOURCE_CATALOG,
}


def f4() -> Path:
    t = F4_TEXT
    _, ev = catalog()
    m45 = ev[(ev.mag1 >= 4.0) & (ev.mag1 <= 4.9) & ev.year.between(2009, 2025)]
    q = m45.groupby("year").phasecount.quantile([0.25, 0.5, 0.75]).unstack()

    fig, ax = frame(5.6, t)
    for (a, b), lbl in zip(PERIODS, (t["period_a"], t["period_b"])):
        ax.axvspan(a - 0.5, b + 0.5, color=TINT["slate8"], lw=0, zorder=0.5)
        ax.text((a + b) / 2, 89, lbl.replace(": ", ":\n", 1), ha="center", va="top", fontsize=SIZE["label"],
                color=GREY_TEXT, linespacing=1.15)  # line break only; wording unchanged
    ax.fill_between(q.index, q[0.25], q[0.75], color=TINT["orange20"], lw=0, zorder=2)
    ax.plot(q.index, q[0.5], color=ORANGE, lw=2.2, marker="o", markersize=5.5, markeredgecolor=BG,
            markeredgewidth=1, zorder=4)
    ax.annotate(t["ribbon"], xy=(2011, q.loc[2011, 0.75] - 1.5), xytext=(2009.0, 41), ha="left", va="bottom",
                fontsize=SIZE["label"], color=ORANGE,
                arrowprops={"arrowstyle": "-", "color": ORANGE, "lw": 0.9, "relpos": (0.25, 0), "shrinkA": 2, "shrinkB": 1})

    ax.set_xlim(2008.5, 2025.5)
    ax.set_ylim(0, 90)
    ax.xaxis.set_major_locator(FixedLocator(range(2009, 2026, 2)))
    ax.xaxis.set_minor_locator(FixedLocator(range(2009, 2026)))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}"))
    ax.tick_params(axis="x", which="both", length=3, color=GREY_TEXT)
    ax.yaxis.set_major_locator(FixedLocator([0, 20, 40, 60, 80]))
    ax.set_ylabel(t["y"])
    return save(fig, "f4_bacaan_fase")


# =============================================================================
# F5 — what a real surge looks like
# =============================================================================
F5_TEXT = {
    "title": "Lonjakan sungguhan terlihat berbeda: singkat, lokal, dan muncul pada gempa M4+",
    "subtitle": "Gempa M4+ per bulan, November 2008 – Juli 2026",
    "y": "Gempa M4+ per bulan",
    "median": "Bulan biasa: ±180 gempa M4+",
    "note": "Bulan dengan data tidak lengkap disetarakan ke satu bulan penuh; garis terputus pada bulan dengan data kurang dari "
            "15 hari (Sep 2009, Jul–Agu 2013). Label: bulan dengan gempa M4+ setidaknya 1,75 kali bulan biasa, dinamai menurut "
            "rangkaian gempa penyumbang terbesar. Wilayah analisis mencakup sebagian Filipina selatan.",
    "source": SOURCE_CATALOG,
}
# month -> (label text, label x in decimal years, label y, ha, two_lines).
# Positions avoid collisions; labels above y = 400 sit in the headroom over the plot.
# two_lines breaks the label before " · " (name / "· date"); every character is kept.
F5_SPIKES = {
    "2010-10": ("Mentawai · Okt 2010", 2011.2, 337, "left", False),
    "2018-08": ("Lombok · Agu 2018", 2018.35, 372, "right", False),
    "2019-07": ("Halmahera & Laut Maluku · Jul 2019", 2019.3, 424, "right", True),
    "2019-11": ("Laut Maluku · Nov 2019", 2019.95, 470, "right", False),
    "2023-01": ("Laut Maluku & Talaud · Jan 2023", 2020.3, 424, "left", True),
    "2026-06": ("Mindanao, Filipina · Jun 2026", 2026.6, 470, "right", True),
}


def decimal_year(p: pd.Period) -> float:
    return p.year + (p.month - 0.5) / 12


def f5() -> Path:
    t = F5_TEXT
    days, ev = catalog()
    mc = clean.monthly_counts(ev[ev.mag1 >= 4], days, "2008-11", "2026-07")
    xs = np.array([decimal_year(m) for m in mc.index])
    drawn = mc[~mc.gap]["count"]
    med = float(drawn.median())

    fig, ax = frame(5.6, t, right=0.79, gap_top=0.12)
    ax.plot(xs, mc["count"].values, color=ORANGE, lw=1.3, zorder=3)  # NaN gap months break the line
    ax.axhline(med, color=GREY_TEXT, lw=1.1, ls=(0, (4, 3)), zorder=2)
    ax.text(1.02, med, t["median"].replace(": ", ":\n", 1), transform=ax.get_yaxis_transform(), ha="left", va="center",
            fontsize=SIZE["label"] - 1, color=GREY_TEXT, clip_on=False, linespacing=1.15)
    size = SIZE["label"] - 1
    for m, (lbl, lx, ly, ha, two_lines) in F5_SPIKES.items():
        p = pd.Period(m, "M")
        px, py = decimal_year(p), float(mc.loc[p, "count"])
        text = lbl.replace(" · ", "\n· ", 1) if two_lines else lbl
        ax.plot([px], [py], marker="o", markersize=6.5, color=ORANGE, markeredgecolor=BG, markeredgewidth=1.2, zorder=5)
        ax.annotate(text, xy=(px, py), xytext=(lx, ly), ha=ha, va="center", fontsize=size, color=INK, zorder=6,
                    linespacing=1.1, annotation_clip=False,
                    arrowprops={"arrowstyle": "-", "color": INK, "lw": 0.7, "shrinkA": 1, "shrinkB": 4,
                                "relpos": (1 if ha == "right" else 0, 0.5)})

    ax.set_xlim(2008.7, 2026.7)
    ax.set_ylim(0, 400)
    ax.xaxis.set_major_locator(FixedLocator(range(2010, 2027, 2)))
    ax.xaxis.set_minor_locator(FixedLocator(range(2009, 2027)))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}"))
    ax.tick_params(axis="x", which="both", length=3, color=GREY_TEXT)
    ax.yaxis.set_major_locator(FixedLocator([0, 100, 200, 300, 400]))
    ax.set_ylabel(t["y"])
    return save(fig, "f5_m4_per_bulan")


# =============================================================================
# F6 — reading the 2026 number
# =============================================================================
F6_TEXT = {
    "title": "Laju gempa M4+ 2026 masih dalam rentang biasanya — dan “biasa” bagi Indonesia sudah tinggi",
    "subtitle": "Gempa M4+ per tahun, 2009–2025, dan laju 2026 hingga 14 Agustus",
    "x": "Gempa M4+ per tahun",
    "label_min": "2013: 1.755",
    "label_max": "2019: 3.042",
    "label_2026": "2026 (s.d. 14 Agu): ±2.430",
    "band": "Rentang 2009–2025",
    "median": "Median: 2.159 per tahun ≈ 6 gempa M4+ setiap hari",
    "note": "Laju 2026 dihitung dari 1 Januari–14 Agustus 2026 dan disetarakan ke satu tahun penuh; angka akhirnya bisa berbeda.",
    "source": SOURCE_CATALOG,
}


def f6() -> Path:
    t = F6_TEXT
    days, ev = catalog()
    hi = ev[ev.mag1 >= 4]
    yearly = clean.yearly_counts(hi, days, range(2009, 2026))
    pace26 = clean.pace(hi, days, 2026)
    lo_v, hi_v, med = yearly.min(), yearly.max(), yearly.median()

    fig, ax = frame(3.9, t, left=0.04, right=0.96, gap_bottom=0.13)
    ax.grid(False)
    ax.add_patch(Rectangle((lo_v, -0.22), hi_v - lo_v, 0.44, facecolor=TINT["grey35"], edgecolor="none", zorder=1))
    ax.text(hi_v, -0.3, t["band"], ha="right", va="top", fontsize=SIZE["label"] - 0.5, color=GREY_TEXT)
    ax.plot([med, med], [-0.62, 0.3], color=INK, lw=1.3, zorder=2)
    ax.text(med, -0.66, t["median"], ha="center", va="top", fontsize=SIZE["label"] - 0.5, color=INK)
    ax.scatter(yearly.values, np.zeros(len(yearly)), s=70, color=TINT["orange45"], edgecolor=BG, linewidth=1.2, zorder=3)
    ax.scatter([pace26], [0], s=130, marker="D", color=ORANGE, edgecolor=BG, linewidth=1.2, zorder=4)
    for xv, lbl, w in [(lo_v, t["label_min"], "normal"), (hi_v, t["label_max"], "normal"), (pace26, t["label_2026"], "bold")]:
        ax.annotate(lbl, xy=(xv, 0.1), xytext=(xv, 0.62), ha="center", va="bottom", fontsize=SIZE["label"],
                    fontweight=w, color=ORANGE if w == "bold" else INK,
                    arrowprops={"arrowstyle": "-", "color": INK, "lw": 0.7, "shrinkA": 1, "shrinkB": 2})

    ax.set_xlim(1600, 3200)
    ax.set_ylim(-1.05, 1.05)
    ax.spines["left"].set_visible(False)
    ax.set_yticks([])
    ax.xaxis.set_major_locator(FixedLocator(range(1600, 3201, 200)))
    ax.xaxis.set_major_formatter(ID_INT)
    ax.set_xlabel(t["x"])
    return save(fig, "f6_laju_m4_2026")


# =============================================================================
# F-X — discarded figure (appendix)
# =============================================================================
FX_TEXT = {
    "title": "Jumlah kode stasiun BMKG di wilayah Indonesia naik lebih dari tiga kali lipat sejak 2017",
    "subtitle": "Kode stasiun kumulatif menurut tanggal berlaku paling awal, 2008–2025",
    "y": "Kode stasiun (kumulatif)",
    "label_2017": "2017: 369",
    "label_2025": "2025: 1.314",
    "ratio": "×3,6",
    "note": "35 kode bertanggal 1 Januari 1970 atau 1 Januari 1980 (tanggal pengganti) tidak dihitung. Sekitar 60% tanggal jatuh "
            "pada 1 Januari, sehingga ketepatannya hanya per tahun. Tabel ini mencampur seismograf dengan jenis sensor lain.",
    "source": "Sumber: Tabel stasiun BMKG (katalog_sensor.tsv), dihimpun A. K. Vigiliant, Kaggle, doi:10.34740/kaggle/ds/1934565; "
              "diunduh 28 Oktober 2026. Olahan: Hanjani & Azizah.",
    "heading": "Gambar yang kami buang",
    "reason": "Gambar ini tampak membuktikan jaringan makin rapat, tetapi tabelnya mencampur seismograf dengan sensor jenis lain, "
              "tanggalnya bukan tanggal pemasangan, dan angkanya berbeda dengan jumlah sensor yang disebut BMKG. Gambar ini akan "
              "memindahkan perdebatan ke soal berapa jumlah alat, yang tidak bisa dijawab data ini. Kami menggantinya dengan "
              "Gambar 4, yang memakai ukuran dari katalog itu sendiri.",
}


def station_first_dates() -> pd.Series:
    """Earliest effective date per station code inside the box; placeholder dates (1970/1980-01-01) removed."""
    sen = pd.read_csv(RAW / "katalog_sensor.tsv", sep="\t", dtype=str, keep_default_na=False)
    for c in ("latitude", "longitude"):
        sen[c] = pd.to_numeric(sen[c], errors="coerce")
    sen["eff"] = pd.to_datetime(sen.datetime, format="ISO8601")  # 50 rows carry fractional seconds
    first = sen[clean.in_box(sen)].groupby("code").eff.min()
    placeholder = first.dt.strftime("%m-%d").eq("01-01") & first.dt.year.isin([1970, 1980])
    return first[~placeholder].sort_values()


def fx() -> Path:
    t = FX_TEXT
    first = station_first_dates()
    start, end = pd.Timestamp("2008-01-01"), pd.Timestamp("2025-12-31 23:59:59")
    steps = pd.concat([pd.Series([start]), first[(first > start) & (first <= end)], pd.Series([end])]).reset_index(drop=True)
    cum = [int((first <= d).sum()) for d in steps]
    xs = [d.year + (d.dayofyear - 1) / 366 for d in steps]

    fig, ax = frame(5.0, t)
    ax.step(xs, cum, where="post", color=SLATE, lw=2.0, zorder=3)
    for yr, lbl in [(2017, t["label_2017"]), (2025, t["label_2025"])]:
        v = int((first <= pd.Timestamp(f"{yr}-12-31 23:59:59")).sum())
        ax.plot([yr + 1], [v], marker="o", markersize=6.5, color=SLATE, markeredgecolor=BG, markeredgewidth=1.2, zorder=4)
        ax.text(yr + 1 - 0.2, v + 45, lbl, ha="right", va="bottom", fontsize=SIZE["label"], color=INK)
    v17 = int((first <= pd.Timestamp("2017-12-31 23:59:59")).sum())
    v25 = int((first <= end).sum())
    # arrow from the 2017 point to the 2025 point, bowed below the step line
    ax.annotate("", xy=(2026.0, v25), xytext=(2018.0, v17),
                arrowprops={"arrowstyle": "-|>", "color": INK, "lw": 1.0, "mutation_scale": 11,
                            "connectionstyle": "arc3,rad=0.28", "shrinkA": 7, "shrinkB": 7})
    ax.text(2023.4, 560, t["ratio"], ha="left", va="center", fontsize=SIZE["label"] + 1.5, fontweight="bold", color=INK)

    ax.set_xlim(2008, 2026.4)
    ax.set_ylim(0, 1500)
    ax.xaxis.set_major_locator(FixedLocator(range(2008, 2027, 2)))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}"))
    ax.yaxis.set_major_locator(FixedLocator([0, 500, 1000, 1500]))
    ax.yaxis.set_major_formatter(ID_INT)
    ax.set_ylabel(t["y"])
    path = save(fig, "discarded/fx_kode_stasiun")
    (FIGURES / "discarded" / "REASON.md").write_text(
        f"# {t['heading']}\n\n![{t['title']}](fx_kode_stasiun.png)\n\n**Alasan dibuang:** {t['reason']}\n\n"
        "_Text verbatim from `docs/figure-text.md` (F-X); written by the group._\n")
    return path


FIGURE_FUNCTIONS = {"f1": f1, "f2": f2, "f3": f3, "f4": f4, "f5": f5, "f6": f6, "fx": fx}


def build_all() -> list[Path]:
    return [fn() for fn in FIGURE_FUNCTIONS.values()]


if __name__ == "__main__":
    for p in build_all():
        print(p.relative_to(ROOT))
