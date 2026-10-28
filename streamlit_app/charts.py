"""Matplotlib figures for the Streamlit version. Same marks, colors and labels as site/ and exports/, drawn plot-only
(title, subtitle, note and source are page text) at a narrow size so the labels stay legible on phones."""
import io
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects

COL = dict(strong="#C2410C", small="#B8BEC6", small_text="#6B7280", neutral="#475569", strong20="#F3D9CE",
           strong_tint="#F9ECE7", strong45="#E4AA92", small35="#E6E8EB", neutral8="#F0F1F3", grid="#E5E7EB",
           dark="#1F2937", text="#374151", label="#4B5563")
MONTHS = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
HALO = [patheffects.withStroke(linewidth=3, foreground="white")]   # white halo behind annotations
W = 6.4                                                            # figure width in inches
FS = 10                                                            # annotation font size

plt.rcParams.update({
    "font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#9CA3AF",
    "xtick.color": "#6B7280", "ytick.color": "#6B7280", "xtick.labelsize": 9, "ytick.labelsize": 9,
    "axes.labelcolor": "#4B5563", "axes.labelsize": 9.5, "axes.labelweight": "bold",
})


def id_int(v):
    return f"{int(round(v)):,}".replace(",", ".")


def id_dec(v, digits=1):
    return f"{v:.{digits}f}".replace(".", ",")


def _style(ax, grid="y"):
    if grid:
        ax.grid(axis=grid, color=COL["grid"], linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)


def _yfmt(ax):
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: id_int(v)))


def _panel_title(ax, title, axis_title):
    t = ax.text(0, 1.05, title, transform=ax.transAxes, fontsize=FS, fontweight="bold", color=COL["text"], va="bottom")
    ax.annotate(axis_title, xy=(1, 0), xycoords=t, xytext=(8, 0), textcoords="offset points", fontsize=8.5,
                color=COL["small_text"], va="bottom")


def png(fig, dpi=220):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def g1(d, variant="final"):
    """variant 'guess': top panel with 2024 highlighted and an empty bottom panel with '?'; 'final': both panels."""
    final = variant == "final"
    yrs = [r["year"] for r in d["years"]]
    xs = np.arange(len(yrs))
    tot = [r["total"] for r in d["years"]]
    m5 = [r["m5plus"] for r in d["years"]]
    fig, (top, bot) = plt.subplots(2, 1, figsize=(W, 5.4), gridspec_kw=dict(height_ratios=[7, 3], hspace=0.42))
    fig.subplots_adjust(left=0.13, right=0.86, top=0.93, bottom=0.06)
    for ax in (top, bot):
        _style(ax)
        ax.set_xticks(xs, yrs)
        ax.set_xlim(-0.6, len(yrs) - 0.4)
    alpha = [1 if final or y == 2024 else 0.35 for y in yrs]
    for x_, v, a in zip(xs, tot, alpha):
        top.bar(x_, v, width=0.62, color=COL["neutral"], alpha=a)
        top.text(x_, v + 700, id_int(v), ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=COL["text"], alpha=a)
    top.set_ylim(0, 45000)
    top.set_yticks(range(0, 45001, 10000))
    _yfmt(top)
    _panel_title(top, "Semua gempa", "Gempa per tahun")
    i24 = yrs.index(2024)
    alt = d["years"][i24]["total_alt"]
    for c, lw in (("white", 3), (COL["neutral"], 1)):
        top.plot([i24 - 0.12, i24 - 0.42], [alt + 1100, 19500], color=c, lw=lw, zorder=3 if c == "white" else 4)
    top.scatter([i24], [alt], s=40, facecolor="white", edgecolor=COL["neutral"], linewidth=1.6, zorder=5)
    top.text(i24 - 0.4, 19900, "\n".join(textwrap.wrap("7.358 (angka akhir tahun, 31 Des 2024)", 20)), ha="right", va="bottom",
             fontsize=9, fontweight="bold", color=COL["neutral"], path_effects=HALO, zorder=6)
    bx = len(yrs) - 0.4 + 0.12
    top.plot([0, bx], [tot[0], tot[0]], ls=(0, (3, 3)), color="#9CA3AF", lw=1, clip_on=False)
    top.plot([bx - 0.08, bx, bx, bx - 0.08], [tot[0], tot[0], tot[-1], tot[-1]], color=COL["neutral"], lw=1.5, clip_on=False)
    top.text(bx + 0.12, (tot[0] + tot[-1]) / 2, "×5,3", fontsize=12.5, fontweight="bold", color=COL["neutral"], va="center")

    bot.set_ylim(0, 300)
    bot.set_yticks([0, 100, 200, 300])
    _yfmt(bot)
    _panel_title(bot, "Gempa M5+", "Gempa per tahun")
    if final:
        bot.bar(xs, m5, width=0.62, color=COL["strong"])
        for x_, v in zip(xs, m5):
            bot.text(x_, v + 8, id_int(v), ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=COL["strong"])
        bot.text(1, 1.05, "244 → 153", transform=bot.transAxes, ha="right", va="bottom", fontsize=11, fontweight="bold",
                 color=COL["strong"])
    else:
        bot.text(0.5, 0.5, "?", transform=bot.transAxes, ha="center", va="center", fontsize=26, fontweight="bold", color="#9CA3AF")
    return fig


