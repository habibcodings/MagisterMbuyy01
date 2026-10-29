# Bukan Bumi yang Makin Gaduh, Telinga Kita yang Makin Tajam

Cerita data interaktif dan notebook yang dapat dijalankan ulang · Interactive data story and reproducible notebook
Visualisasi Data Lanjut (CAK7AGB4), Magister Informatika, Telkom University
Yasmina Arethaya Hanjani & Cut Nabilah Nuur Azizah

**Repositori / Repository:** https://github.com/habibcodings/MagisterMbuyy01 · **Halaman cerita / Story page:** https://habibcodings.github.io/MagisterMbuyy01/ (aktif setelah GitHub Pages dinyalakan / live once GitHub Pages is enabled)

**Data:** Vigiliant, A. K. *Earthquakes in Indonesia* (katalog v2), Kaggle, doi:10.34740/kaggle/ds/1934565, dari BMKG RepoGempa; dibangun ulang dari `github.com/kekavigi/repo-gempa` pada commit `539ed6e` · rebuilt from the author's repository at commit `539ed6e`. Angka rilis BMKG / BMKG release figures: `data/release_figures_bmkg.csv` (sumber S3–S11 di / sources S3–S11 in `docs/03_storyboard.md` §7).

---

## Bahasa Indonesia

### Isi repositori

| Jalur | Isi |
|---|---|
| `docs/02_brief.md`, `docs/03_storyboard.md` | Message Brief dan Storyboard |
| `notebooks/analisis.ipynb` | Seluruh pipeline: ambil data, hitung, tulis data gambar, ekspor gambar statis, tabel verifikasi |
| `data/release_figures_bmkg.csv` | Angka rilis tahunan BMKG untuk Gambar 1 (jangan diubah) |
| `data/expected_numbers.json` | Angka rujukan; notebook membandingkan hasilnya dengan berkas ini |
| `data/figure_data/*.json` | Data gambar rujukan; `site/data/*.json` harus sama nilainya |
| `data/computed_numbers.json` | Angka hasil notebook (ditulis ulang setiap kali dijalankan) |
| `exports/` | SVG + PNG keadaan akhir setiap gambar (G1–G6, GX), dari notebook |
| `site/` | Halaman cerita (HTML/CSS/JS statis, tanpa langkah build) |
| `streamlit_app/` | Versi Streamlit dari cerita yang sama (teks dan angka sama dengan `site/`) |

### Menjalankan ulang notebook

Butuh Python 3.12 dan koneksi internet (untuk mengambil repositori data satu kali).

```bash
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/jupyter nbconvert --to notebook --execute --inplace notebooks/analisis.ipynb
```

Notebook mengambil `kekavigi/repo-gempa` tepat pada commit `539ed6e` ke `work/` (hanya commit itu, ±25 MB), menjalankan pengurai penulis (`extract_tsv.py`) untuk membangun ulang kedua TSV, dan memeriksa SHA-256-nya. `pandas==2.2.3` sengaja dikunci karena versi ini menghasilkan TSV yang identik byte demi byte. Notebook lalu menulis `site/data/*.json`, `data/computed_numbers.json`, dan `exports/`, dan diakhiri dengan tabel verifikasi (✓/✗) terhadap `data/expected_numbers.json`: bilangan bulat harus sama persis, desimal ±0,05. Jika ada ✗, sel terakhir berhenti dengan error. Jangan ubah angka agar cocok; laporkan selisihnya.

Hasil terakhir: 178 ✓ · 0 ✗; ketujuh `site/data/*.json` identik byte demi byte dengan `data/figure_data/`; menjalankan ulang menghasilkan berkas yang sama byte demi byte.

### Melihat halaman di komputer sendiri

```bash
python3 -m http.server 8000 --directory site
```

Lalu buka `http://localhost:8000`. Halaman membaca `data/*.json` lewat `fetch`, jadi harus dibuka lewat server, tidak langsung dari berkas.

### Menerbitkan dengan GitHub Pages

1. Isi `git config user.name` dan `git config user.email` (sekali per komputer).
2. Buat repositori **publik** di github.com, lalu commit dan push folder ini ke cabang `main`.
3. Settings → Pages → Build and deployment → Source: **GitHub Actions**. Workflow `.github/workflows/pages.yml` menerbitkan isi `site/` setiap kali ada push ke `main`. Alamatnya `https://<user>.github.io/<repo>/`.
4. Isi pernyataan penggunaan AI di footer `site/index.html` (cari `data-todo`). Tautan repositori sudah terisi.

### Versi Streamlit

Cerita yang sama dalam bentuk aplikasi Streamlit: teks diambil dari `streamlit_app/teks.py` (sama persis dengan `site/`), angka dari `site/data/*.json`. Tebak dulu, versi mudah per bagian dan untuk semua, mode "Hanya MLv", kartu lonjakan, dan Cek judulmu menjadi kontrol Streamlit. Bedanya dengan halaman web: tidak ada animasi gulir (gambar langsung dalam keadaan akhir, mirip versi cetak), tidak ada tooltip saat kursor di atas grafik, label lonjakan di Gambar 5 dipendekkan (nama lengkap ada di kartu lonjakan), dan tombol "Versi mudah untuk semua" tidak punya keadaan campuran.

Menjalankan di komputer sendiri (dari folder repositori):

```bash
.venv/bin/pip install -r streamlit_app/requirements.txt
.venv/bin/streamlit run streamlit_app/app.py
```

