import pandas as pd
import psycopg2
from psycopg2 import sql
import os


def save_to_csv(df: pd.DataFrame, filename: str = "products.csv"):
    try:
        df.to_csv(filename, index=False)
        print(f"📁 Data berhasil disimpan ke CSV: {filename}")
    except Exception as e:
        print(f"❌ Gagal menyimpan ke CSV: {e}")

def save_to_postgresql(df: pd.DataFrame, db_config: dict):
    conn = None
    cursor = None
    try:
        # Koneksi ke database PostgreSQL
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            dbname=db_config['dbname'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()

        # Membuat tabel jika belum ada
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            price INTEGER,
            rating FLOAT,
            colors INTEGER,
            size TEXT,
            gender TEXT,
            timestamp TIMESTAMP
        )
        '''
        cursor.execute(create_table_query)

        # Insert data
        for _, row in df.iterrows():
            insert_query = '''
            INSERT INTO products (title, price, rating, colors, size, gender, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, tuple(row))

        conn.commit()
        print("🗄️ Data berhasil disimpan ke PostgreSQL.")
    except Exception as e:
        print(f"❌ Gagal menyimpan ke PostgreSQL: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
