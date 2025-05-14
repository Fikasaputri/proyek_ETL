import unittest
from unittest.mock import patch, Mock
from utils.extract import scrape_product

class TestExtract(unittest.TestCase):
    @patch('utils.extract.requests.get')
    def test_scrape_product(self, mock_get):
        # Setup mock response HTML sesuai struktur website fashion-studio.dicoding.dev
        html_content = '''
        <main class="container">
            <div class="collection-grid">
                <div class="collection-card">
                    <h3 class="product-title">Test Product</h3>
                    <span class="price">$10.00</span>
                    <p>Rating: 4.5 / 5</p>
                    <p>3 Colors</p>
                    <p>Size: M</p>
                    <p>Gender: Unisex</p>
                </div>
            </div>
        </main>
        '''
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = html_content
        mock_get.return_value = mock_response

        # URL sesuai dengan struktur aslinya (tapi tetap dummy karena pakai mock)
        base_url_template = 'https://fashion-studio.dicoding.dev/page/{}'
        first_page_url = 'https://fashion-studio.dicoding.dev/'

        result = scrape_product(base_url_template, first_page_url, max_page=1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Test Product')
        self.assertEqual(result[0]['price'], '$10.00')
        self.assertEqual(result[0]['rating'], '4.5 / 5')
        self.assertEqual(result[0]['colors'], '3 Colors')
        self.assertEqual(result[0]['size'], 'Size: M')
        self.assertEqual(result[0]['gender'], 'Gender: Unisex')
        self.assertIn('timestamp', result[0])

if __name__ == '__main__':
    unittest.main()