def g2(d, variant="final"):
    """variant 'guess': totals only, faded; 'final': stacked M4+ / below M4 with the range band and the 2025 label."""
    final = variant == "final"
    yrs = [r["year"] for r in d["years"]]
    xs = np.arange(len(yrs))
    m4 = np.array([r["m4plus"] for r in d["years"]])
    b4 = np.array([r["below4"] for r in d["years"]])
    fig, ax = plt.subplots(figsize=(W, 4.6))
    fig.subplots_adjust(left=0.13, right=0.83, top=0.9, bottom=0.08)
    _style(ax)
    for a, b, lab in [(2014, 2017, "2014–2017"), (2022, 2025, "2022–2025")]:
        ax.axvspan(yrs.index(a) - 0.45, yrs.index(b) + 0.45, color=COL["neutral8"], zorder=0)
        ax.text((yrs.index(a) + yrs.index(b)) / 2, 20300, lab, ha="center", va="bottom", fontsize=8.5, fontweight="bold",
                color=COL["label"])
    ax.set_ylim(0, 20000)
    ax.set_yticks(range(0, 20001, 5000))
    _yfmt(ax)
    ax.set_ylabel("Gempa per tahun")
    ax.set_xticks(xs[::2], yrs[::2])
    ax.set_xlim(-0.6, len(yrs) - 0.4)
    if not final:
        ax.bar(xs, m4 + b4, width=0.68, color=COL["neutral"], alpha=0.3, zorder=2)
        return fig
    mn, mx = d["m4plus_min"]["value"], d["m4plus_max"]["value"]
    ax.axhspan(mn, mx, color=COL["strong20"], zorder=0.5)
    ax.bar(xs, m4, width=0.68, color=COL["strong"], edgecolor="white", linewidth=1, zorder=2)
    ax.bar(xs, b4, bottom=m4, width=0.68, color=COL["small"], edgecolor="white", linewidth=1, zorder=2)
    for v in (mn, mx):
        ax.axhline(v, color=COL["strong"], lw=1, ls=(0, (4, 3)), zorder=3)
    ax.text(-0.3, mx + 250, "M4+: 1.755–3.042 per tahun sejak 2009", fontsize=9, fontweight="bold", color=COL["strong"],
            va="bottom", zorder=4, path_effects=HALO)
    r25 = d["years"][-1]
    ax.text(len(yrs) - 0.4 + 0.2, r25["m4plus"] / 2, "M4+", color=COL["strong"], fontsize=9.5, fontweight="bold", va="center")
    ax.text(len(yrs) - 0.4 + 0.2, r25["m4plus"] + r25["below4"] / 2, "Di bawah\nM4", color=COL["small_text"], fontsize=9.5,
            fontweight="bold", va="center")
    ax.annotate("\n".join(textwrap.wrap("2025: total tertinggi (18.357), tetapi M4+ termasuk yang terendah (1.895)", 30)),
                xy=(len(yrs) - 1 - 0.36, r25["total"] - 200), xytext=(len(yrs) - 1.8, 19000), ha="right", va="top",
                fontsize=9, fontweight="bold", color=COL["text"], path_effects=HALO,
                arrowprops=dict(arrowstyle="-", color=COL["text"], lw=1, shrinkA=2, shrinkB=0))
    return fig


G3_TEXT = {"all": ("2014–2017", "2022–2025", "Puncak bergeser: M3,4 → M3,0", 700),
           "mlv": ("2014–2017 (MLv)", "2025 (MLv)", "Puncak bergeser: M3,4 → M2,7", 1100)}


