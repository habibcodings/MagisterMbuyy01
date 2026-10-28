# Storyboard dan Justifikasi Desain

**Kelompok:** Yasmina Arethaya Hanjani · Cut Nabilah Nuur Azizah
**Judul cerita:** *Bukan Bumi yang Makin Gaduh, Telinga Kita yang Makin Tajam*

**Pesan utama** (kalimat pertama di halaman):
> Jumlah gempa yang diumumkan BMKG naik lima kali lipat dari 2020 ke 2025, tetapi menurut angka BMKG sendiri gempa M5 ke atas justru turun dari 244 menjadi 153, sehingga yang bertambah adalah gempa kecil yang kini lebih banyak terekam, bukan gempa yang lebih kuat.

---

## 1. Bentuk cerita: interaktif, tetapi terarah

Ceritanya berupa halaman web satu kolom berbahasa Indonesia, dengan **6 gambar** dan **1 gambar yang dibuang** di lampiran. Dashboard membiarkan pembaca mencari sendiri. Cerita ini justru menuntun pembaca, dan interaksi hanya dipakai bila memperkuat alur.

Strukturnya mengikuti pola *martini glass*. Bagian awal sampai tengah dikendalikan penulis lewat gulir: setiap langkah membuka satu anotasi. Baru di akhir pembaca mendapat satu alat untuk mencoba sendiri.

| Interaksi | Gunanya bagi cerita | Di mana |
|---|---|---|
| Langkah gulir (*scrollytelling*) | Perhatian diarahkan satu temuan pada satu waktu, sesuai urutan setup, konflik, resolusi. | Semua gambar |
| "Tebak dulu" | Pembaca berkomitmen pada dugaannya sebelum fakta kunci dibuka, jadi konfliknya terasa sebagai kejutan. | G1 (arah M5+), G2 (berapa dari 100) |
| Tombol **Versi mudah** di setiap gambar | Hanya bagian itu yang berubah: grafik berubah bentuk menjadi satu blok sederhana, dan paragrafnya menjadi satu kalimat yang bisa dikutip. Halaman lain tidak berubah. | Semua gambar dan pembuka |
| Kontrol "Hanya MLv" | Menjawab keraguan bahwa pergeseran ini disebabkan oleh pergantian jenis magnitudo. | G3 |
| Ketuk lonjakan | Setiap lonjakan menampilkan nama dan bulannya. | G5 |
| Alat **Cek judulmu** | Mengubah keputusan audiens menjadi tindakan. Pembaca memasukkan angka rilis BMKG dan mendapat kata kerja judul yang tepat. | Setelah G6 |

**Batas 7 gambar:**
- Versi mudah *menggantikan* gambarnya di tempat, tidak ditampilkan bersamaan. Pembaca selalu hanya melihat 6 gambar.
- Alat Cek judulmu berupa teks tanpa grafik.
- Gambar yang dibuang ada di lampiran, sehingga jumlah gambar di halaman 6 + 1 = 7.

Untuk versi PDF, setiap gambar ditampilkan dalam keadaan akhirnya dan semua kontrol disembunyikan.

---

## 2. Alur

| Bagian | Kalimat kunci | Gambar | Interaksi |
|---|---|---|---|
| Pembuka | Pesan utama, lalu: "Januari 2025, berita menulis gempa 'makin sering'. Gempa apa yang sebenarnya bertambah?" | — | Versi mudah: kartu kalimat sederhana |
| **Setup** | "Angka yang diumumkan BMKG naik lima kali lipat dalam lima tahun." | G1 (panel atas) | Langkah gulir |
| **Konflik 1** | "Tetapi menurut rilis yang sama, gempa M5+ justru turun." | G1 (panel bawah) | Tebak dulu: naik, tetap, atau turun? |
| **Konflik 2** | "Katalog publik BMKG menunjukkan pola yang sama sejak 2009: 97 dari 100 gempa tambahan adalah gempa kecil." | G2 | Tebak dulu: berapa dari 100? |
| *(penghubung)* | "Kepala BMKG saat itu menyatakan kenaikan ini bukan karena alat bertambah. Mari lihat jejak yang direkam katalognya sendiri." | — | — |
| **Konflik 3** | "Yang bertambah hanya sisi kiri kurva, yaitu gempa kecil, juga dalam satu jenis magnitudo." | G3 | Hanya MLv |
| **Konflik 4** | "Gempa berukuran sama kini terekam oleh dua kali lebih banyak bacaan seismik." | G4 | Langkah gulir |
| **Resolusi 1** | "Lonjakan yang layak jadi judul punya nama, tempat, dan akhir." | G5 | Ketuk lonjakan |
| **Resolusi 2** | "'Biasa' bagi Indonesia sudah tinggi, dan itulah alasan untuk bersiap." | G6 | Cek judulmu + daftar periksa |
| Penutup | Keterbatasan data, sumber, gambar yang dibuang | GX | — |

