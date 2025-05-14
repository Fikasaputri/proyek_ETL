import unittest
import pandas as pd
from utils.transform import (
    clean_price, clean_rating, clean_colors,
    clean_size, clean_gender, transform_data
)

class TestTransform(unittest.TestCase):

    def test_clean_price(self):
        self.assertEqual(clean_price("$10.00"), 160000)
        self.assertEqual(clean_price("$0"), 0)
        self.assertIsNone(clean_price("invalid"))

    def test_clean_rating(self):
        self.assertEqual(clean_rating("4.5 / 5"), 4.5)
        self.assertEqual(clean_rating("5"), 5.0)
        self.assertIsNone(clean_rating("no rating"))

    def test_clean_colors(self):
        self.assertEqual(clean_colors("3 Colors"), 3)
        self.assertIsNone(clean_colors("Colors Unavailable"))

    def test_clean_size(self):
        self.assertEqual(clean_size("Size: L"), "L")
        self.assertEqual(clean_size("Size: XL"), "XL")

    def test_clean_gender(self):
        self.assertEqual(clean_gender("Gender: Female"), "Female")
        self.assertEqual(clean_gender("Gender: Male"), "Male")

    def test_transform_data(self):
        raw_data = [
            {
                "title": "Cool Shirt",
                "price": "$25.00",
                "rating": "4.8 / 5",
                "colors": "3 Colors",
                "size": "Size: M",
                "gender": "Gender: Male",
                "timestamp": "2024-05-14T12:00:00"
            },
            {
                "title": "Unknown Product",
                "price": "$20.00",
                "rating": "4.0 / 5",
                "colors": "2 Colors",
                "size": "Size: S",
                "gender": "Gender: Female",
                "timestamp": "2024-05-14T12:00:00"
            },
            {
                "title": "Invalid Price",
                "price": "not valid",
                "rating": "4.0 / 5",
                "colors": "2 Colors",
                "size": "Size: S",
                "gender": "Gender: Female",
                "timestamp": "2024-05-14T12:00:00"
            }
        ]
        df = transform_data(raw_data)

        # Hanya satu baris valid yang harus lolos
        self.assertEqual(len(df), 1)

        row = df.iloc[0]
        self.assertEqual(row['title'], 'Cool Shirt')
        self.assertEqual(row['price'], 400000)
        self.assertEqual(row['rating'], 4.8)
        self.assertEqual(row['colors'], 3)
        self.assertEqual(row['size'], 'M')
        self.assertEqual(row['gender'], 'Male')

if __name__ == '__main__':
    unittest.main()