def g3(d, variant="all"):
    """variant 'all' (every magnitude type) or 'mlv' (MLv only: 2014–2017 vs 2025)."""
    s = d["mlv"] if variant == "mlv" else d["all"]
    lab_a, lab_b, arrow_text, ymax = G3_TEXT[variant]
    m = np.array([p["m"] for p in s["A"]])
    va = np.array([p["per_year"] for p in s["A"]])
    vb = np.array([p["per_year"] for p in s["B"]])
    fig, ax = plt.subplots(figsize=(W, 4.6))
    fig.subplots_adjust(left=0.13, right=0.97, top=0.97, bottom=0.13)
    _style(ax)
    ax.axvspan(1, 4, color=COL["small35"], zorder=0)
    ax.axvspan(4, 6, color=COL["strong_tint"], zorder=0)
    ax.plot(m, va, color=COL["small_text"], lw=1.5, ls=(0, (5, 4)), zorder=3)
    ax.plot(m, vb, color=COL["dark"], lw=2.5, zorder=3)
    ax.set_xlim(1, 6)
    ax.set_ylim(0, ymax)
    ax.set_yticks(range(0, ymax + 1, 100 if ymax <= 700 else 200))
    _yfmt(ax)
    ax.set_xticks(range(1, 7), [id_dec(x) for x in range(1, 7)])
    ax.set_xlabel("Magnitudo")
    ax.set_ylabel("Gempa per tahun")
    ax.text(1.08, ymax * 0.98, "\n".join(textwrap.wrap("Di bawah M4: kini jauh lebih banyak yang “terdengar”", 20)), va="top",
            fontsize=9, fontweight="bold", color=COL["label"], path_effects=HALO)
    ax.text(4.1, 330, "\n".join(textwrap.wrap("M4+: kedua garis berdekatan", 16)), va="bottom", fontsize=9, fontweight="bold",
            color=COL["strong"], path_effects=HALO)
    ib = int(vb.argmax())
    rise = next(i for i in range(ib) if vb[i] >= 0.6 * vb[ib])
    ax.text(m[rise] - 0.08, vb[rise], lab_b, ha="right", va="center", fontsize=9.5, fontweight="bold", color=COL["dark"],
            path_effects=HALO)
    i36 = int(np.argmin(abs(m - 3.6)))
    ax.text(3.6, va[i36] - ymax * 0.02, lab_a, ha="center", va="top", fontsize=9.5, fontweight="bold", color=COL["small_text"],
            path_effects=HALO)
    ia = int(va.argmax())
    ax.annotate("", xy=(m[ib] + 0.06, vb[ib] - ymax * 0.01), xytext=(m[ia] + 0.03, va[ia] + ymax * 0.015),
                arrowprops=dict(arrowstyle="-|>", color=COL["text"], lw=1.3, connectionstyle="arc3,rad=0.35"))
    ax.text(m[ia] + 0.42, (va[ia] + vb[ib]) / 2, "\n".join(textwrap.wrap(arrow_text, 18)), fontsize=9.5, fontweight="bold",
            color=COL["text"], path_effects=HALO)
    return fig


def g4(d, variant="final"):
    yrs = np.array([r["year"] for r in d["years"]])
    med = np.array([r["median"] for r in d["years"]])
    q1 = np.array([r["q1"] for r in d["years"]])
    q3 = np.array([r["q3"] for r in d["years"]])
    fig, ax = plt.subplots(figsize=(W, 4.4))
    fig.subplots_adjust(left=0.12, right=0.97, top=0.96, bottom=0.08)
    _style(ax)
    for a, b, lab in [(2014, 2017, f"2014–2017: median {id_int(d['median_A'])}"),
                      (2022, 2025, f"2022–2025: median {id_int(d['median_B'])}")]:
        ax.axvspan(a - 0.45, b + 0.45, color=COL["neutral8"], zorder=0)
        ax.text((a + b) / 2, 1.5, "\n".join(textwrap.wrap(lab, 11)), ha="center", va="bottom", fontsize=9.5, fontweight="bold",
                color=COL["neutral"], path_effects=HALO, zorder=5)
    ax.fill_between(yrs, q1, q3, color=COL["neutral"], alpha=0.15, lw=0, zorder=1)
    ax.plot(yrs, med, color=COL["neutral"], lw=2.5, marker="o", ms=4.5, zorder=3)
    ax.set_ylim(0, 80)
    ax.set_yticks(range(0, 81, 20))
    ax.set_xlim(2008.5, 2025.5)
    ax.set_xticks(yrs[::2], yrs[::2])
    ax.set_ylabel("Bacaan fase (median)")
    r10 = d["years"][1]
    ax.annotate("\n".join(textwrap.wrap("Separuh gempa berada di dalam pita ini", 18)), xy=(2010, (r10["q1"] + r10["q3"]) / 2),
                xytext=(2009, 47), ha="left", va="bottom", fontsize=9, fontweight="bold", color=COL["neutral"],
                path_effects=HALO, arrowprops=dict(arrowstyle="-", color=COL["neutral"], lw=1, relpos=(0.15, 0)))
    return fig


