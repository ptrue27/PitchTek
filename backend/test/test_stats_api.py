from app import stats_api
import unittest

class TestStatsAPI(unittest.TestCase):
    def test_get_table_existing(self):
        # Test getting existing table with SQL
        result = stats_api.get_table("TEAMS")
        self.assertEqual(len(result["id"]), 30)

    def test_get_table_nonexistent(self):
        # Test getting nonexistent table with SQL
        result = stats_api.get_table("NONEXISTENT_TABLE")
        self.assertIsNone(result)

    def test_get_row_existing(self):
        # Test getting existing row with SQL
        result = stats_api.get_row('BATTERS', 457759)
        self.assertEqual(result['name'], 'Justin Turner')

    def test_get_row_nonexistent(self):
        # Test getting nonexistent row with SQL
        result = stats_api.get_row('BATTERS', 0)
        self.assertIsNone(result)

    def test_get_row_injection(self):
        # Test getting row with malicious input string
        result = stats_api.get_row('BATTERS', '457759 OR 1=1')
        self.assertIsNone(result)
        
if __name__ == '__main__':
    unittest.main()