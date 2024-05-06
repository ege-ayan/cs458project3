import unittest
from selenium import webdriver
import page

class DistanceToSun(unittest.TestCase):
    distance_to_sun_page = None
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:3000/distance-to-sun")
        self.distance_to_sun_page = page.DistanceToSunPage(self.driver)
    # CASE 1
    def test_empty_credentials(self):
        self.assertTrue(self.distance_to_sun_page.empty_credentials_test())
    
    # CASE 2
    def test_out_of_boundary_values(self):
        self.assertTrue(self.distance_to_sun_page.out_of_boundary_values_test())

    # CASE 3
    def test_calculate_from_gps_button(self):
        self.assertTrue(self.distance_to_sun_page.calculate_from_gps_button_test())
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    # Create a test suite
    suite = unittest.TestSuite()

    # Add tests to the suite in the following order
    suite.addTest(DistanceToSun('test_empty_credentials'))
    suite.addTest(DistanceToSun('test_out_of_boundary_values'))
    suite.addTest(DistanceToSun('test_calculate_from_gps_button'))
    # Run the tests
    unittest.TextTestRunner().run(suite)