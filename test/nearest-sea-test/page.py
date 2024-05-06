from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import geocoder
import csv
from geopy.distance import geodesic
import os

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

class NearestSeaPage(BasePage):
    map_element = None
    distance_scraped = None
    sea_name_scraped = None

    def __init__(self, driver):
        super().__init__(driver)

    def get_user_location(self):
        # Get the user's current location using the geocoder module
        location = geocoder.ip('me')
        return location.latlng[0], location.latlng[1] # Latitude and longitude respectively

    def get_distance_to_seas(self, user_latitude, user_longitude):
        # Get the directory of the current script
        current_directory = os.path.dirname(__file__)

        # Construct the absolute path to the CSV file
        csv_file_path = os.path.join(current_directory, 'nearest_sea.csv')

        # Load sea data from CSV file
        seas = []
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                name, latitude, longitude = row
                seas.append({'name': name, 'latitude': float(latitude), 'longitude': float(longitude)})

        # Calculate distances to each sea
        min_distance = float('inf')
        nearest_sea = None
        for sea in seas:
            sea_latitude = sea['latitude']
            sea_longitude = sea['longitude']
            distance = geodesic((user_latitude, user_longitude), (sea_latitude, sea_longitude)).kilometers
            if distance < min_distance:
                min_distance = distance
                nearest_sea = sea['name']

        return nearest_sea, min_distance

    # CASE 1 - Does map appears in 10 seconds
    def does_map_exist(self):
        # Wait for up to 10 seconds for the element to become visible
        wait = WebDriverWait(self.driver, 10)
        NearestSeaPage.map_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".leaflet-container")))
        return self.map_element.is_displayed() if self.map_element else False
    
    # CASE 2 Is Nearest Sea name Correct
    def is_nearest_sea_name_correct(self):
        lat, long = self.get_user_location()
        nearest_sea, distance = self.get_distance_to_seas(lat, long)

        wait = WebDriverWait(self.driver, 10)

        scrape_info = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sea-name")))
        scrape_info_text = scrape_info.text
        parts = scrape_info_text.split('(')

        NearestSeaPage.sea_name_scraped = parts[0].strip()
        colon_index = NearestSeaPage.sea_name_scraped.find(':')  # Find the index of the colon

        # Eliminate other chars except the name of the sea
        if colon_index != -1: 
            NearestSeaPage.sea_name_scraped = NearestSeaPage.sea_name_scraped[colon_index+1:].strip() 

        if nearest_sea.strip().lower() != NearestSeaPage.sea_name_scraped.lower():
            return False
        return True
    
    # CASE 3 Is the nerest sea distance correct up to 10% precision
    def is_nearest_sea_distance_correct(self):
        lat, long = self.get_user_location()
        nearest_sea, distance = self.get_distance_to_seas(lat, long)

        wait = WebDriverWait(self.driver, 10)

        scrape_info = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sea-name")))
        scrape_info_text = scrape_info.text
        parts = scrape_info_text.split('(')

        distance_text = parts[1].split()[0]
        NearestSeaPage.distance_scraped = float(distance_text)

        if distance * 0.9 > NearestSeaPage.distance_scraped or distance * 1.1 < NearestSeaPage.distance_scraped:
            return False

        return True