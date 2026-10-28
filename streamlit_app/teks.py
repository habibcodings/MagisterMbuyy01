"""Every visible string of the Streamlit version, verbatim from the page copy (05_page_copy.md), the same text as site/.
Do not edit wording here without editing site/index.html: both must stay identical. {…} marks a value filled from data."""

TITLE = "Bukan Bumi yang Makin Gaduh, Telinga Kita yang Makin Tajam"
HEADER_TITLE = "Telinga yang Makin Tajam"
PROGRESS = [("Setup", "hero"), ("Konflik", "konflik"), ("Resolusi", "g5")]
GLOBAL_TOGGLE = "Versi mudah untuk semua"
GLOBAL_TOGGLE_ARIA = "Ubah semua gambar ke versi mudah"
SECTION_TOGGLE = "Versi mudah"
SECTION_TOGGLE_ARIA = "Tampilkan versi mudah Gambar {n}"
SKIP_LINK = "Langsung ke sumber dan keterbatasan data"
ANNOUNCE_EASY = "Gambar {n} sekarang dalam versi mudah"
ANNOUNCE_CHART = "Gambar {n} sekarang dalam versi grafik"
FIG_NUM = "Gambar {n}"

HERO_KICKER = "CERITA DATA · GEMPA BUMI INDONESIA"
MAIN_MESSAGE = ("Jumlah gempa yang diumumkan BMKG naik lima kali lipat dari 2020 ke 2025, tetapi menurut angka BMKG sendiri gempa M5 "
                "ke atas justru turun dari 244 menjadi 153, sehingga yang bertambah adalah gempa kecil yang kini lebih banyak terekam, "
                "bukan gempa yang lebih kuat.")
PLAIN_CARD = ("BMKG kini mencatat jauh lebih banyak gempa, tetapi gempa yang kuat tidak ikut bertambah; yang bertambah adalah gempa "
              "kecil yang kini lebih mudah terekam. (M4 dan M5 adalah ukuran kekuatan gempa; makin besar angkanya, makin kuat gempanya.)")
BYLINE = ("Yasmina Arethaya Hanjani & Cut Nabilah Nuur Azizah · Visualisasi Data Lanjut, Magister Informatika Telkom University · "
          "Oktober 2026")
SCROLL_CUE = "Gulir untuk mulai"

LEDE = ("Januari 2025, Kepala BMKG mengumumkan 29.869 gempa sepanjang 2024, dan berita menulis gempa “makin sering” "
        "(CNBC Indonesia, 21 Januari 2025). Setahun kemudian angkanya 43.439. Pertanyaannya: gempa apa yang sebenarnya bertambah?")

BRIDGE = ("Kepala BMKG saat itu, Dwikorita Karnawati, menolak anggapan bahwa kenaikan ini terjadi karena alat bertambah: menurutnya "
          "jumlah sensor sekitar 170 pada 2009–2019 ketika jumlah gempa melonjak, dan pada 2020, saat seismograf sudah lebih dari 300, "
          "jumlah gempa justru turun (IDX Channel dan Okezone, 17 Januari 2025). BMKG juga melaporkan membangun 95 seismograf baru pada "
          "2023 sehingga totalnya 533 (Beritasatu). Lonjakan 2018–2019 memang memuat rangkaian gempa sungguhan, seperti terlihat pada "
          "Gambar 5. Tetapi katalog itu sendiri juga merekam jejak deteksi.")
BRIDGE_EASY = "BMKG menyatakan kenaikan ini bukan karena alat bertambah. Mari lihat apa yang direkam katalognya sendiri."

SOURCE_CATALOG = ("Sumber: Katalog gempa BMKG (RepoGempa), dihimpun A. K. Vigiliant, Kaggle, doi:10.34740/kaggle/ds/1934565; "
                  "diunduh 28 Oktober 2026. Wilayah 11° LS–6° LU, 94°–142° BT. Olahan: Hanjani & Azizah.")

