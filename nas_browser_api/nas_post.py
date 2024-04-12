import os
import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv


class SynType1:
    def __init__(self, user):
        self.url = user["url"]
        self.username = user["username"]
        self.password = user["password"]
        self.driver = webdriver.Firefox()

    def test_connection(self):
        try:
            self.driver.get(self.url)
            return True
        except Exception as e:
            print(f"Failed to connect to {self.url}: {str(e)}")
            return False

    def login(self):
        print("Navigating to URL:", self.url)
        self.driver.get(self.url)

        wait = WebDriverWait(self.driver, 60)
        username_input = wait.until(EC.element_to_be_clickable((By.ID, 'login_username')))
        username_input.send_keys(self.username)

        password_input = wait.until(EC.element_to_be_clickable((By.ID, 'login_passwd')))
        password_input.send_keys(self.password)

        login_button = wait.until(EC.element_to_be_clickable((By.ID, 'login-btn')))
        login_button.click()

    def get_info(self):
        wait = WebDriverWait(self.driver, 60)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'syno-sysinfo-system-health-content-header-normal')))
        
        status_div = self.driver.find_element(By.CLASS_NAME, 'syno-sysinfo-system-health-content-header-normal')
        status_text = status_div.text
        
        return {"disk_status": status_text}

    def fetch_data(self):
        self.login()
        info = self.get_info()
        data = {"url": self.url, **info}

        # Notify API
        self.notify_api(data)

        # Quit driver
        self.quit_driver()

    def notify_api(self, data):
        api_endpoint = os.getenv('API_ENDPOINT')
        if api_endpoint:
            response = requests.post(api_endpoint, json=data)
            if response.status_code == 201:
                print(f"Data sent successfully for URL: {data['url']}")
            else:
                print(f"Failed to send data for URL: {data['url']}. Status code: {response.status_code}")
        else:
            print("API_ENDPOINT not found in the environment variables.")

    def quit_driver(self):
        self.driver.quit()


class SynType2(SynType1):
    def __init__(self, user):
        super().__init__(user)

    def login(self):
        print("Navigating to URL:", self.url)
        self.driver.get(self.url)

        wait = WebDriverWait(self.driver, 60)
        username_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[syno-id="username"]')))
        username_input.send_keys(self.username)

        advance_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[syno-id="account-panel-next-btn"]')))
        advance_button.click()

        password_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[syno-id="password"]')))
        password_input.send_keys(self.password)

        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[syno-id="password-panel-next-btn"]')))
        login_button.click()

    def get_info(self):
        wait = WebDriverWait(self.driver, 60)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'syno-sysinfo-system-health-content-header-normal')))
        
        status_div = self.driver.find_element(By.CLASS_NAME, 'syno-sysinfo-system-health-content-header-normal')
        status_text = status_div.text
        
        return {"disk_status": status_text}


# Load environment variables from .env file
load_dotenv()

# Test credentials for SynType1
syn_type1_users = [
    {"url": os.getenv("SYN_TYPE1_URL1"), "username": os.getenv("SYN_TYPE1_USER1"), "password": os.getenv("SYN_TYPE1_PASS1")},
    {"url": os.getenv("SYN_TYPE1_URL2"), "username": os.getenv("SYN_TYPE1_USER2"), "password": os.getenv("SYN_TYPE1_PASS2")},
    {"url": os.getenv("SYN_TYPE1_URL3"), "username": os.getenv("SYN_TYPE1_USER3"), "password": os.getenv("SYN_TYPE1_PASS3")},
    {"url": os.getenv("SYN_TYPE1_URL4"), "username": os.getenv("SYN_TYPE1_USER4"), "password": os.getenv("SYN_TYPE1_PASS4")},
    {"url": os.getenv("SYN_TYPE1_URL5"), "username": os.getenv("SYN_TYPE1_USER5"), "password": os.getenv("SYN_TYPE1_PASS5")}
]

# Test credentials for SynType2
syn_type2_users = [
    {"url": os.getenv("SYN_TYPE2_URL1"), "username": os.getenv("SYN_TYPE2_USER1"), "password": os.getenv("SYN_TYPE2_PASS1")},
    {"url": os.getenv("SYN_TYPE2_URL2"), "username": os.getenv("SYN_TYPE2_USER2"), "password": os.getenv("SYN_TYPE2_PASS2")}
]

# Create SynType1 instances and fetch data
for user in syn_type1_users:
    instance = SynType1(user)
    if instance.test_connection():
        instance.fetch_data()

# Create SynType2 instances and fetch data
for user in syn_type2_users:
    instance = SynType2(user)
    if instance.test_connection():
        instance.fetch_data()

