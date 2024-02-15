
'''
table = sql_utils.get_table('TEAMS')
print(table, '\n')

row = sql_utils.get_row('ROSTERS', 457759)
print(row)

row = sql_utils.get_row('PITCHERS', 1)
row['img'] = 'PLACEHOLDER'
print(row)

row = sql_utils.get_row('BATTERS', 1)
row['img'] = 'PLACEHOLDER'
print(row)
'''
import sql_utils
import unittest

class TestSqlUtils(unittest.TestCase):
    def test_get_table_existing_table(self):
        # Test the function with an existing table
        result = sql_utils.get_table('TEAMS')
        self.assertEqual(len(result), 2)

    def test_get_table_nonexistent_table(self):
        # Test the function with a nonexistent table
        result = sql_utils.get_table('NONEXISTENT_TABLE')
        self.assertIsNone(result)

    def test_get_row_existing_row(self):
        # Test the function with an existing row
        result = sql_utils.get_row('ROSTERS', 457759)
        self.assertEqual(result['name'], 'Justin Turner')

    def test_get_row_nonexistent_row(self):
        # Test the function with a nonexistent row
        result = sql_utils.get_row('ROSTERS', 1)
        self.assertIsNone(result)
        
if __name__ == '__main__':
    unittest.main()