FIGS = {
    "g1": dict(
        n=1, kicker="SETUP → KONFLIK",
        title="Total gempa yang diumumkan BMKG naik lima kali lipat, tetapi gempa M5+ menurut BMKG sendiri justru turun",
        subtitle="Angka tahunan dalam rilis BMKG, 2020–2025",
        note=("BMKG mengumumkan dua angka untuk 2024: 7.358 (Direktur Gempabumi dan Tsunami, 31 Des 2024) dan 29.869 (Kepala BMKG, "
              "17 Jan 2025); jumlah M5+ 2024 (186) berasal dari rilis 31 Des 2024. Batas M5 ditulis “di atas M5” atau “M≥5”, "
              "tergantung rilis. Gempa dirasakan: 754 (2020) dan 973 (2025)."),
        source=("Sumber: rilis tahunan BMKG, dikutip CNN Indonesia (30 Des 2021), Antara, Beritasatu, IDX Channel (31 Des 2024), "
                "Okezone (17 Jan 2025) dan kumparan (2 Jan 2026). Olahan: Hanjani & Azizah."),
        alt=("Dua panel kolom. Total gempa yang diumumkan BMKG naik dari 8.264 (2020) menjadi 43.439 (2025), sedangkan gempa M5+ "
             "turun dari 244 menjadi 153."),
        steps=["Pada 2020, BMKG mengumumkan 8.264 gempa di Indonesia.",
               "Lima tahun kemudian, angkanya 43.439. Lima kali lipat.",
               "Untuk 2024, BMKG bahkan merilis dua angka: 7.358 pada 31 Desember 2024, lalu 29.869 dua minggu kemudian."],
        easy=("BMKG mengumumkan lima kali lebih banyak gempa pada 2025 dibanding 2020, tetapi gempa M5 ke atas justru berkurang dari "
              "244 menjadi 153."),
        key="Angkanya naik lima kali lipat, tetapi gempa yang kuat tidak ikut naik.",
        block=dict(type="compare", tone="strong", rows=[("2020", "m5_2020"), ("2025", "m5_2025")]),
    ),
    "g2": dict(
        n=2, kicker="KONFLIK",
        title="Di katalog publik BMKG, 97% kenaikan adalah gempa di bawah M4; gempa M4+ nyaris tidak berubah",
        subtitle="Gempa per tahun menurut kekuatan, katalog RepoGempa, 2009–2025",
        note=("Magnitudo dibulatkan ke satu desimal seperti yang diumumkan BMKG; M4+ berarti M4,0 ke atas. Tahun dengan data tidak "
              "lengkap (2009, 2010, 2013, 2018) disetarakan ke satu tahun penuh. 923 gempa tanpa magnitudo (0,6%) tidak dihitung."),
        source=SOURCE_CATALOG,
        alt=("Kolom bertumpuk per tahun 2009–2025. Bagian oranye (M4+) tetap di kisaran 1.755–3.042 per tahun, sementara bagian "
             "abu-abu (di bawah M4) membesar sehingga total naik dua kali lipat."),
        steps=[None,  # step 1 is the guess
               ("Ini katalog publik BMKG, data yang bisa diunduh siapa pun. Untuk 2020–2024, totalnya selisih kurang dari 5% dari "
                "angka akhir tahun BMKG. Untuk 2025, katalog ini memuat 18.592 gempa, lebih sedikit daripada 43.439 yang diumumkan; "
                "rinciannya belum dirilis."),
               "Pisahkan menurut kekuatan: oranye untuk gempa M4 ke atas, abu-abu untuk gempa di bawah M4.",
               "Sejak 2009, gempa M4+ bertahan di kisaran 1.755–3.042 per tahun.",
               "2025 punya total tertinggi, tetapi jumlah M4+-nya termasuk yang terendah."],
        easy="Dari setiap 100 gempa tambahan di katalog BMKG, hanya 3 yang berkekuatan M4 ke atas; 97 sisanya gempa kecil.",
        key="97 dari 100 gempa tambahan adalah gempa kecil.",
        block=dict(type="dots", tone="strong", highlight=3, caption="3 dari 100"),
    ),
    "g3": dict(
        n=3, kicker="KONFLIK",
        title="Jaringan kini menangkap gempa yang lebih kecil, sementara gempa M4+ nyaris tidak bertambah",
        subtitle="Jumlah gempa per tahun di setiap kekuatan, 2014–2017 dibanding 2022–2025",
        note=("Magnitudo dibulatkan ke 0,1. Gempa di atas M6,0 (±5 per tahun pada 2014–2017, ±13 pada 2022–2025) dan di bawah M1,0 "
              "(±3 per tahun pada 2022–2025) tidak digambar. Mode “Hanya MLv” membandingkan 2014–2017 dengan 2025, tahun ketika "
              "hampir semua gempa memakai MLv."),
        source=SOURCE_CATALOG,
        alt=("Dua kurva sebaran magnitudo. Kurva 2022–2025 jauh lebih tinggi di bawah M4 dengan puncak M3,0, sedangkan di atas M4 "
             "kedua kurva berdekatan."),
        steps=["Begini sebaran kekuatan gempa per tahun pada 2014–2017. Puncaknya di M3,4.",
               "Dan ini 2022–2025. Puncaknya bergeser ke M3,0, dan sisi kirinya melonjak.",
               "Di atas M4, kedua garis berdekatan: gempa M4+ hampir tidak bertambah.",
               ("Ragu karena jenis magnitudo berganti antartahun? Pilih “Hanya MLv”. Dengan satu jenis magnitudo saja, puncaknya "
                "tetap bergeser, dari M3,4 ke M2,7.")],
        easy=("Gempa kecil sekitar M3 kini tercatat hampir tiga kali lebih banyak setiap tahun, sementara gempa sekitar M4,5 hampir "
              "tidak berubah."),
        key="Yang bertambah hanya gempa kecil, dengan jenis magnitudo apa pun.",
        block=dict(type="compare", tone="small", rows=[("2014–2017", "at_3_0[0]"), ("2022–2025", "at_3_0[1]")]),
        modes=["Semua jenis magnitudo", "Hanya MLv"],
    ),
    "g4": dict(
        n=4, kicker="KONFLIK",
        title="Gempa berukuran sama kini terekam oleh dua kali lebih banyak bacaan seismik",
        subtitle="Median jumlah bacaan fase untuk gempa M4,0–M4,9, per tahun, 2009–2025",
        note=("Bacaan fase adalah kedatangan gelombang seismik di stasiun yang dipakai untuk menentukan lokasi gempa. Dengan satu "
              "jenis magnitudo saja (MLv): 18 (2014–2017) → 42 (2025). Perubahan sistem pengolahan juga dapat menambah jumlah bacaan."),
        source=SOURCE_CATALOG,
        alt=("Garis median bacaan fase naik dari sekitar 20 pada 2014–2017 menjadi 44 pada 2022–2025, dengan lonjakan antara 2019 "
             "dan 2022."),
        steps=[("Lokasi sebuah gempa ditentukan dari bacaan gelombangnya di banyak stasiun. Ini median jumlah bacaan untuk gempa "
                "berukuran sama, M4,0–4,9."),
               "Mulai 2020, gempa berukuran sama dibaca oleh jauh lebih banyak stasiun.",
               ("2022–2025: median 44 bacaan, dua kali lipat 2014–2017. Lebih banyak “telinga” untuk setiap gempa, sehingga gempa "
                "kecil pun lebih mudah tertangkap.")],
        easy=("Gempa yang ukurannya sama kini terekam oleh dua kali lebih banyak bacaan alat, tanda jaringan pemantau yang makin "
              "peka."),
        key="Jaringannya makin peka, jadi makin banyak gempa kecil yang tercatat.",
        block=dict(type="compare", tone="neutral", rows=[("2014–2017", "median_A"), ("2022–2025", "median_B")]),
    ),
    "g5": dict(
        n=5, kicker="RESOLUSI",
        title="Lonjakan sungguhan terlihat berbeda: singkat, lokal, dan muncul pada gempa M4+",
        subtitle="Gempa M4+ per bulan, November 2008 – Juli 2026",
        note=("Bulan dengan data tidak lengkap disetarakan ke satu bulan penuh; garis terputus pada bulan dengan data kurang dari 15 "
              "hari (Sep 2009, Jul–Agu 2013). Label: bulan dengan gempa M4+ setidaknya 1,75 kali bulan biasa, dinamai menurut "
              "rangkaian gempa penyumbang terbesar. Wilayah analisis mencakup sebagian Filipina selatan."),
        source=SOURCE_CATALOG,
        alt=("Garis bulanan gempa M4+ yang datar di sekitar 180 per bulan, dengan enam lonjakan singkat berlabel: Mentawai 2010, "
             "Lombok 2018, Halmahera dan Laut Maluku 2019, Laut Maluku 2019, Laut Maluku dan Talaud 2023, serta Mindanao 2026."),
        steps=["Lonjakan sungguhan juga ada. Ini jumlah gempa M4+ per bulan sejak akhir 2008.",
               "Bulan biasa: sekitar 180 gempa M4+.",
               ("Hanya enam bulan yang melonjak sampai 1,75 kali bulan biasa atau lebih, dan setiap lonjakan punya nama. (Lonjakan "
                "Palu, September 2018, tepat di bawah batas ini.)"),
               "Ketuk sebuah lonjakan untuk melihat asalnya."],
        easy=("Lonjakan sungguhan terjadi singkat dan punya nama tempat, seperti Laut Maluku pada November 2019, ketika gempa M4 ke "
              "atas lebih dari dua kali bulan biasa."),
        key="Lonjakan yang layak jadi judul punya nama, tempat, dan akhir.",
        block=dict(type="compare", tone="strong", rows=[("Bulan biasa", "median"), ("Nov 2019 (Laut Maluku)", "spike_2019_11")]),
        card="{nama} · {bulan} · {nilai} gempa M4+, {kelipatan}× bulan biasa",
    ),
    "g6": dict(
        n=6, kicker="RESOLUSI",
        title="Laju gempa M4+ 2026 masih dalam rentang biasanya — dan “biasa” bagi Indonesia sudah tinggi",
        subtitle="Gempa M4+ per tahun, 2009–2025, dan laju 2026 hingga 14 Agustus",
        note="Laju 2026 dihitung dari 1 Januari–14 Agustus 2026 dan disetarakan ke satu tahun penuh; angka akhirnya bisa berbeda.",
        source=SOURCE_CATALOG,
        alt=("Titik per tahun untuk gempa M4+ antara 1.755 dan 3.042 per tahun; laju 2026 sekitar 2.430 berada di dalam rentang "
             "itu."),
        steps=["Setiap titik adalah satu tahun: jumlah gempa M4+ di katalog.",
               "Rentangnya dari 1.755 (2013) sampai 3.042 (2019). Mediannya 2.159 per tahun, sekitar 6 gempa M4+ setiap hari.",
               "Dan 2026 sejauh ini? Sekitar 2.430 per tahun, masih di dalam rentang."],
        easy=("Rata-rata ada sekitar 6 gempa M4 ke atas setiap hari di Indonesia; angka ini sudah tinggi, dan 2026 sejauh ini masih "
              "di kisaran yang sama."),
        key="“Biasa” bagi Indonesia sudah tinggi, dan itulah alasan untuk bersiap.",
        block=dict(type="number", tone="strong", value=6),
    ),
}

