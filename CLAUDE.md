# Midterm VDL — Data Story: Earthquakes in Indonesia

> Adapted 2026-10-28 by Claude from the group's original CLAUDE.md. "Your role", Phase 2, Phase 3 and "Logs to maintain" are the group's text unchanged. Context, Phase 0, Phase 1 and file names were rewritten for this dataset — **the group should review them.**

> **2026-10-28, later:** the group supplied a build package (`vdl-midterm-package.zip`, AI-assisted per its own README: brief, storyboard, page copy, design and data specs, reference pipeline). It supersedes the file names below: the story is `site/` (interactive, no build step), the notebook is `notebooks/analisis.ipynb`, static figures are in `exports/`, the brief and storyboard are `docs/02_brief.md` and `docs/03_storyboard.md`, and reference numbers are in `data/expected_numbers.json`. The package's precedence rules apply. Numbers come from `expected_numbers.json`, words from its `05_page_copy.md`, behaviour from `04_design_interaction_spec.md`, and story choices from `03_storyboard.md`. At the group's request, the older pipeline and its documents were moved to `archive/` (see `archive/README.md`); the "Repo structure" below describes that earlier layout. A Streamlit version of the same story (`streamlit_app/`, text in `teks.py` kept identical to `site/`) was added on request.

## Context
- Course: Visualisasi Data Lanjut (CAK7AGB4), Magister Informatika, Telkom University. Midterm data story, 30% of final grade.
- Task guide: `docs/Panduan_Midterm_Project-V2.pdf`. It is the authority. If this file conflicts with it, the guide wins. Read it at the start of any session where you haven't seen it yet.
- Dataset: "Earthquakes in Indonesia" (A. K. Vigiliant), Kaggle, DOI 10.34740/kaggle/ds/1934565 — a compilation of BMKG's RepoGempa preliminary catalog. File used: `katalog_gempa_v2.tsv` (37 columns). Not clipped to Indonesia. The author's GitHub repo `kekavigi/repo-gempa` holds the raw archive (`bmkg_html.sqlite`), the parser (`extract_tsv.py`) and a generated `MANIFEST.md` with row counts and SHA-256.
- Registered source URL: `https://www.kaggle.com/datasets/kekavigi/earthquakes-in-indonesia`
- Registration date: 28-10-2026 01:07 (as shown on the mid-terdaftar page)
- Group: Yasmina Arethaya Hanjani (NIM `<FILL IN>`), Cut Nabilah Nuur Azizah (NIM `<FILL IN>`)
- Brief and storyboard: `docs/brief.md`, `docs/storyboard.md`, plus `docs/figure-text.md` (verbatim figure text) and `docs/qa-notes.md` (internal). The group declared all four **final on 2026-10-28** — the Phase 1 gate is passed.

## Your role — read before doing anything
This is graded coursework. Section 6 of the guide limits how AI may be used, we must declare all AI use on the submission form, and we must defend every decision orally in week 8. Stay inside these limits even if we ask otherwise in the moment; if we do, remind us briefly and offer the allowed alternative.

You MAY:
- Write and debug code: download scripts, cleaning, schema harmonization, profiling, the reproducible pipeline, figure code, page build/hosting.
- Implement figures exactly to the spec in our storyboard.
- Explain concepts in general terms (chart types and when they fit, perceptual principles, annotation techniques, time-series pitfalls).
- Critique text and designs we wrote: point out problems, ask questions, check them against the guide and rubric.
- Check compliance with the guide's requirements and report what is missing.

You MUST NOT:
- Propose or choose our target audience.
- Propose our main message, supporting claims, or the decision the story should influence.
- Choose chart types, figure order, highlights, or attention cues for the story.
- Write narrative text: the brief, storyboard justifications, finding-style figure titles, captions, story paragraphs, limitations prose, or presentation content. Insert our text verbatim where needed.
- Rank findings by "story potential" or suggest headlines. When profiling, report descriptive facts neutrally.

## Workflow (order is graded — do not skip ahead)

### Phase 0 — Setup and acquisition
- Create the repo structure below.
- Before writing the downloader, report the source facts to us (done 2026-10-28: `reports/source_survey.md`) and wait for our confirmation of which file version to use.
- `src/download.py`: follow the storyboard's reproducibility plan — fetch `bmkg_html.sqlite` and `extract_tsv.py` from `kekavigi/repo-gempa` **pinned to a commit**, run the parser (needs `selectolax<1.0`), and verify the TSV's SHA-256 against the author's `MANIFEST.md`. Read the parser before running it; run it isolated. Never use a pre-cleaned copy or another re-upload.
- Commit the verified TSV (~30 MB) so the pipeline also runs without the rebuild step.
- Record each file in `data/raw/MANIFEST.md`: source URL, commit, filename, download date, SHA-256.

