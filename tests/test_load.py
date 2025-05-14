import unittest
import pandas as pd
import os
from unittest.mock import patch, MagicMock
from utils.load import save_to_csv, save_to_postgresql

class TestLoad(unittest.TestCase):
    def setUp(self):
        # Setup dummy DataFrame untuk pengujian
        self.df = pd.DataFrame({
            'title': ['Test Product'],
            'price': [160000],
            'rating': [4.5],
            'colors': [3],
            'size': ['M'],
            'gender': ['Unisex'],
            'timestamp': ['2025-05-14T10:00:00']
        })
        self.test_csv = 'test_output.csv'

    def tearDown(self):
        # Hapus file CSV setelah test
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)

    def test_save_to_csv(self):
        save_to_csv(self.df, self.test_csv)
        self.assertTrue(os.path.exists(self.test_csv))

        # Baca kembali dan bandingkan
        loaded_df = pd.read_csv(self.test_csv)
        self.assertEqual(len(loaded_df), 1)
        self.assertIn('title', loaded_df.columns)

    @patch('utils.load.psycopg2.connect')
    def test_save_to_postgresql(self, mock_connect):
        # Mock koneksi dan cursor PostgreSQL
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        db_params = {
            'host': 'localhost',
            'port': 5432,
            'dbname': 'test_db',
            'user': 'test_user',
            'password': 'test_pass'
        }

        try:
            save_to_postgresql(self.df, db_params)
            mock_connect.assert_called_once()
            mock_cursor.execute.assert_called()  # Pastikan query SQL dijalankan
            mock_conn.commit.assert_called_once()
        except Exception as e:
            self.fail(f"save_to_postgresql raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