G1_GUESS = dict(
    kicker="Tebak dulu.",
    question="Bagaimana dengan gempa M5 ke atas, gempa yang lebih kuat? Dari 2020 ke 2025, menurutmu jumlahnya…",
    buttons=[("naik", "Naik"), ("tetap", "Tetap"), ("turun", "Turun")],
    skip="Lewati, tunjukkan saja",
    turun="Tepat. Gempa M5+ turun dari 244 menjadi 153.",
    other="Banyak yang menduga begitu. Faktanya, gempa M5+ turun dari 244 menjadi 153.",
    skipped="Gempa M5+ turun dari 244 menjadi 153.",
    always="Menurut rilis BMKG sendiri, yang bertambah adalah gempa kecil.",
)
G2_GUESS = dict(
    kicker="Tebak dulu.",
    question=("Katalog publik BMKG mencatat dua kali lebih banyak gempa per tahun pada 2022–2025 dibanding 2014–2017. Dari setiap "
              "100 gempa tambahan itu, menurutmu berapa yang berkekuatan M4 ke atas?"),
    slider="Tebakanmu: {x} dari 100",
    button="Lihat jawabannya",
    skip="Lewati",
    answered="Tebakanmu {x} dari 100. Faktanya: hanya 3.",
    skipped="Hanya 3 dari 100.",
)

