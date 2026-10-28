# Compliance check against the guide

Checked 2026-10-28 against `docs/Panduan_Midterm_Project-V2.pdf` (§3 Tahap 3, §5, §6) and the CLAUDE.md submission list. Facts only; nothing below was written into the story.

## Data story (submission item 2)

| requirement | status | evidence |
|---|---|---|
| Main message printed at the very top, as one sentence | **OK** | page header; one sentence (build check) |
| At most 7 figures | **OK** | 6 story figures + 1 discarded in the appendix |
| Each figure has a finding title | **OK** | titles inside each PNG, verbatim from `docs/figure-text.md` |
| Each figure has attention markers | **OK** | bands, direct labels, arrows and markers as specified in storyboard §3 |
| Data source cited in full, with download date | **OK** | sources section ("Diunduh 28 Oktober 2026", SHA-256); a source line under every figure |
| Data limitations stated | **OK, see note** | limitations section = storyboard §5 table, verbatim (in English) |
| One discarded figure, with its reason | **OK** | appendix: heading, F-X and reason, verbatim |
| Link publicly accessible | **NOT YET** | page builds locally; needs a public GitHub repo + Pages (see README) |

## Notebook / repository (submission item 3)

| requirement | status | evidence |
|---|---|---|
| Produces every number and figure in the story | **OK** | `notebooks/main.ipynb`; `reports/number_check.md` (94 match, 7 close, 2 differ in internal Q&A notes only, 2 context rows) |
| Re-runnable, with data or download script | **OK** | one command `.venv/bin/python -m src.run`; raw TSV committed; `src/download.py` rebuilds and verifies it; a clean-room rebuild from committed inputs reproduced all 12 outputs byte for byte |
| Link publicly accessible | **NOT YET** | repository is local only (no commits yet; git user name/email not set) |

## Message Brief & Storyboard (submission item 1)

| requirement | status | evidence |
|---|---|---|
| One PDF on the course template | **NOT IN REPO** | `docs/brief.md` and `docs/storyboard.md` are Markdown; the template PDF is the group's to produce |
| Brief is one page | **CHECK** | depends on the template layout |
| NIMs | **MISSING** | `docs/brief.md` line 3: "NIM ________" for both members |
| Link publicly accessible | **NOT YET** | |

## AI declaration (§6)

- Required on the submission form: tools used, for which parts, and to what extent. `AI_USAGE.md` logs every session in this repository.
- `docs/qa-notes.md` states the brief and storyboard "were drafted with Claude". §6 also forbids handing message, audience and design decisions to AI and copying AI-written narrative; the declaration should describe the actual extent.

## Observations (not failures of a stated requirement)

- **Body text:** the page carries the lede, the bridge (after Gambar 2) and the checklist box. Storyboard §1 has key sentences for Setup, Conflict 1–4 and Resolution 1–2, but no paragraphs for them exist yet; storyboard F5 says Palu (Sep 2018) "is mentioned in the body text", which is not on the page. Invisible comments in `story/content.md` mark each spot.
- **Language:** the story is in Bahasa Indonesia; the limitations table (storyboard §5) and the group labels/annotations in the sources list (storyboard §6) are in English.
- **Section headings:** the sources and limitations sections have no heading text.
- **Numbers in the text:** the checklist says "sekitar 2.150" M4+ a year; Gambar 6's label says the median is 2.159.
- **Figure numbers:** "Gambar 1–6" labels are added by the page layout because the bridge and the F-X reason refer to "Gambar 5" and "Gambar 4".
- **"explain easier" mode:** implemented from the group's `docs/easy-version.md`: when the toggle is on, each of the six charts is swapped for one block with one plain sentence (verbatim), and the plain card appears under the main message; default is off. All its numbers are verified in `reports/number_check.md`. The storyboard still says "Why static"; the change belongs in `docs/decision_log.md`.
- **Phones:** figures are PNGs 7 in wide; on a 375 px screen their smallest text is hard to read in the column. Tapping a figure opens it at 1100 px wide to pan and read.
