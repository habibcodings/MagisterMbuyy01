# Storyboard & Design Justification

**Kelompok:** Yasmina Arethaya Hanjani · Cut Nabilah Nuur Azizah
**Judul:** *Bukan Bumi yang Makin Gaduh, Telinga Kita yang Makin Tajam*

**Main message (printed as the first sentence of the story):**
> Jumlah gempa yang diumumkan BMKG naik lima kali lipat dari 2020 ke 2025, tetapi menurut angka BMKG sendiri gempa M5 ke atas justru turun dari 244 menjadi 153, sehingga yang bertambah adalah gempa kecil yang kini lebih banyak terekam, bukan gempa yang lebih kuat.

**Format:** a static, long-form web article (exportable to PDF), in Bahasa Indonesia, single column. It has **6 figures**, plus 1 discarded figure in the appendix.

**Why static:** the story makes one fixed argument. Interactivity would turn it into a dashboard.

**Two data sources, two roles:**

- **BMKG's annual release figures (F1).** These are the numbers the audience actually prints: totals plus BMKG's own M5+ split, taken from press reports and cited in §6.
- **The registered dataset, BMKG's public RepoGempa catalog (F2–F6).** This is the 17-year, event-level evidence that explains those numbers.
- **The link between them.** The catalog matches BMKG's year-end totals for 2020–2024 within 5% (§5).

> Process note: all numbers come from exploratory tables; no figure has been drawn yet. Every piece of visible figure text is specified word for word in `figure-text.md`.

---

## 1. Story arc

| Part | Role | Key sentence (kalimat kunci) | Figure |
|---|---|---|---|
| Opening | Claim and hook | The main message, then the lede: the 29.869 headline of January 2025 and the 43.439 that followed. | (none) |
| **Setup** | The number reporters print | "Angka yang diumumkan BMKG naik lima kali lipat hanya dalam lima tahun." | F1 (top panel) |
| **Conflict 1** | BMKG's own split | "Tetapi menurut rilis yang sama, gempa M5+ justru turun." | F1 (bottom panel) |
| **Conflict 2** | The long view in the public catalog | "Katalog publik BMKG menunjukkan pola yang sama sejak 2009, sampai ke M4." | F2 |
| *(bridge, text only)* | BMKG's counter-argument, stated fairly | "Kepala BMKG saat itu menyatakan kenaikan ini bukan karena alat bertambah. Mari lihat jejak yang direkam katalognya sendiri." | (none) |
| **Conflict 3** | The fingerprint of detection | "Yang bertambah hanya sisi kiri kurva, yaitu gempa-gempa kecil, juga dalam satu jenis magnitudo yang sama." | F3 |
| **Conflict 4** | The mechanism | "Gempa berukuran sama kini terekam oleh dua kali lebih banyak bacaan seismik." | F4 |
| **Resolution 1** | What a real increase looks like | "Lonjakan yang layak jadi judul berita punya nama, tempat, dan akhir." | F5 |
| **Resolution 2** | How to read January 2027 | "'Biasa' bagi Indonesia sudah tinggi, dan itulah alasan untuk bersiap." | F6 + checklist box |
| Closing | Sources, limitations, discarded figure | (none) | Appendix |

---

## 2. Visual system (final)

### Counting rules

- **F1** uses BMKG's release figures exactly as published, with no rescaling.
- **F2–F6** count catalog events inside lat −11° to 6°, lon 94° to 142°.
  - Magnitudes are rounded to one decimal, as BMKG publishes them; "M4+" means M4,0 or more.
  - The 923 events without a magnitude are excluded everywhere.
  - Incomplete years and months are scaled to full calendar length: count × (days in period ÷ days with data). Complete periods show raw counts.
  - Months with fewer than 15 days of data are gaps.
- **Comparison periods:** 2014–2017 vs 2022–2025, two full, gap-free windows. They are used identically in F2, F3 and F4.

### Palette

| Role | Hex | Use |
|---|---|---|
| **Stronger quakes**: M5+ in BMKG releases, M4+ in the catalog | `#C2410C` | Fills, lines, labels (5,2:1 contrast on white) |
| **Smaller quakes** (below the threshold) | `#B8BEC6` | Fills only; directly labeled |
| Text for the grey category, axes, notes | `#6B7280` | 4,8:1 on white |
| Totals not split by size (F1 top, F-X) | `#475569` | |
| Titles and annotations | `#1F2937` | |
| Gridlines and background | `#E5E7EB` / `#FFFFFF` | |
| Tints | `#F9ECE7` (orange 10%), `#F3D9CE` (orange 20%), `#E4AA92` (orange 45%), `#E6E8EB` (grey 35%), `#F0F1F3` (slate 8%) | Per figure, below |