TOOL = dict(
    heading="Cek judulmu",
    intro=("Pilih tahun, atau masukkan angka dari rilis BMKG berikutnya. Alat ini menyarankan kata kerja untuk judulmu, mengikuti "
           "daftar periksa di bawah."),
    tabs=["Tahun 2021–2025", "Angka baru"],
    year="Tahun",
    inputs=dict(year="Tahun rilis", total="Total gempa tahun ini", now="Gempa M5+ tahun ini", last="Gempa M5+ tahun lalu",
                felt="Gempa dirasakan tahun ini (opsional)"),
    button="Cek",
    copy="Salin judul",
    copied="Tersalin",
    footnote=("Alat ini memakai aturan sederhana dari cerita ini, bukan model statistik. Rentang 153–244 adalah jumlah M5+ tahunan "
              "dalam rilis BMKG 2020–2025."),
    avoid="Hindari “makin sering”. Tulis “lebih banyak gempa yang tercatat”.",
    a_finding="Gempa M5+ turun dari {last} menjadi {now}.",
    a_headline="BMKG Catat {total} Gempa Sepanjang {tahun}, Gempa M5+ Justru Turun",
    b_finding="Gempa M5+ sama dengan tahun lalu ({now}).",
    b_headline="BMKG Catat {total} Gempa Sepanjang {tahun}; Gempa M5+ Tidak Bertambah",
    c_finding="Gempa M5+ naik dari {last} menjadi {now} (+{pct}%).",
    c_in_range="Masih dalam rentang 2020–2025 (153–244).",
    c_above_range=("Ini di atas rentang 2020–2025 (153–244). Cari rangkaian gempa yang menyebabkannya dan sebut namanya."),
    c_advice="Kata “naik” tepat untuk gempa M5+, bukan untuk total.",
    c_headline="BMKG Catat {total} Gempa Sepanjang {tahun}, Gempa M5+ Naik {pct}%",
    felt_line="Gempa dirasakan: {felt}. Cantumkan di samping total.",
    extra_2024="Catatan: BMKG juga merilis angka 7.358 untuk 2024 (31 Des 2024).",
)

