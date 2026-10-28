# Data limitations log

Factual notes on data issues found during acquisition and profiling (appended by the pipeline work). Raw material for the group's own limitations section; not story text.

- 2026-10-28 (Phase 0): the registered Kaggle page is at version 31 (updated 2026-07-17); the author's GitHub MANIFEST (generated 2026-08-16) describes a newer build covering events to 2026-08-14. The two are not the same file.
- 2026-10-28 (Phase 0): the catalog is BMKG's *preliminary* catalog; the Kaggle description says recent events may not yet be accurate because preliminary solutions are revised.
- 2026-10-28 (Phase 0): the author states field meanings, units and methods are BMKG's to define and are not documented in the repository.
- 2026-10-28 (Phase 0): 143 days in the source archive are marked `broken` (collection gaps, not zero seismicity), concentrated in 2008–2009, 2013 and Nov–Dec 2018.
- 2026-10-28 (Phase 0): the catalog's bytes depend on the pandas version used by the parser (pandas 3 writes whole-second timestamps as ".000000"); pandas 2.2.3 reproduces the author's SHA-256, so it is pinned.
- 2026-10-28 (Phase 1): `datetime` mixes formats: 4 timestamps have no fractional seconds. Years are assigned by UTC date.
- 2026-10-28 (Phase 1): `mag_type` mix changes sharply between years inside the box, e.g. unlabeled `M` is 92.7–95.0% in 2020–2022, `MLv` 93.9% in 2025 vs 28.7% in 2024 (see `reports/profiling.md` §4).
- 2026-10-28 (Phase 1): 923 events in the box have no magnitude, concentrated in 2017 (190), 2018 (154), 2025 (235) and 2026 (133).
- 2026-10-28 (Phase 1): 59 events in the box have `depth` > 700, most at exactly 750; one event outside the box has `depth` 90,000. Units are not documented upstream.
- 2026-10-28 (Phase 1): the max-curvature completeness bin in the box ranges from 2.7 (2025) to 3.7 (2015) for 2010–2025; 2008 and 2009 are 4.8 and 4.3 (partial or gap-heavy years).
- 2026-10-28 (Phase 1): of 298 M4+ events in Jan 2023, 119 carry Northern Molucca Sea / Talaud labels and 51 carry Banda Sea / Tanimbar labels.
- 2026-10-28 (Phase 1): 1,357 station-table rows fall inside the box; 50 have no effective date.
- 2026-10-28 (Phase 1): BMKG's announced 2024 total as cited in the brief (29,869) vs. this catalog: 9,097 events dated 2024 anywhere, 7,498 inside the box.
