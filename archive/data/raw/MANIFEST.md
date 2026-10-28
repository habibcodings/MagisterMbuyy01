# Raw data manifest

Written by `src/download.py`. Upstream files are fetched from the author's repository at a pinned commit; the catalog is rebuilt with the author's parser and checked against the author's MANIFEST.md.

- Repository: https://github.com/kekavigi/repo-gempa at commit `539ed6e461c409da1475781fd57bbc6deaef66ef`
- Dataset citation: Vigiliant, A. K. *Earthquakes in Indonesia*, Kaggle, DOI 10.34740/kaggle/ds/1934565
- Fetched / rebuilt (UTC): 2026-10-28 02:31

| file | role | source | SHA-256 |
|---|---|---|---|
| `upstream/bmkg_html.sqlite` | upstream input (not committed) | `https://raw.githubusercontent.com/kekavigi/repo-gempa/539ed6e461c409da1475781fd57bbc6deaef66ef/katalog_gempa_v2/bmkg_html.sqlite` | `13c5333d0d4bf15648c4c0d114771e06e595958e910a0718b500bffe93689cf2` |
| `upstream/extract_tsv.py` | upstream input (not committed) | `https://raw.githubusercontent.com/kekavigi/repo-gempa/539ed6e461c409da1475781fd57bbc6deaef66ef/katalog_gempa_v2/extract_tsv.py` | `a87c11a3badf35f9e0e41bd894b410786b456c1be8c5d5661a08423caa18e469` |
| `upstream/MANIFEST.md` | upstream input (not committed) | `https://raw.githubusercontent.com/kekavigi/repo-gempa/539ed6e461c409da1475781fd57bbc6deaef66ef/MANIFEST.md` | `2cd51c9757773a13e65c29b28e0f3f3e11662d1dcbe926cd42f7d0960299dee8` |
| `katalog_gempa_v2.tsv` | rebuilt by `extract_tsv.py`, matches author's MANIFEST | parser output | `7c92b9e9fba06a04b436c39956ba8ee7e7615fdbda9370d7a768e0f893dd77a7` |
| `katalog_sensor.tsv` | rebuilt by `extract_tsv.py`, matches author's MANIFEST | parser output | `5a4e57671c6b0ac718108987ad191c59a2870adf24f3ef101774bc145f66e466` |
| `archive_days.csv` | `days` table of the archive (date, status, event_count) | exported from `bmkg_html.sqlite` | `e3dd529714cfe120bb70cc4eb4f9cab65848d34d30aab27ca7dcf280a83236c6` |