---

## 3. Sistem visual

**Warna data (tetap di semua gambar):**
- **Oranye `#C2410C`** = gempa yang lebih kuat (M5+ di rilis BMKG, M4+ di katalog).
- **Abu-abu `#B8BEC6`** = gempa yang lebih kecil. Label teksnya memakai `#6B7280`.
- **Slate `#475569`** = angka yang tidak dipisah menurut kekuatan, misalnya total atau jumlah bacaan.

Pembaca mempelajari arti oranye di G1 dan memakainya sampai G6. Warna merah muda antarmuka (tombol, progres) tidak pernah dipakai di grafik.

**Judul dan anotasi:**
- Judul setiap gambar menyatakan temuan, bukan nama variabel.
- Setiap gambar punya satu sorotan utama, label langsung tanpa legenda, catatan, dan baris sumber.
- Angka memakai format Indonesia: 1.755; M3,4; ×5,3.

**Aturan hitung katalog:**
- Wilayah: kotak 11° LS–6° LU, 94°–142° BT.
- Magnitudo dibulatkan ke satu desimal, seperti yang diumumkan BMKG.
- 923 gempa tanpa magnitudo tidak dihitung.
- Tahun atau bulan yang datanya tidak lengkap disetarakan ke panjang penuh. Bulan dengan data kurang dari 15 hari dibiarkan kosong.
- Periode pembanding adalah 2014–2017 dan 2022–2025, dua jendela empat tahun yang datanya lengkap.

---

## 4. Gambar

### G1 — Setup dan konflik pertama: angka yang dicetak wartawan

- **Pertanyaan:** Bagaimana total gempa yang diumumkan BMKG berubah, dan bagaimana jumlah gempa M5+ menurut BMKG sendiri?
- **Data:** Rilis tahunan BMKG 2020–2025 (§7). Totalnya 8.264 · 10.570 · 10.792 · 10.789 · 29.869 · 43.439. Untuk 2024 ada angka kedua, 7.358, yaitu angka akhir tahun yang dirilis 31 Des 2024. Jumlah M5+-nya 244 · 244 · 205 · 219 · 186 · 153. Tipe datanya tahun (diskret) × jumlah (kuantitatif).
- **Bentuk dan alasannya:** Dua panel kolom yang disejajarkan pada sumbu tahun yang sama. Panel atas menampilkan total, panel bawah menampilkan M5+, dan masing-masing sumbu Y dimulai dari nol.
  - Kedua besaran berbeda 30–280 kali lipat. Kalau digambar pada satu sumbu, M5+ tidak akan terlihat.
  - *Ditolak:* kolom bertumpuk (M5+ kurang dari 1% kolom 2025), sumbu ganda (tinggi batang seolah bisa dibandingkan), dan garis indeks (menyembunyikan angka absolut yang dikutip wartawan).
- **Pengarahan perhatian:**
  - Panel atas berwarna slate dengan kurung "×5,3" dari 2020 ke 2025.
  - Untuk 2024, penanda kosong di 7.358 menunjukkan bahwa BMKG merilis dua angka.
  - Panel bawah berwarna oranye dengan label "244 → 153".
  - Urutan baca: panel atas, lalu turun ke panel bawah.
- **Langkah gulir:**
  1. Hanya batang 2020 yang tampil.
  2. Batang 2021–2025 tumbuh dan kurung ×5,3 muncul.
  3. Dua angka 2024 disorot.
  4. Pertanyaan "tebak dulu" tampil.
  5. Panel bawah terbuka.
- **Versi mudah:** Blok *compare* oranye: 2020 = 244, 2025 = 153. Kalimatnya: "BMKG mengumumkan lima kali lebih banyak gempa pada 2025 dibanding 2020, tetapi gempa M5 ke atas justru berkurang dari 244 menjadi 153."

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