### Phase 1 — Harmonize and profile
Inspect the file before assuming a schema. Check, do not assume:
- column types; `datetime` format and time zone; parse failures
- duplicate `eventID`s and duplicate events
- events outside the analysis box (lat −11…6, lon 94…142); count per year
- `broken` days from the source archive (collection gaps) → valid days per year; partial years (2008, 2026)
- missing `magnitude`; `mag_type` mix per year
- `depth`, `phasecount`, `azimuth_gap`: missing, zero, negative or extreme values
- completeness magnitude per year (maximum-curvature estimate), as a descriptive check

Outputs:
- `data/processed/gempa_box.csv`: one row per event inside the box — eventID, datetime_utc, date, year, month, latitude, longitude, depth, magnitude, mag_type, phasecount, azimuth_gap, location, agency, source_file.
- `data/processed/valid_days.csv`: one row per calendar day — date, status (`ok`/`broken`).
- `reports/profiling.md`: events per year (all / in box), valid days per year, events per valid day, magnitude-type mix, missing values, distributions, completeness estimates, and a log of every schema issue found.
- **Number check:** recompute every number cited in `docs/brief.md` and `docs/storyboard.md` and report match / mismatch factually.
- Reconciliation: BMKG's announced yearly totals vs. the public catalog — report differences factually; do not decide which figure is right.
- Quick-look plots are allowed only in `exploration/`, clearly marked as not for the story.
- Append every data issue found to `docs/limitations_log.md` as factual notes.

**GATE: stop after Phase 1.** We write the Message Brief and Storyboard ourselves. Do not create any story figure until `docs/brief.md` and `docs/storyboard.md` exist and we say they are final. If asked earlier, remind us of this gate.

### Phase 2 — Figure implementation
- Implement exactly the figures in `docs/storyboard.md`: chart type, encodings, highlight, annotations, and title text as we specified.
- If a spec is ambiguous or missing (e.g., colors, which routes to highlight), ask. Do not fill design gaps yourself.
- Technical hygiene is fine without asking: legible font sizes, no clipped labels, consistent export size/DPI, readable on mobile, thousands separators on axes.
- Maximum 7 story figures in `figures/`. Keep the one discarded figure in `figures/discarded/` with our stated reason in `figures/discarded/REASON.md`.
- Each figure comes from one function in `src/figures.py`, called from the notebook. Deterministic output.

### Phase 3 — Assembly and reproducibility
- `notebooks/main.ipynb` runs end-to-end, from download to every number and figure in the story. One command reproduces everything (document it in README).
- Pin dependencies in `requirements.txt`. Relative paths only.
- Story page in `story/`: you handle layout, build, and hosting (e.g., GitHub Pages). All visible text is ours.
- Before submission, run a compliance check against the guide and list anything missing. Do not write the missing content:
  - main message as one sentence at the very top
  - ≤ 7 figures, each with a finding title and attention markers
  - full source citation with download date
  - limitations section
  - discarded figure with reason
  - all three links publicly accessible

## Logs to maintain
- `AI_USAGE.md`: at the end of each session, append date, what we asked, what you did, files touched. Factual, no spin. We need this for the mandatory AI declaration.
- `docs/decision_log.md`: when we change a design or data decision, remind us to record what changed and why. We write the entry. (The presentation asks for one thing that changed during the work.)

## Repo structure
```
CLAUDE.md
README.md
AI_USAGE.md
requirements.txt
docs/
  Panduan_Midterm_Project-V2.pdf
  brief.md              # written by us
  storyboard.md         # written by us
  limitations_log.md
  decision_log.md
data/raw/               # + MANIFEST.md (verified TSV committed)
data/processed/         # gempa_box.csv, valid_days.csv
src/download.py
src/clean.py
src/figures.py
notebooks/main.ipynb
exploration/            # not for the story
reports/profiling.md
figures/
figures/discarded/
story/
```

## Tech conventions
- Python 3.12, pandas 2.2.3 (pinned for the byte-identical rebuild). Plotting library: matplotlib (proposed by Claude 2026-10-28; the group did not object). Font: bundled DejaVu Sans for deterministic output.
- Code comments in English. Talk to us in the language we write in.
- Commit raw data if small enough for GitHub; otherwise rely on `src/download.py`.
