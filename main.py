from utils.extract import scrape_product
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_postgresql

def main():
    BASE_URL_TEMPLATE = 'https://fashion-studio.dicoding.dev/page{}'
    FIRST_PAGE_URL = 'https://fashion-studio.dicoding.dev/'

    raw_data = scrape_product(BASE_URL_TEMPLATE, FIRST_PAGE_URL)
    if not raw_data:
        print("❌ Tidak ada data yang diambil.")
        return

    print(f"📦 Data mentah diambil: {len(raw_data)} entri")

    df = transform_data(raw_data)
    print(f"✅ Data setelah transformasi: {len(df)} entri")

    # Simpan ke CSV
    save_to_csv(df)

    # Konfigurasi PostgreSQL
    db_config = {
    "host": "127.0.0.1",
    "port": "5432",
    "dbname": "pentaho_db",
    "user": "postgres",
    "password": "fikadiansari"
}


    # Simpan ke PostgreSQL
    save_to_postgresql(df, db_config)

if __name__ == '__main__':
    main()
