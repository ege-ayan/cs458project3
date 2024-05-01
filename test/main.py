import unittest
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium import webdriver
import page
import time

class LoginTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:3000")

    def test_all(self):
        
        self.correct_credentials()
        self.invalid_credentials()
        self.empty_credentials()
        
        login_page = page.LoginPage(self.driver)
        self.assertTrue(login_page.invalid_google_login())
        self.assertTrue(login_page.valid_google_login())


    # Case 3 login with valid credentials
    def correct_credentials(self):
       user_credentials = {
          'user1@example.com': 'password1',
          'user2@example.com': 'password2',
          'user3@example.com': 'password3',
          'user4@example.com': 'password4',
          'user5@example.com': 'password5'
        } 
       credentials_list = list(user_credentials.items())

       for i in range(len(user_credentials)):
        email, password = credentials_list[i]
        login_page = page.LoginPage(self.driver)
        self.assertTrue(login_page.is_correct_login_successful(email, password))
    

    # Case 2.2 login with invalid credentials
    def invalid_credentials(self):
        # Test with correct e-mail and wrong password (other users password)
        wrong_password = {
            'user1@example.com': 'password5',
            'user2@example.com': 'password1',
            'user3@example.com': 'password2',
            'user4@example.com': 'password3',
            'user5@example.com': 'password4'
        }  
        credentials_list = list(wrong_password.items())


        for i in range(len(wrong_password)):
            email, password = credentials_list[i]
            login_page = page.LoginPage(self.driver)
            self.assertTrue(login_page.is_invalid_login_successful(email, password))

        # Test with wrong e-mail address and passwords
        wrong_credentials = {
            'inv1@example.com': 'inv1',
            'inv2@example.com': 'inv2',
            'inv3@example.com': 'inv3',
            'inv4@example.com': 'inv4',
            'inv5@example.com': 'inv5'
        }

        credentials_list = list(wrong_credentials.items())
        
        for i in range(len(wrong_credentials)):
            email, password = credentials_list[i]
            login_page = page.LoginPage(self.driver)
            self.assertTrue(login_page.is_invalid_login_successful(email, password))

    # Case 2.1 login with empty credentials
    def empty_credentials(self):
        email_empty = ""
        email = "user1@example.com"
        password_empty = ""
        password = "password1"

        login_page = page.LoginPage(self.driver)

        # Test wth cases which email OR password are empty
        self.assertTrue(login_page.is_empty_login_successful(email_empty, password_empty))
        self.assertTrue(login_page.is_empty_login_successful(email_empty, password))
        self.assertTrue(login_page.is_empty_login_successful(email, password_empty))



    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()