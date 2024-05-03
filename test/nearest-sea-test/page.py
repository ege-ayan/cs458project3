from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

class NearestSeaPage(BasePage):
    map_element = None

    def __init__(self, driver):
        super().__init__(driver)
           
    def does_map_exist(self):
        # Wait for up to 10 seconds for the element to become visible
        wait = WebDriverWait(self.driver, 10)
        NearestSeaPage.map_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".leaflet-container")))
        return self.map_element.is_displayed() if self.map_element else False