- Stacked segments are separated by a 1 px white stroke.
- The two colors differ strongly in lightness, so they stay distinguishable in greyscale and for color-blind readers.
- Orange always means "the stronger quakes": readers learn this in F1 and carry it through F6.

### Text conventions

- Titles state findings (in Bahasa Indonesia). Subtitles give measure, unit and scope.
- Each figure has a note line and a source line.
- One highlight per figure, with direct labels instead of legends.
- Indonesian number format everywhere, including axes: 1.755, M3,4, ×2,1, ranges with en dashes, month abbreviations Jan–Des.

---

## 3. Figures

### F1 — Setup and first turn: the number reporters print

- **Question:** What happened to BMKG's announced yearly total, and to BMKG's own count of stronger quakes?
- **Data:** BMKG release figures for 2020–2025 (§6): total, and M5+.
  - Totals: 8.264 · 10.570 · 10.792 · 10.789 · 29.869 · 43.439.
  - M5+: 244 · 244 · 205 · 219 · 186 · 153.
  - For 2024 BMKG published two totals: 7.358 (year-end, 31 Des 2024) and 29.869 (17 Jan 2025).
- **Chart form and why:** two vertically aligned column panels sharing the year axis, each with its own y-axis starting at zero. The top panel (total) is about three times the height of the bottom one (M5+).
  - The two quantities differ by a factor of 30–280, so on one axis M5+ would be invisible.
  - Separate zero-based panels keep each honest while the shared x-axis lets readers compare direction year by year.
  - *Rejected:* a stacked column. M5+ is below 1% of the 2025 column.
  - *Rejected:* a dual axis. It invites comparing bar heights that are not comparable.
  - *Rejected:* an index line (2020 = 100). It hides the absolute numbers reporters quote, and the 2024 double figure breaks the line.
- **Directing attention:**
  - Top columns are slate.
  - The 2024 column shows 29.869, with a hollow slate marker at 7.358 and a label explaining the two figures.
  - A "×5,3" bracket runs from 2020 to 2025.
  - Bottom columns are orange, with a "244 → 153" label.
  - Reading order: the top bracket, then down to the bottom label.

```
 Semua gempa (rilis BMKG)
 45.000 |                                      43.439
        |                                        ##
 30.000 |                             29.869     ##
        |                               ##       ##
 15.000 |         10.570 10.792 10.789  ##       ##
        |  8.264    ##     ##     ##    ## o 7.358
        |    ##     ##     ##     ##    ##       ##
        +-------------------------------------------- 
 Gempa M5+
    300 |   244    244
        |    ##     ##    205    219    186      153
        |    ##     ##     ##     ##     ##       ##
        +--------------------------------------------
           2020   2021   2022   2023   2024     2025
```

---

### F2 — Conflict 2: the same pattern in the public catalog, since 2009

- **Question:** Over a longer period and at a finer threshold (M4), which quakes increased?
- **Data:** catalog, year × count, split into below M4 / M4+, 2009–2025.
- **Chart form and why:** stacked columns with **M4+ at the bottom**. Because M4+ sits on the zero baseline, its flatness can be read directly, and the total stays visible.
  - *Rejected:* a 100% stacked chart (M4+ would look like it declines).
  - *Rejected:* two separate lines (the total gets lost).
  - *Rejected:* a dual axis.
- **Directing attention:**
  - Orange M4+ segments and grey segments below M4.
  - An orange-20% band spans 1.755–3.042, the M4+ minimum and maximum since 2009.
  - A label on 2025.
  - Slate-tint bands mark the two comparison periods.

```
 gempa per tahun                       2025: total tertinggi, tetapi M4+ --+
 20.000 |                                                                  v
        |                                                                  .
        |                                          .                       .
 10.000 |                         .  .  .   .   .  .  .  .                 .
        |          .  .  .  .  .  .  .  .   .   .  .  .  .  .              .
        |  [##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##] <- band 1.755-3.042
        +-------------------------------------------------------------------------
         2009                                                            2025
         # = M4+ (oranye)    . = di bawah M4 (abu-abu)
```

**Bridge (text only, after F2):**

