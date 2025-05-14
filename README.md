# proyek_ETL
# Deskripsi:
ETL pipeline ini mengambil data dari situs https://fashion-studio.dicoding.dev, lalu mengekstrak, mentransformasi, dan menyimpannya ke dalam database PostgreSQL. Data hasil transformasi juga disimpan sebagai cadangan ke dalam file `products.csv`.

Struktur pipeline:
1. **utils/extract.py** – mengekstrak data HTML dari website.
2. **utils/transform.py** – membersihkan dan mengonversi data (seperti harga dan warna).
3. **utils/load.py** – menyimpan hasil akhir ke PostgreSQL dan/atau CSV.
4. **main.py** – menggabungkan proses ETL end-to-end.
5. **tests/** – berisi unit test untuk masing-masing modul (dengan test coverage >80%).

# Teknologi:
- Python
- BeautifulSoup4
- Pandas
- PostgreSQL (via psycopg2)
- unittest / pytest
- Coverage

  Test Coverage: 83%