def g5(d, variant="final"):
    """Monthly M4+ with gaps, the median line and the six spikes. Spike labels are short (place + month) at this width;
    the full name is in the spike card under the chart."""
    ms = [x for x in d["months"] if x["month"] <= d["last_month"]]
    t = np.array([int(x["month"][:4]) + (int(x["month"][5:]) - 1) / 12 for x in ms])
    v = np.array([np.nan if x["value"] is None else x["value"] for x in ms], dtype=float)
    fig, ax = plt.subplots(figsize=(W, 4.8))
    fig.subplots_adjust(left=0.12, right=0.97, top=0.72, bottom=0.08)
    _style(ax)
    ax.plot(t, v, color=COL["strong"], lw=1.1, zorder=3)
    ax.axhline(d["median"], color=COL["small_text"], lw=1.2, ls=(0, (5, 4)), zorder=2)
    ax.text(t[0] + 0.15, d["median"] + 6, "Bulan biasa: ±180 gempa M4+", fontsize=9, fontweight="bold", color=COL["label"],
            va="bottom", path_effects=HALO, zorder=5)
    ax.set_ylim(0, 400)
    ax.set_yticks(range(0, 401, 100))
    x0, x1 = t[0], t[-1] + 0.1
    ax.set_xlim(x0, x1)
    ax.set_xticks(range(2010, 2027, 4), range(2010, 2027, 4))
    ax.set_ylabel("Gempa M4+ per bulan")
    # labels in two alternating tiers above the plot, pushed apart where they would overlap
    axis_in = W * (0.97 - 0.12)
    labels = []
    for i, s in enumerate(sorted(d["spikes"], key=lambda s: s["month"])):
        ts = int(s["month"][:4]) + (int(s["month"][5:]) - 1) / 12
        l1 = s["label"].split(" & ")[0].split(",")[0]
        l2 = f"{MONTHS[int(s['month'][5:]) - 1]} {s['month'][:4]}"
        width = (max(len(l1), len(l2)) * 0.62 * 8.5 / 72) / axis_in * (x1 - x0) + 0.3
        labels.append(dict(s=s, ts=ts, text=f"{l1}\n{l2}", w=width, tier=i % 2, cx=ts))
    for tier in (0, 1):
        row = [L for L in labels if L["tier"] == tier]
        for L in row:
            L["cx"] = min(max(L["cx"], x0 + L["w"] / 2), x1 - L["w"] / 2)
        for a, b in zip(row, row[1:]):
            b["cx"] = max(b["cx"], a["cx"] + (a["w"] + b["w"]) / 2)
        for a, b in reversed(list(zip(row, row[1:]))):
            if b["cx"] > x1 - b["w"] / 2:
                b["cx"] = x1 - b["w"] / 2
            a["cx"] = min(a["cx"], b["cx"] - (a["w"] + b["w"]) / 2)
    for L in labels:
        ax.scatter([L["ts"]], [L["s"]["value"]], s=34, color=COL["strong"], edgecolor="white", linewidth=1.1, zorder=4)
        ax.annotate(L["text"], xy=(L["ts"], L["s"]["value"] + 9), xycoords="data", xytext=(L["cx"], 1.04 + 0.17 * (1 - L["tier"])),
                    textcoords=("data", "axes fraction"), annotation_clip=False, ha="center", va="bottom", fontsize=8.5,
                    fontweight="bold", color=COL["text"], path_effects=HALO,
                    arrowprops=dict(arrowstyle="-", color=COL["text"], lw=0.8, shrinkA=1, shrinkB=0))
    return fig