### G2 — Konflik kedua: pola yang sama di katalog publik, sejak 2009

- **Pertanyaan:** Dalam rentang yang lebih panjang dan pada batas yang lebih halus (M4), gempa mana yang bertambah?
- **Data:** Katalog, tahun × jumlah, dibagi menjadi di bawah M4 dan M4+ untuk 2009–2025.
- **Bentuk dan alasannya:** Kolom bertumpuk dengan **M4+ di dasar**. Karena berada di garis nol, datarnya M4+ bisa dibaca langsung, dan totalnya tetap terlihat.
  - *Ditolak:* 100% bertumpuk (M4+ akan tampak menurun), dua garis terpisah (totalnya hilang), dan sumbu ganda.
- **Pengarahan perhatian:**
  - Pita oranye muda menandai rentang 1.755–3.042, yaitu minimum dan maksimum M4+ sejak 2009.
  - Kolom 2025 diberi label.
  - Pita slate menandai kedua periode pembanding.
- **Langkah gulir:**
  1. Tebak dulu: dari 100 gempa tambahan, berapa yang M4+?
  2. Kolom total tampil, bersama catatan bahwa katalog ini cocok dengan angka akhir tahun BMKG hingga 2024.
  3. Kolom dipecah menjadi oranye dan abu-abu.
  4. Pita rentang M4+ muncul.
  5. Label 2025 tampil.
- **Versi mudah:** Blok *dots* oranye: 3 dari 100. Kolom-kolomnya berubah bentuk menjadi 100 titik. Kalimatnya: "Dari setiap 100 gempa tambahan di katalog BMKG, hanya 3 yang berkekuatan M4 ke atas; 97 sisanya gempa kecil."

```
 gempa per tahun                       2025: total tertinggi, tetapi M4+ --+
 20.000 |                                                                  v
        |                                                                  .
        |                                          .                       .
 10.000 |                         .  .  .   .   .  .  .  .                 .
        |          .  .  .  .  .  .  .  .   .   .  .  .  .  .              .
        |  [##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##=##] <- pita 1.755-3.042
        +-------------------------------------------------------------------------
         2009                                                            2025
         # = M4+ (oranye)    . = di bawah M4 (abu-abu)
```

**Penghubung (teks):**
- Untuk 2025, dan untuk angka 29.869 pada 2024, BMKG belum merilis rincian per kejadian.
- Kepala BMKG saat itu menolak anggapan bahwa kenaikan ini terjadi karena alat bertambah. Menurutnya, ada sekitar 170 sensor pada 2009–2019, dan pada 2020, ketika sudah ada lebih dari 300 seismograf, jumlah gempa justru turun.
- BMKG juga melaporkan membangun 95 seismograf baru pada 2023, sehingga totalnya 533.
- Lonjakan 2018–2019 memang memuat rangkaian gempa sungguhan, seperti yang terlihat di G5.

### G3 — Konflik ketiga: jejak deteksi

- **Pertanyaan:** Bagaimana *sebaran* kekuatan gempa berubah antara kedua periode?
- **Data:** Katalog, magnitudo (per 0,1) × jumlah per tahun, untuk 2014–2017 dan 2022–2025.
- **Bentuk dan alasannya:** Dua poligon frekuensi yang ditumpuk pada sumbu Y linear. Pembaca melihat garisnya berpisah jauh di bawah M4 dan berdekatan di atasnya.
  - *Ditolak:* plot Gutenberg–Richter bersumbu log (asing bagi wartawan, jadi dipindah ke notebook), histogram berdampingan, dan box plot.
- **Rentang:** Sumbu X dari M1,0 sampai M6,0 tanpa bin gabungan. Sumbu Y dari 0 sampai 700.
- **Pengarahan perhatian:**
  - Garis 2014–2017 putus-putus abu tua. Garis 2022–2025 tegas dan gelap.
  - Latar di bawah M4 berwarna abu-abu, dan dari M4 ke atas oranye muda.
  - Panah menunjuk pergeseran puncak dari M3,4 ke M3,0.
- **Langkah gulir:**
  1. Kurva 2014–2017 tergambar.
  2. Kurva 2022–2025 tergambar, bersama panah puncak.
  3. Latar dua wilayah muncul.
  4. Kontrol "Hanya MLv" tampil. Dengan satu jenis magnitudo saja (2014–2017 dibanding 2025), puncaknya bergeser dari M3,4 ke M2,7, jadi polanya tetap.
