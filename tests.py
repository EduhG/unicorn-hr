import unittest

from app import app

class AppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index_page(self):
        self.assertIn('Unicorn-HR', self.app.get('/').data)

if __name__ == '__main__':
    unittest.main()