def g6(d, variant="final"):
    vals = np.array([r["m4plus"] for r in d["years"]])
    fig, ax = plt.subplots(figsize=(W, 3.7))
    fig.subplots_adjust(left=0.04, right=0.96, top=0.98, bottom=0.17)
    _style(ax, grid="x")
    ax.spines["left"].set_visible(False)
    ax.set_yticks([])
    ax.set_xlim(1600, 3200)
    ax.set_ylim(-0.72, 0.95)
    ax.set_xticks(range(1600, 3201, 200), [id_int(x) for x in range(1600, 3201, 200)], fontsize=8.5)
    ax.set_xlabel("Gempa M4+ per tahun")
    mn, mx = d["min"]["value"], d["max"]["value"]
    ax.add_patch(plt.Rectangle((mn, -0.3), mx - mn, 0.6, color=COL["small35"], zorder=0))
    ax.text(mx - 25, -0.27, "Rentang 2009–2025", ha="right", va="bottom", fontsize=8.5, fontweight="bold", color=COL["label"])
    ax.plot([d["median"]] * 2, [-0.38, 0.38], color=COL["small_text"], lw=2, zorder=2)
    ax.text(d["median"], -0.45, "\n".join(textwrap.wrap("Median: 2.159 per tahun ≈ 6 gempa M4+ setiap hari", 30)), ha="center",
            va="top", fontsize=9.5, fontweight="bold", color=COL["text"], path_effects=HALO)
    # vertical jitter only where dots would overlap (same rule as the page)
    axis_in = W * 0.92
    dot_x = (np.sqrt(80) / 72) / axis_in * 1600 * 1.08
    dot_y = (np.sqrt(80) / 72) / (3.7 * 0.81) * 1.8 * 1.08
    placed, ys = [], []
    for x_ in vals:
        k = 0
        while True:
            off = 0 if k == 0 else (1 if k % 2 else -1) * ((k + 1) // 2) * dot_y
            if not any(abs(px - x_) < dot_x and abs(po - off) < dot_y * 0.95 for px, po in placed):
                break
            k += 1
        placed.append((x_, off))
        ys.append(off)
    ax.scatter(vals, ys, s=80, color=COL["strong45"], zorder=3, linewidth=0)
    ax.text(mn - 8, 0.36, "2013: 1.755", ha="left", va="bottom", fontsize=9.5, fontweight="bold", color=COL["text"], path_effects=HALO)
    ax.text(mx + 8, 0.36, "2019: 3.042", ha="right", va="bottom", fontsize=9.5, fontweight="bold", color=COL["text"], path_effects=HALO)
    ax.scatter([d["pace_2026"]], [0], marker="D", s=105, color=COL["strong"], edgecolor="white", linewidth=1.2, zorder=4)
    ax.annotate("2026 (s.d. 14 Agu): ±2.430", xy=(d["pace_2026"], 0.1), xytext=(d["pace_2026"], 0.66), ha="center", va="bottom",
                fontsize=10.5, fontweight="bold", color=COL["strong"], path_effects=HALO,
                arrowprops=dict(arrowstyle="-", color=COL["strong"], lw=1))
    return fig


def gx(d, variant="final"):
    yrs = np.array([r["year"] for r in d["years"]])
    codes = np.array([r["codes"] for r in d["years"]])
    fig, ax = plt.subplots(figsize=(W, 4.2))
    fig.subplots_adjust(left=0.14, right=0.86, top=0.96, bottom=0.08)
    _style(ax)
    ax.step(yrs, codes, where="post", color=COL["neutral"], lw=2.2, zorder=3)
    c17, c25 = d["y2017"], d["y2025"]
    ax.scatter([2017, 2025], [c17, c25], s=26, color=COL["neutral"], zorder=4)
    ax.text(2016.8, c17 + 30, "2017: 369", ha="right", va="bottom", fontsize=9.5, fontweight="bold", color=COL["neutral"],
            path_effects=HALO)
    ax.text(2024.8, c25 + 30, "2025: 1.314", ha="right", va="bottom", fontsize=9.5, fontweight="bold", color=COL["neutral"],
            path_effects=HALO)
    bx = 2025.6
    ax.plot([2017, bx], [c17, c17], ls=(0, (3, 3)), color="#9CA3AF", lw=1, clip_on=False)
    ax.plot([bx - 0.2, bx, bx, bx - 0.2], [c17, c17, c25, c25], color=COL["neutral"], lw=1.5, clip_on=False)
    ax.text(bx + 0.3, (c17 + c25) / 2, "×3,6", fontsize=12.5, fontweight="bold", color=COL["neutral"], va="center")
    ax.set_xlim(2008, 2025.2)
    ax.set_ylim(0, 1400)
    ax.set_yticks(range(0, 1401, 200))
    _yfmt(ax)
    ax.set_xticks(range(2008, 2026, 4), range(2008, 2026, 4))
    ax.set_ylabel("Kode stasiun (kumulatif)")
    return fig


FIGURES = {"g1": g1, "g2": g2, "g3": g3, "g4": g4, "g5": g5, "g6": g6, "gx": gx}