CHECKLIST_TITLE = "Cara membaca angka gempa tahunan BMKG"
CHECKLIST = [
    "Cetak jumlah gempa M5+ dan gempa dirasakan di samping total. Keduanya sudah ada di rilis tahunan BMKG.",
    "Tulis “naik” atau “makin sering” hanya jika jumlah gempa M5+ ikut naik. Jika tidak, tulis “lebih banyak gempa yang tercatat”.",
    "Jika ada lonjakan, sebut nama rangkaian gempanya. Lonjakan sungguhan punya tempat dan akhir.",
    ("Ajak bersiap karena angka dasar Indonesia memang sudah tinggi, sekitar 2.150 gempa M4+ per tahun atau kira-kira enam setiap "
     "hari, bukan karena totalnya naik."),
]

LIMITS_TITLE = "Keterbatasan data"
LIMITS = [  # (text, words to set in italics)
    ("Angka rilis BMKG (Gambar 1) kami ambil dari pemberitaan media. Penulisan batas M5 berbeda-beda antarrilis. Bila media "
     "berbeda angka (satu media menulis 10.983 untuk 2023), kami memakai angka yang dimuat dua media (10.789).", None),
    ("BMKG merilis dua total untuk 2024, yaitu 7.358 dan 29.869, tanpa penjelasan perbedaannya.", None),
    ("Katalog publik (Gambar 2–6) selisih kurang dari 5% dari angka akhir tahun BMKG untuk 2020–2024. Untuk 2025, katalog hanya "
     "memuat 43% dari 43.439 gempa yang diumumkan, dan rinciannya belum dirilis.", None),
    ("Wilayah analisis berupa kotak koordinat, sehingga mencakup sebagian negara tetangga.", None),
    ("Ada 143 hari tanpa data di katalog. Hari-hari itu adalah celah pengumpulan, bukan hari tanpa gempa; tahun dan bulan yang "
     "terdampak disetarakan ke panjang penuh.", None),
    ("Jenis magnitudo di katalog berganti antartahun. Kami menguji pola di dalam satu jenis magnitudo (Gambar 3–4). Magnitudo "
     "gempa kecil tidak bisa dicek terhadap skala independen, sehingga Gambar 3–4 menunjukkan pola yang konsisten dengan deteksi "
     "yang lebih baik, bukan bukti tunggal.", "konsisten dengan"),
    ("Katalog bersifat pendahuluan; magnitudo dan lokasinya bisa direvisi.", None),
    ("Jumlah gempa bukan ukuran dampak. Cerita ini tidak membuat klaim tentang kerusakan atau korban.", None),
]

