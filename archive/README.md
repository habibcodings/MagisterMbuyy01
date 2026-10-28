# Archive: earlier static version (superseded)

This folder holds the first, static version of the story, built before the group's build package (28 Oct 2026) replaced it. It is kept for the record and is not maintained. The current deliverables are `site/`, `notebooks/analisis.ipynb`, `exports/` and `docs/02_brief.md` / `docs/03_storyboard.md` at the repository root.

| Path | Contents |
|---|---|
| `docs/` | earlier brief, storyboard, verbatim figure text, easy-version spec, internal QA notes |
| `src/` | earlier pipeline: download, cleaning, profiling, number check, matplotlib figures, story builder |
| `notebooks/main.ipynb` | earlier end-to-end notebook |
| `figures/` | earlier static figures F1–F6 and the discarded F-X |
| `story/` | earlier story source and template |
| `reports/` | source survey, profiling, number check, compliance check |
| `data/raw/` | verified catalog TSVs (SHA-256 in `data/raw/MANIFEST.md`) and the archive's day table |
| `data/processed/` | events in the analysis box and valid days |

The code here uses paths relative to the old layout (for example `data/raw/` at the repository root), so it does not run from this folder as is.
