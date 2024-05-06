import unittest
from selenium import webdriver
import page

class NearestSeaTest(unittest.TestCase):
    nearest_sea_page = None
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:3000/nearest-sea")
        self.nearest_sea_page = page.NearestSeaPage(self.driver)

    # CASE 1
    def test_map_existence(self):
        # Assert that the map element is displayed
        self.assertTrue(self.nearest_sea_page.does_map_exist())
    
    # CASE 2
    def test_name_of_nearest_sea(self):
        self.assertTrue(self.nearest_sea_page.is_nearest_sea_name_correct())

    # CASE 3
    def test_distance_to_nearest_sea(self):
        self.assertTrue(self.nearest_sea_page.is_nearest_sea_distance_correct())

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    # Create a test suite
    suite = unittest.TestSuite()

    # Add tests to the suite in the following order
    suite.addTest(NearestSeaTest('test_map_existence'))
    suite.addTest(NearestSeaTest('test_name_of_nearest_sea'))
    suite.addTest(NearestSeaTest('test_distance_to_nearest_sea'))

    # Run the tests
    unittest.TextTestRunner().run(suite)