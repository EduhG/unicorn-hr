import unittest
from app import create_app

class AppTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_index_page(self):
        self.assertIn('Unicorn-HR', self.client.get('/').data)

if __name__ == '__main__':
    unittest.main()
