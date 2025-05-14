import pandas as pd
import re

def clean_price(price_str):
    try:
        return int(float(price_str.replace("$", "").strip()) * 16000)
    except Exception as e:
        print(f"❌ Error konversi price: {price_str} → {e}")
        return None

def clean_rating(rating_str):
    try:
        # Ekstrak angka float pertama dalam string, contoh: "4.8 / 5"
        match = re.search(r"(\d+(\.\d+)?)", rating_str)
        if match:
            return float(match.group(1))
        return None
    except Exception as e:
        print(f"❌ Error konversi rating: {rating_str} → {e}")
        return None

def clean_colors(colors_str):
    try:
        return int(colors_str.strip().split()[0])
    except Exception as e:
        print(f"❌ Error konversi colors: {colors_str} → {e}")
        return None

def clean_size(size_str):
    return size_str.replace("Size: ", "").strip()

def clean_gender(gender_str):
    return gender_str.replace("Gender: ", "").strip()

def transform_data(raw_data):
    df = pd.DataFrame(raw_data)

    # Bersihkan setiap kolom
    df['price'] = df['price'].apply(clean_price)
    df['rating'] = df['rating'].apply(clean_rating)
    df['colors'] = df['colors'].apply(clean_colors)
    df['size'] = df['size'].apply(clean_size)
    df['gender'] = df['gender'].apply(clean_gender)

    # Hapus baris dengan judul "Unknown Product"
    df = df[df['title'] != "Unknown Product"]

    # Drop baris dengan nilai kosong di kolom penting
    df = df.dropna(subset=['price', 'rating', 'colors'])

    # Hapus duplikat
    df = df.drop_duplicates()

    print(f"✅ Data setelah transformasi: {len(df)} entri")
    return df
