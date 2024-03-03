import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_teams(self):
        # Test the route to get team list
        response = self.app.get('/get_teams')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', data)

    def test_get_roster_existing(self):
        # Test the route to get roster list for existing roster
        response = self.app.get('/get_roster/108')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('batters', data)
        self.assertIn('pitchers', data)

    def test_get_roster_nonexisting(self):
        # Test the route to get roster list for nonexisting roster
        response = self.app.get('/get_roster/0')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)

    def test_get_batter_existing(self):
        # Test the route to get batter stats for existing player
        response = self.app.get('/get_batter/457759')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], "Justin Turner")

    def test_get_batter_nonexisting(self):
        # Test the route to get batters stats for nonexisting player
        response = self.app.get('/get_batter/0')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)

    def test_get_pitcher_existing(self):
        # Test the route to get pitcher stats for existing player
        response = self.app.get('/get_pitcher/425844')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], "Zack Greinke")

    def test_get_pitcher_nonexisting(self):
        # Test the route to get pitcher stats for nonexisting player
        response = self.app.get('/get_pitcher/0')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
