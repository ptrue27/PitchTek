from create_heatmap import make_heat_map
import unittest

# A test case class that inherits from unittest.TestCase
class Test_make_heat_map(unittest.TestCase):

    # Each test is a method that starts with "test_"
    def test_return_type(self):
        return_obj = make_heat_map("FF")
        self.assertIsInstance(return_obj, str)

    def test_jpg_extension(self):
        return_obj = make_heat_map("FF")
        self.assertTrue(return_obj.endswith(".jpg"))

if __name__ == '__main__':
    unittest.main()