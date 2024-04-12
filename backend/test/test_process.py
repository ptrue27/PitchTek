import unittest
import pandas as pd
from experiments.process_csv import determine_data_type


class TestProcessCSV(unittest.TestCase):
    def test_determine_data_type_numeric(self):
        series = pd.Series([1, 2, 3])
        self.assertEqual(determine_data_type(series), 'numeric')

    def test_determine_data_type_string(self):
        series = pd.Series(['a', 'b', 'c'])
        self.assertEqual(determine_data_type(series), 'string')

    def test_determine_data_type_datetime(self):
        series = pd.Series(pd.date_range('20230101', periods=3))
        self.assertEqual(determine_data_type(series), 'datetime')


if __name__ == '__main__':
    unittest.main()
