import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_table_existing_table(self):
        # Test the route with an existing table
        response = self.app.get('/get_table/TEAMS')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', data)

    def test_get_table_nonexistent_table(self):
        # Test the route with a nonexistent table
        response = self.app.get('/get_table/NONEXISTENT_TABLE')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)

    def test_get_row_existing_row(self):
        # Test the route with an existing row
        response = self.app.get('/get_row/TEAMS/112')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', data)

    def test_get_row_nonexistent_row(self):
        # Test the route with a nonexistent row
        response = self.app.get('/get_row/TEAMS/1')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