- The bridge states the catalog's link to the announced numbers. For 2020–2024 the catalog's yearly totals differ from BMKG's year-end figures by less than 5%. For 2025, and for the 29.869 figure for 2024, BMKG has not published an event-level breakdown.
- It then paraphrases BMKG's counter-argument with sources:
  - The then-head said instrument numbers stayed around 170 sensors from 2009 to 2019 even though counts jumped in 2018–2019, and that counts fell in 2020 despite more than 300 seismographs.
  - BMKG also reported operating 533 seismographs after building 95 in 2023.
- It acknowledges that 2018–2019 contains real sequences (F5) and turns to what the catalog itself records.

---

### F3 — Conflict 3: the fingerprint of detection

- **Question:** How did the *distribution* of magnitudes change between the two periods?
- **Data:** catalog, magnitude (rounded to 0,1) × events per year, 2014–2017 vs 2022–2025.
- **Chart form and why:** two overlaid frequency polygons on a linear y-axis. Readers see the lines separate sharply below M4 and stay close above it.
  - *Rejected for the main text:* the log-scale Gutenberg–Richter plot. It is unfamiliar to journalists, so it goes to the notebook.
  - *Rejected:* side-by-side histograms and box plots.
- **Ranges:**
  - x from M1,0 to M6,0, with no pooled bin; y from 0 to 700.
  - Events above M6,0 and below M1,0 are not drawn, and the note gives their counts.
- **Directing attention:**
  - 2014–2017 is dashed `#6B7280`; 2022–2025 is solid `#1F2937` and thicker.
  - The background is grey 35% below M4,0 and orange 10% from M4,0.
  - An arrow runs between the peaks, M3,4 → M3,0.
- **Rival explanation addressed (note line):**
  - The magnitude type switches between years, so the note reports the same comparison within one type: MLv only, where the peak moves from M3,4 (2014–2017) to M2,7 (2025).
  - The shift therefore isn't produced by changing labels.

```
 gempa per tahun
 700 |
     |            .-.            <- 2022-2025 (solid), puncak M3,0
     |           /   \
 300 |          /  .-.\.          <- 2014-2017 (dashed), puncak M3,4
     |        _/ ./   \ \.
     |   ___.' ./      '-.'-.___________
     +-----+-----+-----+-----+-----+
     1,0   2,0   3,0   4,0   5,0   6,0      magnitudo
     [:::: abu-abu < M4 ::::][ oranye M4+ ]
```

---

### F4 — Conflict 4: more ears per quake

- **Question:** Is the network measuring each quake more densely than before?
- **Data:** catalog, year × median phase count, for M4,0–4,9 events only. Holding size fixed removes the "bigger quakes get more readings" confound.
- **Chart form and why:** a line with points plus an interquartile ribbon. The slope is the message, and the ribbon shows the change is not driven by outliers.
  - *Rejected:* columns of medians, and a scatter of all events.
- **Directing attention:**
  - An orange line with an orange-20% ribbon.
  - Slate-tint bands mark the same two comparison periods as F2 and F3, labeled with their medians (20 and 44), so the numbers match the brief.
- **Note line:** the within-type check (MLv only: 18 → 42) and the caveat that processing changes can also add readings.

```
 bacaan fase (median)
 50 |                                   :     o      :
    |                                   :  o / \  o  :
 40 |                                   : / \/   \/  :
 30 |                          o--o     :  med. 44   :
 20 |   :  o--o--o--o  :  o--o'         :            :
 10 |  o: med. 20      :
    +-----------------------------------------------
     2009 2014-2017              2022-2025
```

---

### F5 — Resolution 1: what a real surge looks like

- **Question:** When M4+ activity does jump, what causes it?
- **Data:** catalog, monthly M4+ counts, Nov 2008 – Jul 2026 (210 months drawn).
  - 10 partial months are scaled to full length.
  - Sep 2009 and Jul–Agu 2013 are gaps where the line breaks.
  - Aug 2026 has only 14 days of data, so the series ends at Jul 2026.
- **Chart form and why:** a monthly line. With 210 points, the shape (a flat baseline with brief spikes) is the message.
  - *Rejected:* a calendar heatmap and a separate map.
- **Labeling rule:**
  - Every month at or above 1,75× the median month gets a label (median 179 → threshold 313). That gives exactly six months, and the next highest month is 307.
  - Each label names the sequence behind at least half of that month's excess.
  - Names and dates only, because catalog magnitudes are preliminary.
  - Palu (Sep 2018, 305) falls below the threshold and is mentioned in the body text.
- **Directing attention:**
  - An orange line, with a dashed `#6B7280` median line.
  - Six labeled dots on the spikes.
  - y from 0 to 400.