- **Versi mudah:** Blok *compare* abu-abu: 2014–2017 = 212, 2022–2025 = 618 (gempa sekitar M3 per tahun). Kalimatnya: "Gempa kecil sekitar M3 kini tercatat hampir tiga kali lebih banyak setiap tahun, sementara gempa sekitar M4,5 hampir tidak berubah."

```
 gempa per tahun
 700 |
     |            .-.            <- 2022-2025 (tegas), puncak M3,0
     |           /   \
 300 |          /  .-.\.          <- 2014-2017 (putus-putus), puncak M3,4
     |        _/ ./   \ \.
     |   ___.' ./      '-.'-.___________
     +-----+-----+-----+-----+-----+
     1,0   2,0   3,0   4,0   5,0   6,0      magnitudo
     [:::: abu-abu < M4 ::::][ oranye M4+ ]
     [ Semua jenis | Hanya MLv ]   <- kontrol
```

### G4 — Konflik keempat: lebih banyak "telinga" untuk setiap gempa

- **Pertanyaan:** Apakah jaringan kini mengukur setiap gempa dengan lebih rapat?
- **Data:** Katalog, tahun × median jumlah bacaan fase, hanya gempa M4,0–4,9. Ukurannya ditahan tetap supaya bukan "gempa besar dibaca lebih banyak stasiun".
- **Bentuk dan alasannya:** Garis dengan titik dan pita antarkuartil. Kemiringannya adalah pesannya, dan pita menunjukkan bahwa perubahan ini bukan ulah pencilan.
  - *Ditolak:* kolom median dan sebaran semua kejadian.
- **Pengarahan perhatian:**
  - Garis dan pitanya slate, karena ini jumlah bacaan, bukan jumlah gempa.
  - Pita periode diberi label median 20 dan 44.
- **Langkah gulir:**
  1. Garis tergambar sampai 2019.
  2. Lonjakan 2020–2022 digambar.
  3. Label kedua median muncul.
- **Versi mudah:** Blok *compare* slate: 20 → 44. Kalimatnya: "Gempa yang ukurannya sama kini terekam oleh dua kali lebih banyak bacaan alat, tanda jaringan pemantau yang makin peka."

```
 bacaan fase (median)
 50 |                                   :     o      :
    |                                   :  o / \  o  :
 40 |                                   : / \/   \/  :
 30 |                          o--o     :  median 44 :
 20 |   :  o--o--o--o  :  o--o'         :            :
 10 |  o: median 20    :
    +-----------------------------------------------
     2009 2014-2017              2022-2025
```

### G5 — Resolusi pertama: seperti apa lonjakan sungguhan

- **Pertanyaan:** Ketika gempa M4+ benar-benar melonjak, apa penyebabnya?
- **Data:** Katalog, jumlah gempa M4+ per bulan dari Nov 2008 sampai Jul 2026 (210 bulan).
  - Bulan yang datanya tidak lengkap disetarakan ke satu bulan penuh.
  - Sep 2009 dan Jul–Agu 2013 dibiarkan kosong, dan garisnya terputus.
- **Bentuk dan alasannya:** Garis bulanan. Dengan 210 titik, bentuknya (dasar datar dengan lonjakan singkat) adalah pesannya.
  - *Ditolak:* heatmap kalender dan peta.
- **Aturan label:**
  - Bulan yang mencapai 1,75× bulan biasa diberi label. Mediannya 179, jadi ambangnya 313. Hasilnya tepat 6 bulan, dan bulan berikutnya hanya 307.
  - Setiap label memakai nama rangkaian gempa penyumbang terbesar, tanpa magnitudo karena magnitudo katalog bersifat pendahuluan.
  - Lonjakan Palu (Sep 2018, 305) berada di bawah ambang dan disebut di teks.
- **Pengarahan perhatian:** Garis oranye, garis median putus-putus, dan enam titik berlabel yang muncul satu per satu.
- **Interaksi:** Mengetuk sebuah lonjakan menampilkan kartu kecil berisi nama, bulan, jumlah, dan kelipatannya terhadap bulan biasa.
- **Versi mudah:** Blok *compare* oranye: Bulan biasa = 179, Nov 2019 (Laut Maluku) = 397. Kalimatnya: "Lonjakan sungguhan terjadi singkat dan punya nama tempat, seperti Laut Maluku pada November 2019, ketika gempa M4 ke atas lebih dari dua kali bulan biasa."

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
      2009   (kosong 2009, 2013)                                Jul 2026
