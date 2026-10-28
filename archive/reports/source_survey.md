# Source survey (Phase 0, before writing the downloader)

Surveyed 2026-10-28 from public metadata only (Kaggle API and Croissant file list, GitHub API, the author's README and MANIFEST). Nothing downloaded yet. Descriptive facts only.

## Registered source: Kaggle

| item | value |
|---|---|
| page | https://www.kaggle.com/datasets/kekavigi/earthquakes-in-indonesia |
| DOI | 10.34740/kaggle/ds/1934565 |
| author | Agapitus Keyka Vigiliant (`kekavigi`) |
| current version | 31, last updated 2026-07-17 |
| license | Database: Open Database (ODbL); Contents: © Original Authors |
| archive | `archive.zip`, 111.4 MB (422 MB unzipped) |
| files | `katalog_gempa_v2.tsv` (37 columns), `katalog_sensor.tsv` (6 columns), `katalog_gempa.csv` (legacy v1, 13 columns) |
| stated origin | BMKG RepoGempa preliminary catalog (`repogempa.bmkg.go.id/eventcatalog`); "the most recent events may not yet be accurate, as preliminary solutions are revised over time" |
| stated coverage | 1 Nov 2008 to the last update; "no longer clipped to Indonesia" |
| other copy | the description points to a daily-updated version at gempa.kekavigi.xyz; "the copy here is refreshed less often" |

`katalog_gempa_v2.tsv` columns: eventID, datetime, latitude, longitude, magnitude, mag_type, depth, phasecount, azimuth_gap, location, agency, then 26 focal-mechanism columns (datetimeFM … misfit).

## Author's GitHub repository

| item | value |
|---|---|
| repo | https://github.com/kekavigi/repo-gempa (public, MIT code license, separate `LICENSE-DATA`) |
| latest commit | `539ed6e461` 2026-08-16 ("Perbarui schema database") |
| contents | `katalog_gempa_v2/bmkg_html.sqlite` (21.4 MB raw archive), `katalog_gempa_v2/extract_tsv.py` (parser, 8.5 kB), `MANIFEST.md` (generated), `docs/SCHEMA.md`, `docs/METHOD.md` |
| TSV in repo | no; the README says the TSVs are derived; get them from Kaggle or rebuild with `extract_tsv.py` |
| citation advice (README) | cite the Kaggle dataset (DOI) and state the version used; the version DOI or the SHA-256 of the file pins it |
| field meanings | "BMKG's to define, not this repository's"; the repository documents structure, coverage and provenance only |

Figures from the author's `MANIFEST.md` (generated 2026-08-16T12:53Z):

| item | value |
|---|---|
| `katalog_gempa_v2.tsv` | 30 MB, 177,353 rows, SHA-256 `7c92b9e9fba06a04b436c39956ba8ee7e7615fdbda9370d7a768e0f893dd77a7` |
| coverage | first event 2008-11-01, last event 2026-08-14 |
| events outside lat −11…6, lon 94…142 | 33,323 (so 144,030 inside) |
| missing `magnitude` / `mag_type` | 1,430 of 177,353 |
| archive days | 6,496 (6,353 `ok`, 143 `broken`); broken days are collection gaps, not zero seismicity |

## How this relates to the brief and storyboard

- The SHA-256 prefix/suffix in the storyboard's draft citation (`7c92b9e9…dd77a7`), the 14 Aug 2026 end date, the 144,030 events in the box and the 143 broken days all match the author's GitHub MANIFEST build, not Kaggle version 31 (updated 2026-07-17).
- The storyboard's reproducibility plan (rebuild from the GitHub archive with the author's parser, verify the SHA-256) is the route the author's README describes for checking a copy.
