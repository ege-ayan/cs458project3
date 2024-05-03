import unittest
from selenium import webdriver
import page

class NearestSeaTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:3000/nearest-sea")

    def test_map_existence(self):
        nearest_sea_page = page.NearestSeaPage(self.driver)
        # Assert that the map element is displayed
        self.assertTrue(nearest_sea_page.does_map_exist())

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()