```
 gempa M4+ per bulan
 400 |                      Lombok       L. Maluku
     |  Mentawai            Agu 2018     Nov 2019   L. Maluku     Mindanao
     |  Okt 2010            *  Halm. &    *         & Talaud      Filipina
 300 |    *                 /\ L.Maluku  /\         Jan 2023      Jun 2026
     |   /\                /  \  *      /  \           *             *
 179 |--/--\--   ---------/----\/\-----/----\---------/\------------/\--  median
     |~~    ~~ ~~ ~~~~~~~~         ~~~~      ~~~~~~~~~  ~~~~~~~~~~~~  ~
     +---------^--^--------------------------------------------------
      2009   (gap 2009, 2013)                                   Jul 2026
```

---

### F6 — Resolution 2: reading the 2026 number

- **Question:** Is 2026 so far unusual?
- **Data:** catalog, 17 yearly M4+ counts (2009–2025) plus the 2026 pace (1 Jan – 14 Agu, scaled to a full year).
- **Chart form and why:** a one-dimensional dot strip. The question is where one value sits in a distribution.
  - *Rejected:* a box plot (too abstract) and a bullet chart (it implies a target).
- **Directing attention:**
  - Orange-45% dots for past years, on a grey band spanning 1.755–3.042.
  - The minimum (2013) and maximum (2019) are labeled.
  - A solid orange diamond marks 2026.
  - A tick marks the median (2.159).
  - x from 1.600 to 3.200.

```
 2013: 1.755                  2026 (s.d. 14 Agu): ±2.430           2019: 3.042
    |                                |                                |
    o  o o o o   o  o o  o o  o   o  <>     o                         o
 [===================== Rentang 2009-2025 ===============================]
 +---------+---------+---------+---------+---------+---------+---------+---------+
 1.600     1.800     2.000     2.200     2.400     2.600     2.800     3.000     3.200
                    Median: 2.159 per tahun = 6 gempa M4+ setiap hari
```

**Checklist box after F6:** the four reader actions from the brief's §4 (worded in `figure-text.md`).

---

## 4. Discarded figure (in the story's appendix, with its reason)

**F-X:** a cumulative line of BMKG station codes inside the box, counted by each code's earliest effective date, 2008–2025. It runs from 369 codes in 2017 to 1.314 by 2025 (×3,6).

**Counting rule:**

- One row per code, using its earliest effective date.
- 35 codes dated 1 Jan 1970 or 1 Jan 1980 are placeholders and are left out.
- Parse the dates with an ISO-8601 parser: 50 rows carry fractional seconds, and a fixed-format parser silently drops them.
- About 60% of dates fall on 1 January, so the line steps by year.

**Visual system:** same as F1–F6, with the line in slate.

**Why it was cut:**

- The table mixes seismographs with other sensor types; many 2018–2020 entries sit at village offices and BPBD buildings.
- The dates are table-entry dates, not installation dates.
- The count conflicts with BMKG's own sensor figures (about 170, then 300+, then 533).

It would move the argument to "how many instruments", which this data cannot settle. F4 measures detection from the catalog itself instead.

**Also considered and not drawn:** a dot map of all 144.030 events. It is overplotted, shows *where* rather than *what changed*, and is the most common existing analysis of this dataset.

---

## 5. Data decisions and limitations (stated in the story)

