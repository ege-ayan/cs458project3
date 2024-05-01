from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import socket


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

class LoginPage(BasePage):
    email_field = None 
    password_field = None
    login_button = None

    def __init__(self, driver):
        super().__init__(driver)
        # Initialize email_field when the LoginPage object is created
        if LoginPage.email_field is None:
            LoginPage.email_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='email']")
            LoginPage.password_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            LoginPage.login_button = self.driver.find_element(By.CSS_SELECTOR, "button.login-button")


    def fill_form(self, email, password, expected_message):
                
                # If there is no internet connection, the expected alert should indicate
                # the internet connection problem before any problem else
                if self.is_internet_available() == False:
                    expected_message = "No internet connection available."
                
                email_field = LoginPage.email_field
                password_field = LoginPage.password_field

                email_field.click()
                email_field.send_keys(Keys.CONTROL + "a")
                email_field.send_keys(Keys.BACKSPACE)

                password_field.click()
                password_field.send_keys(Keys.CONTROL + "a")
                password_field.send_keys(Keys.BACKSPACE)

                if email != "": 
                    email_field.send_keys(email)
                if password != "":
                    password_field.send_keys(password)

                login_button = LoginPage.login_button
                login_button.click()

                try:
                    # Switch to the alert
                    alert = Alert(self.driver)
                    # Get the text of the alert
                    alert_text = alert.text
                    # Close the alert (accept or dismiss)
                    alert.accept()  # To accept the alert
                    # Or alert.dismiss()  # To dismiss the alert
                except NoAlertPresentException:
                    print("No alert present")
                    return False
                if alert_text == expected_message:
                    return True
                return False
   
    def is_correct_login_successful(self, email, password):
        expected_message = "Successfully logged in"
        return self.fill_form(email, password, expected_message)
    

    def is_invalid_login_successful(self, email, password):
        expected_message = "Invalid email or password"
        return self.fill_form(email, password, expected_message)

    
    def is_empty_login_successful(self, email, password):
        expected_message = "Email and password are required."
        return self.fill_form(email, password, expected_message)
    

    # Case 4 valid log in with Google
    def valid_google_login(self):
        expected_message = "Successfully logged in using Google Auth"
        google_email = "userexample49@gmail.com"
        google_password = "!Psw7818"
        return self.google_login(google_email, google_password, expected_message)

    # Case 5 invalid log in with Google
    def invalid_google_login(self):
        expected_message = "Error logging in with Google Auth"
        google_email = "userexample49@gmail.com"
        google_password = "invpsw" # Wrong password for the given user email
        return self.google_login_inv(google_email, google_password, expected_message)
    
    def google_login_inv(self, google_email, google_password, expected_message):
        time.sleep(1) # sleep to wait google login button to be visible
        google_sign_in_button = self.driver.find_element(By.CSS_SELECTOR, ".google-login-button")
        time.sleep(0.5)
        google_sign_in_button.click()

        new_window = self.driver.window_handles[-1]
        self.driver.switch_to.window(new_window)
        email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@type='email']")))
        
        email_input.send_keys(google_email)
        email_input.send_keys(Keys.ENTER)

        password_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@type='password']")))
        password_input.send_keys(google_password)
        time.sleep(2)
        password_input.send_keys(Keys.ENTER)
        error_message = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span[jsslot='']")))
        self.driver.switch_to.window(self.driver.window_handles[0])
        if error_message is not None:
            return True
        return False

    def google_login(self, google_email, google_password, expected_message):
        time.sleep(1) # sleep to wait google login button to be visible
        google_sign_in_button = self.driver.find_element(By.CSS_SELECTOR, ".google-login-button")
        time.sleep(0.5)
        google_sign_in_button.click()

        new_window = self.driver.window_handles[-1]
        self.driver.switch_to.window(new_window)
        email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@type='email']")))
        
        email_input.send_keys(google_email)
        email_input.send_keys(Keys.ENTER)

        password_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@type='password']")))
        password_input.send_keys(google_password)
        time.sleep(2)
        password_input.send_keys(Keys.ENTER)
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(6) # Wait for the alert to be present
        try:
            # Switch to the alert
            alert = Alert(self.driver)
            # Get the text of the alert
            alert_text = alert.text
            # Close the alert (accept or dismiss)
            alert.accept()  # To accept the alert
            # Or alert.dismiss()  # To dismiss the alert
        except NoAlertPresentException:
            print("No alert present")
            return False
        if alert_text == expected_message:
            return True
        return False

    # Case 1 detect the existence of the internet connection
    def is_internet_available(self):
        try:
            # Attempt to create a socket connection to Google's DNS server
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True  # Connection succeeded, internet is available
        except OSError:
            pass
        return False  # Connection failed, internet is not available