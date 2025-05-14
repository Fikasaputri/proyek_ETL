import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
import re

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

# Pola data kotor
dirty_patterns = {
    "Title": ["Unknown Product"],
    "Rating": ["Invalid Rating / 5", "Not Rated"],
    "Price": ["Price Unavailable", None]
}

# Fungsi untuk memeriksa apakah nilai field kotor
def is_dirty_field(field_name, value):
    return value in dirty_patterns.get(field_name, [])

# Fungsi fetch
def fetching_content(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error saat fetch URL: {url}, {e}")
        return None

# Fungsi ekstraksi
def extract_product_data(card):
    try:
        product_title_elem = card.find('h3', class_='product-title')
        price_elem = card.find('span', class_='price')
        rating_text = card.get_text()

        paragraphs = card.find_all('p')
        product_title = product_title_elem.text.strip() if product_title_elem else None
        price = price_elem.text.strip() if price_elem else None
        color = paragraphs[1].text.strip() if len(paragraphs) > 1 else ""
        size = paragraphs[2].text.strip() if len(paragraphs) > 2 else ""
        gender = paragraphs[3].text.strip() if len(paragraphs) > 3 else ""

        # Ambil rating pakai regex
        rating_match = re.search(r'(\d+(?:\.\d+)?)\s*/\s*5', rating_text)
        rating = rating_match.group(0) if rating_match else "Not Rated"

        # Cek data kotor
        if (
            is_dirty_field("Title", product_title) or
            is_dirty_field("Price", price) or
            is_dirty_field("Rating", rating)
        ):
            print(f"Dilewati karena data kotor: {product_title} | {price} | {rating}")
            return None

        return {
            'title': product_title,
            'price': price,
            'rating': rating,
            'colors': color,
            'size': size,
            'gender': gender,
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        print(f"Gagal ekstrak produk: {e}")
        return None

# Fungsi scraping utama
def scrape_product(base_url_template, first_page_url, start_page=1, delay=2, max_page=50):
    data = []
    page_number = start_page

    while page_number <= max_page:
        url = first_page_url if page_number == 1 else base_url_template.format(page_number)
        print(f"Scraping: {url}")
        content = fetching_content(url)
        if not content:
            break

        soup = BeautifulSoup(content, 'html.parser')
        main = soup.find('main', class_='container')
        if not main:
            break

        product_grid = main.find('div', class_='collection-grid')
        if not product_grid:
            break

        cards = product_grid.find_all('div', class_='collection-card')
        if not cards:
            break

        for card in cards:
            product = extract_product_data(card)
            if product:
                data.append(product)

        page_number += 1
        time.sleep(delay)

    return data