| Decision or limitation | What we do about it |
|---|---|
| **BMKG release figures come from press reports**, and the wording of the M5 boundary varies ("di atas M5", "M≥5"). | We use figures reported consistently by named outlets (§6). Where outlets disagree (one reports 10.983 for 2023), we use the figure reported by two outlets (10.789). |
| **BMKG published two totals for 2024** (7.358 on 31 Des 2024; 29.869 on 17 Jan 2025) without explaining the difference. | F1 shows both. The 2024 M5+ count (186) comes from the 31 Des release. |
| **The public catalog vs the announced totals.** The catalog is within 5% of BMKG's year-end totals for 2020–2024 (2020: 8.283 vs 8.264; 2021: 10.460 vs 10.570; 2022: 10.390 vs 10.792; 2023: 11.277 vs 10.789; 2024: 7.498 vs 7.358). For 2025 it holds 18.592, 43% of the announced 43.439. | We state this. The main message's numbers come from BMKG's own releases; the catalog explains the pattern but does not reproduce the 2025 total. |
| The catalog is **not clipped to Indonesia**. | We use the coordinate box, which includes border areas (e.g. F5's Mindanao spike). |
| **143 days have no data.** | Gaps are scaled or broken as in §2. |
| **Magnitude types switch between years** (MLv vs unlabeled M). | Rounded magnitudes, M4 used as an approximate boundary, and the within-type checks in F3 and F4. |
| **Small-quake magnitudes cannot be checked against an independent scale.** Only larger quakes have moment-tensor magnitudes. | F3 and F4 are framed as *consistent with* better detection. |
| The catalog is **preliminary**. | No magnitudes in F5's labels. |
| **Counts are not impact.** | No claim about losses. |

---

## 6. Sources (for the story's sources section)

**Dataset**

1. Vigiliant, A. K. *Earthquakes in Indonesia* (catalog v2) [dataset]. Kaggle. https://doi.org/10.34740/kaggle/ds/1934565. Diunduh 28 Oktober 2026. `katalog_gempa_v2.tsv` SHA-256 `7c92b9e9…dd77a7`.
2. BMKG. RepoGempa event catalog. https://repogempa.bmkg.go.id/eventcatalog

**BMKG release figures (F1, bridge, lede)**

3. CNN Indonesia, 30 Des 2021. "Aktivitas Gempa di Indonesia Meningkat Sepanjang 2021." Totals, M5+ and felt counts for 2020 and 2021. https://www.cnnindonesia.com/teknologi/20211230134505-199-740553/aktivitas-gempa-di-indonesia-meningkat-sepanjang-2021
4. Antara News. "Ini jumlah rata-rata banyaknya gempa di Indonesia dalam setahun." Totals, M5+ and felt counts for 2022 and 2023. https://www.antaranews.com/berita/4191750/ini-jumlah-rata-rata-banyaknya-gempa-di-indonesia-dalam-setahun
5. Beritasatu. "BMKG Catat 10.789 Gempa Bumi di Indonesia Sepanjang 2023." 2023 total; 95 new seismographs; 533 in operation. https://www.beritasatu.com/nusantara/2791754/bmkg-catat-10789-gempa-bumi-di-indonesia-sepanjang-2023
6. IDX Channel, 31 Des 2024. "BMKG: 7.358 Gempa Bumi Guncang Indonesia Sepanjang 2024." 2024 year-end total, M5+ and felt counts. https://www.idxchannel.com/news/bmkg-7358-gempa-bumi-guncang-indonesia-sepanjang-2024
7. IDX Channel, 17 Jan 2025. "Indonesia Diguncang Hampir 30.000 Gempa Bumi Sepanjang 2024." The figure 29.869; the head of BMKG on instrument numbers (about 170 sensors, 2009–2019). https://www.idxchannel.com/news/indonesia-diguncang-hampir-30000-gempa-bumi-sepanjang-2024
8. Okezone, 17 Jan 2025. "BMKG: 29.869 Gempa Terjadi di Tahun 2024, 20 di Antaranya Merusak." The figure 29.869; 300+ seismographs from 2020. https://news.okezone.com/read/2025/01/17/337/3105363/bmkg-29-869-gempa-terjadi-di-tahun-2024-20-di-antaranya-merusak
9. CNBC Indonesia, 21 Jan 2025. "Gempa Makin Sering-Megathrust Ancam RI, Kepala BMKG Beri Warning Keras." https://www.cnbcindonesia.com/news/20250121140939-4-604849/gempa-makin-sering-megathrust-ancam-ri-kepala-bmkg-beri-warning-keras
10. kumparan, 2 Jan 2026. "BMKG Catat 43.439 Gempa Terjadi di Indonesia Sepanjang 2025." 2025 total, M5+ and felt counts. https://kumparan.com/kumparannews/bmkg-catat-43-439-gempa-terjadi-di-indonesia-sepanjang-2025-26YLtQKF0D1

**Method background**

11. Diantari, H. C. (2017). *Kuantifikasi Kelengkapan Magnitudo pada Katalog Modern BMKG (2008–2016) dalam Pemantauan Gempabumi Indonesia.* Skripsi, FMIPA Universitas Gadjah Mada. https://etd.repository.ugm.ac.id/penelitian/detail/114101

**Reproducibility:** one notebook takes these steps:

1. Shallow-clone `github.com/kekavigi/repo-gempa`. It needs no Kaggle login.
2. Run the author's parser with `selectolax<1.0`.
3. Verify the SHA-256 against `MANIFEST.md`.
4. Apply §2 and produce every catalog number and figure.

The release figures for F1 are typed into the notebook as a small table, with the source number from §6 for each value.