SOURCES_TITLE = "Sumber"
SOURCES = [  # (label, text before the link, link text, url, text after the link)
    ("S1.", "Vigiliant, A. K. <em>Earthquakes in Indonesia</em> (katalog v2) [dataset]. Kaggle.",
     "https://doi.org/10.34740/kaggle/ds/1934565", "https://doi.org/10.34740/kaggle/ds/1934565",
     ". Diunduh 28 Oktober 2026. Kode sumber: <a href=\"https://github.com/kekavigi/repo-gempa/tree/539ed6e461c409da1475781fd57bbc6deaef66ef\">github.com/kekavigi/repo-gempa, commit 539ed6e</a>."),
    ("S2.", "BMKG. RepoGempa event catalog.", "https://repogempa.bmkg.go.id/eventcatalog", "https://repogempa.bmkg.go.id/eventcatalog", ""),
    ("S3.", "CNN Indonesia, 30 Des 2021. \"Aktivitas Gempa di Indonesia Meningkat Sepanjang 2021.\"",
     "https://www.cnnindonesia.com/teknologi/20211230134505-199-740553/aktivitas-gempa-di-indonesia-meningkat-sepanjang-2021",
     "https://www.cnnindonesia.com/teknologi/20211230134505-199-740553/aktivitas-gempa-di-indonesia-meningkat-sepanjang-2021", ""),
    ("S4.", "Antara News. \"Ini jumlah rata-rata banyaknya gempa di Indonesia dalam setahun.\"",
     "https://www.antaranews.com/berita/4191750/ini-jumlah-rata-rata-banyaknya-gempa-di-indonesia-dalam-setahun",
     "https://www.antaranews.com/berita/4191750/ini-jumlah-rata-rata-banyaknya-gempa-di-indonesia-dalam-setahun", ""),
    ("S5.", "Beritasatu. \"BMKG Catat 10.789 Gempa Bumi di Indonesia Sepanjang 2023.\"",
     "https://www.beritasatu.com/nusantara/2791754/bmkg-catat-10789-gempa-bumi-di-indonesia-sepanjang-2023",
     "https://www.beritasatu.com/nusantara/2791754/bmkg-catat-10789-gempa-bumi-di-indonesia-sepanjang-2023", ""),
    ("S6.", "IDX Channel, 31 Des 2024. \"BMKG: 7.358 Gempa Bumi Guncang Indonesia Sepanjang 2024.\"",
     "https://www.idxchannel.com/news/bmkg-7358-gempa-bumi-guncang-indonesia-sepanjang-2024",
     "https://www.idxchannel.com/news/bmkg-7358-gempa-bumi-guncang-indonesia-sepanjang-2024", ""),
    ("S7.", "IDX Channel, 17 Jan 2025. \"Indonesia Diguncang Hampir 30.000 Gempa Bumi Sepanjang 2024.\"",
     "https://www.idxchannel.com/news/indonesia-diguncang-hampir-30000-gempa-bumi-sepanjang-2024",
     "https://www.idxchannel.com/news/indonesia-diguncang-hampir-30000-gempa-bumi-sepanjang-2024", ""),
    ("S8.", "Okezone, 17 Jan 2025. \"BMKG: 29.869 Gempa Terjadi di Tahun 2024, 20 di Antaranya Merusak.\"",
     "https://news.okezone.com/read/2025/01/17/337/3105363/bmkg-29-869-gempa-terjadi-di-tahun-2024-20-di-antaranya-merusak",
     "https://news.okezone.com/read/2025/01/17/337/3105363/bmkg-29-869-gempa-terjadi-di-tahun-2024-20-di-antaranya-merusak", ""),
    ("S9.", "CNBC Indonesia, 21 Jan 2025. \"Gempa Makin Sering-Megathrust Ancam RI, Kepala BMKG Beri Warning Keras.\"",
     "https://www.cnbcindonesia.com/news/20250121140939-4-604849/gempa-makin-sering-megathrust-ancam-ri-kepala-bmkg-beri-warning-keras",
     "https://www.cnbcindonesia.com/news/20250121140939-4-604849/gempa-makin-sering-megathrust-ancam-ri-kepala-bmkg-beri-warning-keras", ""),
    ("S10.", "kumparan, 2 Jan 2026. \"BMKG Catat 43.439 Gempa Terjadi di Indonesia Sepanjang 2025.\"",
     "https://kumparan.com/kumparannews/bmkg-catat-43-439-gempa-terjadi-di-indonesia-sepanjang-2025-26YLtQKF0D1",
     "https://kumparan.com/kumparannews/bmkg-catat-43-439-gempa-terjadi-di-indonesia-sepanjang-2025-26YLtQKF0D1", ""),
    ("S11.", "Daryono (BMKG), \"Refleksi Gempa 2022\" (paparan, Teknik Geofisika ITS).",
     "https://www.its.ac.id/tgeofisika/wp-content/uploads/sites/33/2022/12/REFLEKSI-GEMPA-2022-DARYONO-BMKG.pdf",
     "https://www.its.ac.id/tgeofisika/wp-content/uploads/sites/33/2022/12/REFLEKSI-GEMPA-2022-DARYONO-BMKG.pdf", ""),
    ("S12.", ("Diantari, H. C. (2017). <em>Kuantifikasi Kelengkapan Magnitudo pada Katalog Modern BMKG (2008–2016) dalam "
              "Pemantauan Gempabumi Indonesia.</em> Skripsi, FMIPA UGM."),
     "https://etd.repository.ugm.ac.id/penelitian/detail/114101", "https://etd.repository.ugm.ac.id/penelitian/detail/114101", ""),
]
REPO_LINE = "Data katalog diunduh 28 Oktober 2026. Seluruh angka dan gambar dapat dihasilkan ulang dari repositori: {link}."
REPO_PLACEHOLDER = "{link repositori}"

