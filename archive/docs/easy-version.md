# Easy version ("explain easier") — brief and block specs

## What it is

Each of the six figures has a plain-language alternative. When the reader turns on the toggle, the chart is **swapped** for one simple block and one plain sentence.

## Who it is for

It is for the same audience, reporters, on the days they cannot or will not read a chart. The sentence is written so it can be quoted in an article as it stands.

## What it is not

- It is not a second story: the claims and numbers are the same as in the charts.
- It is not extra figures: a block replaces its chart and is never shown beside it.

## Rules

1. **Swap, never add.** When the toggle is on, each chart is replaced by its block. When it is off, only the chart shows. The default is **off**, so the charts are what the reader sees first.
2. **Same numbers as the charts.** Every number below already appears in a figure or in the brief. No new numbers.
3. **One idea per block.** A block shows a single number, one pair, or one share.
   - **number:** one value that stands on its own.
   - **compare:** two values of the same thing, drawn on one scale.
   - **dots:** a share, out of 100.
4. **Tone follows the color system.**

   | Tone | Meaning | Color |
   |---|---|---|
   | strong | stronger quakes (M5+ in BMKG's releases, M4+ in the catalog) | `#C2410C` |
   | small | quakes below the threshold | `#B8BEC6` (labels in `#6B7280`) |
   | neutral | anything that isn't a quake-size count (totals, readings) | `#475569` |

5. **The main message never changes.** The official sentence stays first in both modes. Easy mode adds one plain card directly below it.
6. **Sentences:** one sentence, at most about 25 words, with no technical terms except "M4"/"M5", which are explained once in the plain card.

## Plain card (easy mode only, directly below the main message)

> BMKG kini mencatat jauh lebih banyak gempa, tetapi gempa yang kuat tidak ikut bertambah; yang bertambah adalah gempa kecil yang kini lebih mudah terekam. (M4 dan M5 adalah ukuran kekuatan gempa; makin besar angkanya, makin kuat gempanya.)

## Block specs

```
Gambar 1 — block: compare
  numbers: 2020 = 244 ; 2025 = 153
  sentence: BMKG mengumumkan lima kali lebih banyak gempa pada 2025 dibanding 2020, tetapi gempa M5 ke atas justru berkurang dari 244 menjadi 153.
  tone: strong

Gambar 2 — block: dots
  numbers: 3 dari 100
  sentence: Dari setiap 100 gempa tambahan di katalog BMKG, hanya 3 yang berkekuatan M4 ke atas; 97 sisanya gempa kecil.
  tone: strong

Gambar 3 — block: compare
  numbers: 2014–2017 = 212 ; 2022–2025 = 618
  sentence: Gempa kecil sekitar M3 kini tercatat hampir tiga kali lebih banyak setiap tahun, sementara gempa sekitar M4,5 hampir tidak berubah.
  tone: small

Gambar 4 — block: compare
  numbers: 2014–2017 = 20 ; 2022–2025 = 44
  sentence: Gempa yang ukurannya sama kini terekam oleh dua kali lebih banyak bacaan alat, tanda jaringan pemantau yang makin peka.
  tone: neutral

Gambar 5 — block: compare
  numbers: Bulan biasa = 179 ; Nov 2019 (Laut Maluku) = 397
  sentence: Lonjakan sungguhan terjadi singkat dan punya nama tempat, seperti Laut Maluku pada November 2019, ketika gempa M4 ke atas lebih dari dua kali bulan biasa.
  tone: strong

Gambar 6 — block: number
  numbers: 6
  sentence: Rata-rata ada sekitar 6 gempa M4 ke atas setiap hari di Indonesia; angka ini sudah tinggi, dan 2026 sejauh ini masih di kisaran yang sama.
  tone: strong
```

## Notes for the implementer

- **Labels.** If the compare block only supports fixed "Sebelum / Sesudah" labels, Gambar 1, 3 and 4 still read correctly. Gambar 5 needs the custom labels above, because a typical month is not a "before".
- **Dot colors.** In the dots block, the 97 non-highlighted dots should use the *small* grey (`#B8BEC6`) rather than a neutral mauve, so the dots keep the same meaning as the charts.
- **Old numbers in the template.** The template's example compare shows 1.820 → 1.995. Those are first-version numbers. The current catalog M4+ values are 1.944 → 2.145 per year. Don't reuse the example.

## Where each number comes from

| Gambar | Value | Source |
|---|---|---|
| 1 | 244 → 153 (and ×5) | BMKG releases (storyboard §6, refs 3 and 10) |
| 2 | 96,8% of the rise is below M4, rounded to 97 of 100 | Catalog, 2014–2017 vs 2022–2025 |
| 3 | 212 → 618 quakes per year at M3,0; 171 → 192 at M4,5 | Catalog, F3 |
| 4 | median 20 → 44 phase readings | Catalog, F4 |
| 5 | median month 179; Nov 2019 = 397 | Catalog, F5 |
| 6 | median 2.159 per year ÷ 365 ≈ 6 per day; 2026 pace ±2.430 inside 1.755–3.042 | Catalog, F6 |