Menerbitkan di Streamlit Community Cloud (gratis, butuh repositori GitHub publik yang sama):

1. Push repositori ini ke GitHub (lihat langkah GitHub Pages di atas).
2. Buka [share.streamlit.io](https://share.streamlit.io), masuk dengan akun GitHub, pilih **Create app**.
3. Pilih repositori, cabang `main`, dan *Main file path* `streamlit_app/app.py`. Di *Advanced settings* pilih Python 3.12. Klik **Deploy**.
4. Alamatnya `https://<nama-pilihan>.streamlit.app`; subdomain bisa diubah di pengaturan aplikasi. Aplikasi gratis tertidur jika lama tidak dibuka dan bangun lagi saat diklik.
5. Isi `AI_STATEMENT` di bagian atas `streamlit_app/app.py` (sekarang masih tampil sebagai tempat kosong). `REPO_URL` sudah terisi.

---

## English

### What is here

| Path | Contents |
|---|---|
| `docs/02_brief.md`, `docs/03_storyboard.md` | Message brief and storyboard |
| `notebooks/analisis.ipynb` | The full pipeline: get data, compute, write figure data, static exports, verification table |
| `data/release_figures_bmkg.csv` | BMKG annual release figures for Figure 1 (do not edit) |
| `data/expected_numbers.json` | Reference numbers; the notebook checks its results against this file |
| `data/figure_data/*.json` | Reference figure data; `site/data/*.json` must match it in value |
| `data/computed_numbers.json` | Numbers computed by the notebook (rewritten on every run) |
| `exports/` | SVG + PNG of every figure's final state (G1–G6, GX), from the notebook |
| `site/` | The story page (static HTML/CSS/JS, no build step) |
| `streamlit_app/` | Streamlit version of the same story (same text and numbers as `site/`) |

### Rerun the notebook

Needs Python 3.12 and internet access (to fetch the data repository once).

```bash
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/jupyter nbconvert --to notebook --execute --inplace notebooks/analisis.ipynb
```

The notebook fetches `kekavigi/repo-gempa` at commit `539ed6e` into `work/` (that commit only, about 25 MB). It runs the author's parser (`extract_tsv.py`) to rebuild both TSVs and checks their SHA-256. `pandas==2.2.3` is pinned because it reproduces the TSV byte for byte. The notebook then writes `site/data/*.json`, `data/computed_numbers.json` and `exports/`. It ends with a verification table (✓/✗) against `data/expected_numbers.json`: integers must match exactly, floats within ±0.05. Any ✗ makes the last cell fail. Report a mismatch; don't patch numbers to make it pass.

Last run: 178 ✓ · 0 ✗; all seven `site/data/*.json` byte-identical to `data/figure_data/`; reruns produce byte-identical files.

### Preview the page locally

```bash
python3 -m http.server 8000 --directory site
```

Then open `http://localhost:8000`. The page loads `data/*.json` with `fetch`, so it needs a server; opening the file directly won't work.

### Deploy with GitHub Pages

1. Set `git config user.name` and `git config user.email` (once per machine).
2. Create a **public** repository on github.com, then commit and push this folder to `main`.
3. Settings → Pages → Build and deployment → Source: **GitHub Actions**. `.github/workflows/pages.yml` publishes `site/` on every push to `main`. The URL is `https://<user>.github.io/<repo>/`.
4. Fill the AI-use statement in the footer of `site/index.html` (search for `data-todo`). The repository link is already filled in.

### Streamlit version

The same story as a Streamlit app. Text comes from `streamlit_app/teks.py` (identical to `site/`); numbers come from `site/data/*.json`. The guesses, per-section and global easy mode, the "Hanya MLv" switch, the spike cards and Cek judulmu are Streamlit widgets. Differences from the web page:

- no scroll animations: figures appear in their final state, like the print version;
- no hover tooltips on the charts;
- Figure 5 uses short spike labels, with the full names in the spike card;
- the "Versi mudah untuk semua" toggle has no mixed state.

Run locally from the repository root:

```bash
.venv/bin/pip install -r streamlit_app/requirements.txt
.venv/bin/streamlit run streamlit_app/app.py
```

Deploy on Streamlit Community Cloud (free; it needs the same public GitHub repository):

1. Push this repository to GitHub (see the GitHub Pages steps above).
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub and choose **Create app**.
3. Pick the repository, branch `main`, and main file path `streamlit_app/app.py`. Under *Advanced settings*, choose Python 3.12. Click **Deploy**.
4. The URL is `https://<chosen-name>.streamlit.app`; you can change the subdomain in the app settings. Free apps go to sleep after a while without visitors and wake up when someone opens them.
5. Fill `AI_STATEMENT` at the top of `streamlit_app/app.py` (it shows as a placeholder until then). `REPO_URL` is already filled in.

### Page technology

Plain HTML/CSS/JS. D3 7.9.0 and Scrollama 3.2.0 load from pinned jsDelivr URLs; Nunito loads from Google Fonts. There are no other runtime requests. `localStorage` holds only the global "Versi mudah untuk semua" choice. Every visible string comes verbatim from the page copy (`05_page_copy.md` in the build package).

### Earlier static version (archived)

`archive/` holds the first, static version of this story: its pipeline, notebook, figures, story builder, reports, data and planning documents. The files above replace it, and it is not maintained. See `archive/README.md`.
