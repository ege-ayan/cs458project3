from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

class DistanceToSunPage(BasePage):
    lat_field = None
    long_field = None
    calculate_button = None
    gps_button = None
    output = None

    def __init__(self, driver):
        super().__init__(driver)

    def empty_credentials_test(self):
        expected_message = "Please enter both latitude and longitude."
        result = True
        DistanceToSunPage.lat_field = self.driver.find_element(By.CSS_SELECTOR, '.inputs input[type="text"][placeholder="Latitude"]')
        DistanceToSunPage.long_field = self.driver.find_element(By.CSS_SELECTOR, '.inputs input[type="text"][placeholder="Longitude"]')
        DistanceToSunPage.calculate_button = self.driver.find_element(By.CSS_SELECTOR, '.inputs button')

        lat_field = DistanceToSunPage.lat_field
        long_field = DistanceToSunPage.long_field
        calculate_button = DistanceToSunPage.calculate_button

        # Test with empty credentials for both field
        calculate_button.click()

        try:
            # Switch to the alert
            alert = Alert(self.driver)
            # Get the text of the alert
            alert_text = alert.text
            # Close the alert (accept or dismiss)
            alert.accept()  # To accept the alert
            # Or alert.dismiss()  # To dismiss the alert
        except NoAlertPresentException:
            result = False
            return result
        if alert_text != expected_message:
            result = False
            return result
        

        # Test with only latitude field empty
        long_field.click()
        long_field.send_keys("42.1313") # An example latitude
        lat_field.clear()
        calculate_button.click()

        try:
            alert = Alert(self.driver)
            alert_text = alert.text
            alert.accept()  # To accept the alert
        except NoAlertPresentException:
            result = False
            return result
        if alert_text != expected_message:
            result = False
            return result
        
        # Test with only longitude field empty
        lat_field.click()
        lat_field.send_keys("42.1313") # An example latitude
        long_field.send_keys(Keys.CONTROL + "a")
        long_field.send_keys(Keys.BACKSPACE)
        calculate_button.click()
        try:
            alert = Alert(self.driver)
            alert_text = alert.text
            alert.accept()  # To accept the alert
        except NoAlertPresentException:
            result = False
            return result
        if alert_text != expected_message:
            result = False
            return result
        return result
    
    def out_of_boundary_values_test(self):
        expected_message = "Failed to fetch data. Please check your inputs and try again."

        DistanceToSunPage.lat_field = self.driver.find_element(By.CSS_SELECTOR, '.inputs input[type="text"][placeholder="Latitude"]')
        DistanceToSunPage.long_field = self.driver.find_element(By.CSS_SELECTOR, '.inputs input[type="text"][placeholder="Longitude"]')
        DistanceToSunPage.calculate_button = self.driver.find_element(By.CSS_SELECTOR, '.inputs button')

        lat_field = DistanceToSunPage.lat_field
        long_field = DistanceToSunPage.long_field
        calculate_button = DistanceToSunPage.calculate_button

        lat_field.click()
        lat_field.send_keys("-90.0001")
        long_field.click()
        long_field.send_keys("180.0001")
        calculate_button.click()
        time.sleep(0.5) # wait for the alert to be present
        try:
            alert = Alert(self.driver)
            alert.accept()  # To accept the alert
        except NoAlertPresentException:
            print("No alert present")
            return False
        time.sleep(0.5) # wait for the alert to be present        
        try:
            alert = Alert(self.driver)
            alert_text = alert.text
            alert.accept()  # To accept the alert
        except NoAlertPresentException:
            print("No alert present")
            return False
        if alert_text != expected_message:
            return False
        return True

    def calculate_from_gps_button_test(self):
        DistanceToSunPage.gps_button = self.driver.find_element(By.CSS_SELECTOR, '.gps-button')
        gps_button = DistanceToSunPage.gps_button
        gps_button.click()
        time.sleep(0.5) # Wait for the result to be generated
        DistanceToSunPage.output =  self.driver.find_element(By.CSS_SELECTOR, '.result p')
        output_text = DistanceToSunPage.output.text
        pattern = r'\d+\.\d+'

        matches = re.findall(pattern, output_text)
        if matches:
            distance_to_sun = float(matches[0])
        else:
            print("No numerical value found")
            return False
        if distance_to_sun > 147000000: # The closest distance between earth and sun is 147.1 M km
            return True
        return False