```

### G6 — Resolusi kedua: membaca angka 2026

- **Pertanyaan:** Apakah 2026 sejauh ini tidak biasa?
- **Data:** Katalog, 17 nilai tahunan gempa M4+ (2009–2025) dan laju 2026 (1 Jan–14 Agu, disetarakan setahun).
- **Bentuk dan alasannya:** *Dot strip* satu dimensi. Pertanyaannya adalah di mana satu nilai jatuh dalam sebaran.
  - *Ditolak:* box plot (terlalu abstrak) dan bullet chart (menyiratkan target).
- **Pengarahan perhatian:**
  - Titik tahun-tahun lalu berwarna oranye muda di atas pita rentang 1.755–3.042.
  - Tahun 2013 dan 2019 diberi label.
  - 2026 ditandai dengan belah ketupat oranye tegas.
  - Ada tanda median 2.159.
- **Langkah gulir:**
  1. Titik-titik tahun tampil.
  2. Pita rentang dan median muncul.
  3. Belah ketupat 2026 tampil.
- **Setelah G6:**
  - Alat **Cek judulmu**: pembaca memilih tahun 2021–2025 atau memasukkan angka rilis baru (total dan M5+ tahun ini serta tahun lalu), lalu mendapat saran kata kerja judul. Aturannya sama dengan keputusan di brief.
  - Daftar periksa empat langkah untuk wartawan.
- **Versi mudah:** Blok *number* oranye: 6. Kalimatnya: "Rata-rata ada sekitar 6 gempa M4 ke atas setiap hari di Indonesia; angka ini sudah tinggi, dan 2026 sejauh ini masih di kisaran yang sama."

```
 2013: 1.755                  2026 (s.d. 14 Agu): ±2.430           2019: 3.042
    |                                |                                |
    o  o o o o   o  o o  o o  o   o  <>     o                         o
 [===================== Rentang 2009-2025 ===============================]
 +---------+---------+---------+---------+---------+---------+---------+---------+
 1.600     1.800     2.000     2.200     2.400     2.600     2.800     3.000     3.200
                    Median: 2.159 per tahun = 6 gempa M4+ setiap hari
