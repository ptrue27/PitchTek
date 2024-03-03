from app import sql_utils
import unittest

class TestSqlUtils(unittest.TestCase):
    def test_get_table_existing_table(self):
        # Test getting existing table
        result = sql_utils.get_table("TEAMS")
        self.assertEqual(len(result["id"]), 30)

    def test_get_table_nonexistent_table(self):
        # Test getting nonexistent table
        result = sql_utils.get_table("NONEXISTENT_TABLE")
        self.assertIsNone(result)

    def test_get_row_existing_row(self):
        # Test getting existing row
        result = sql_utils.get_row('BATTERS', 457759)
        self.assertEqual(result['name'], 'Justin Turner')

    def test_get_row_nonexistent_row(self):
        # Test getting nonexistent row
        result = sql_utils.get_row('BATTERS', 0)
        self.assertIsNone(result)
        
if __name__ == '__main__':
    unittest.main()