GX = dict(
    heading="Gambar yang kami buang",
    title="Jumlah kode stasiun BMKG di wilayah Indonesia naik lebih dari tiga kali lipat sejak 2017",
    subtitle="Kode stasiun kumulatif menurut tanggal berlaku paling awal, 2008–2025",
    note=("35 kode bertanggal 1 Januari 1970 atau 1 Januari 1980 (tanggal pengganti) tidak dihitung. Sekitar 60% tanggal jatuh "
          "pada 1 Januari, sehingga ketepatannya hanya per tahun. Tabel ini mencampur seismograf dengan jenis sensor lain."),
    source=("Sumber: Tabel stasiun BMKG (katalog_sensor.tsv), dihimpun A. K. Vigiliant, Kaggle, doi:10.34740/kaggle/ds/1934565; "
            "diunduh 28 Oktober 2026. Olahan: Hanjani & Azizah."),
    reason=("Gambar ini tampak membuktikan jaringan makin rapat, tetapi tabelnya mencampur seismograf dengan sensor jenis lain, "
            "tanggalnya bukan tanggal pemasangan, dan angkanya berbeda dengan jumlah sensor yang disebut BMKG. Gambar ini akan "
            "memindahkan perdebatan ke soal berapa jumlah alat, yang tidak bisa dijawab data ini. Kami menggantinya dengan Gambar 4, "
            "yang memakai ukuran dari katalog itu sendiri."),
)

FOOTER_REPRO = "Reproduksi: {link}"
FOOTER_REPRO_PLACEHOLDER = "{link repositori GitHub}"
FOOTER_AI = "Pernyataan penggunaan AI: {isi}"
FOOTER_AI_PLACEHOLDER = "{isi sesuai ketentuan bagian 6 panduan mata kuliah}"
FOOTER_COPYRIGHT = "© 2026 Yasmina Arethaya Hanjani & Cut Nabilah Nuur Azizah"