```

---

## 5. Gambar yang dibuang (GX, di lampiran)

**Isinya:** garis kumulatif jumlah kode stasiun BMKG di wilayah analisis menurut tanggal berlaku paling awal, 2008–2025. Jumlahnya naik dari 369 (2017) menjadi 1.314 (2025), atau ×3,6.

**Aturan hitung:**
- Satu baris per kode.
- 35 kode bertanggal 1 Jan 1970 atau 1 Jan 1980 adalah tanggal pengganti dan tidak dihitung.
- Tanggal dibaca dengan parser ISO-8601, karena 50 baris memiliki pecahan detik.

**Alasan dibuang:**
- Tabel ini mencampur seismograf dengan jenis sensor lain.
- Tanggalnya bukan tanggal pemasangan.
- Angkanya berbeda dengan jumlah sensor yang disebut BMKG (±170, lalu 300+, lalu 533).
- Gambar ini akan memindahkan perdebatan ke soal jumlah alat, yang tidak bisa dijawab data ini. G4 mengukur deteksi dari katalog itu sendiri.

**Juga dipertimbangkan, tidak digambar:** peta titik 144.030 gempa. Peta itu terlalu padat, menunjukkan *di mana* alih-alih *apa yang berubah*, dan merupakan analisis yang paling umum untuk dataset ini.

---

## 6. Keterbatasan data (disebut di cerita)

1. **Angka rilis BMKG berasal dari pemberitaan.** Penulisan batas M5 berbeda-beda antarrilis. Bila media berbeda angka (satu media menulis 10.983 untuk 2023), kami memakai angka yang dimuat dua media (10.789).
2. **BMKG merilis dua total untuk 2024** (7.358 dan 29.869) tanpa penjelasan. G1 menampilkan keduanya.
3. **Katalog publik hanya sebagian cocok dengan rilis.** Selisihnya kurang dari 5% dari angka akhir tahun BMKG untuk 2020–2024. Untuk 2025, katalog hanya memuat 43% dari 43.439.
4. **Wilayah berupa kotak koordinat**, sehingga mencakup wilayah perbatasan (misalnya Mindanao di G5).
5. **Ada 143 hari tanpa data.** Hari-hari itu adalah celah pengumpulan, bukan hari tanpa gempa.
6. **Jenis magnitudo berganti antartahun** (MLv dan "M" tanpa label). Kami menguji pola di dalam satu jenis (G3, G4). Magnitudo gempa kecil tidak bisa dicek terhadap skala independen, sehingga G3–G4 dibingkai sebagai *konsisten dengan* deteksi yang lebih baik.
7. **Katalog bersifat pendahuluan**, sehingga tidak ada magnitudo di label G5.
8. **Jumlah gempa bukan dampak.** Cerita ini tidak membuat klaim tentang kerugian.

---

## 7. Sumber

- **S1.** Vigiliant, A. K. *Earthquakes in Indonesia* (katalog v2) [dataset]. Kaggle. https://doi.org/10.34740/kaggle/ds/1934565. Diunduh 28 Oktober 2026. Kode sumber: github.com/kekavigi/repo-gempa, commit 539ed6e.
- **S2.** BMKG. RepoGempa event catalog. https://repogempa.bmkg.go.id/eventcatalog
- **S3.** CNN Indonesia, 30 Des 2021. "Aktivitas Gempa di Indonesia Meningkat Sepanjang 2021." https://www.cnnindonesia.com/teknologi/20211230134505-199-740553/aktivitas-gempa-di-indonesia-meningkat-sepanjang-2021
- **S4.** Antara News. "Ini jumlah rata-rata banyaknya gempa di Indonesia dalam setahun." https://www.antaranews.com/berita/4191750/ini-jumlah-rata-rata-banyaknya-gempa-di-indonesia-dalam-setahun
- **S5.** Beritasatu. "BMKG Catat 10.789 Gempa Bumi di Indonesia Sepanjang 2023." https://www.beritasatu.com/nusantara/2791754/bmkg-catat-10789-gempa-bumi-di-indonesia-sepanjang-2023
- **S6.** IDX Channel, 31 Des 2024. "BMKG: 7.358 Gempa Bumi Guncang Indonesia Sepanjang 2024." https://www.idxchannel.com/news/bmkg-7358-gempa-bumi-guncang-indonesia-sepanjang-2024
- **S7.** IDX Channel, 17 Jan 2025. "Indonesia Diguncang Hampir 30.000 Gempa Bumi Sepanjang 2024." https://www.idxchannel.com/news/indonesia-diguncang-hampir-30000-gempa-bumi-sepanjang-2024
- **S8.** Okezone, 17 Jan 2025. "BMKG: 29.869 Gempa Terjadi di Tahun 2024, 20 di Antaranya Merusak." https://news.okezone.com/read/2025/01/17/337/3105363/bmkg-29-869-gempa-terjadi-di-tahun-2024-20-di-antaranya-merusak
- **S9.** CNBC Indonesia, 21 Jan 2025. "Gempa Makin Sering-Megathrust Ancam RI, Kepala BMKG Beri Warning Keras." https://www.cnbcindonesia.com/news/20250121140939-4-604849/gempa-makin-sering-megathrust-ancam-ri-kepala-bmkg-beri-warning-keras
- **S10.** kumparan, 2 Jan 2026. "BMKG Catat 43.439 Gempa Terjadi di Indonesia Sepanjang 2025." https://kumparan.com/kumparannews/bmkg-catat-43-439-gempa-terjadi-di-indonesia-sepanjang-2025-26YLtQKF0D1
- **S11.** Daryono (BMKG), "Refleksi Gempa 2022" (paparan, Teknik Geofisika ITS). https://www.its.ac.id/tgeofisika/wp-content/uploads/sites/33/2022/12/REFLEKSI-GEMPA-2022-DARYONO-BMKG.pdf
- **S12.** Diantari, H. C. (2017). *Kuantifikasi Kelengkapan Magnitudo pada Katalog Modern BMKG (2008–2016) dalam Pemantauan Gempabumi Indonesia.* Skripsi, FMIPA UGM. https://etd.repository.ugm.ac.id/penelitian/detail/114101
