import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
from dotenv import load_dotenv
from selenium.webdriver.firefox.options import Options

class SynType1:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        ff_options = Options()
        ff_options.add_argument("--headless")
        grid_url = "http://127.0.0.1:4444/wd/hub"
        self.driver = webdriver.Remote(
            command_executor=grid_url,
            options=ff_options
        )

    def login(self):
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
        try:
            status_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'syno-sysinfo-system-health-content-header-normal')))
        except TimeoutException:
            try:
                status_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'syno-sysinfo-system-health-content-header-warning')))
            except TimeoutException:
                print("No status found")
                return {"disk_status": "No status found"}
        status_text = status_div.text
        return {"disk_status": "Attention"} if "Attention" in status_text else {"disk_status": status_text}

    def fetch_send_data(self):
        self.login()
        info = self.get_info()
        data = {"url": self.url, **info}
        self.quit_driver()
        return data

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
    def __init__(self, url, username, password):
        super().__init__(url, username, password)

    def login(self):
        self.driver.get(self.url)
        wait = WebDriverWait(self.driver, 120)
        username_input = wait.until(EC.element_to_be_clickable((By.ID, 'login_username')))
        username_input.send_keys(self.username)
        password_input = wait.until(EC.element_to_be_clickable((By.ID, 'login_passwd')))
        password_input.send_keys(self.password)
        login_button = wait.until(EC.element_to_be_clickable((By.ID, 'login-btn')))
        login_button.click()

    def get_info(self):
        wait = WebDriverWait(self.driver, 120)
        try:
            status_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'syno-sysinfo-system-health-content-header-normal')))
        except TimeoutException:
            try:
                status_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'syno-sysinfo-system-health-content-header-warning')))
            except TimeoutException:
                print("No status found")
                return {"disk_status": "No status found"}
        status_text = status_div.text
        return {"disk_status": "Attention"} if "Attention" in status_text else {"disk_status": status_text}

class SynType3(SynType1):
    def __init__(self, url, username, password):
        super().__init__(url, username, password)

    def login(self):
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
        wait = WebDriverWait(self.driver, 30)
        try:
            status_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'syno-sysinfo-system-health-content-header-normal')))
        except TimeoutException:
            try:
                status_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'syno-sysinfo-system-health-content-header-warning')))
            except TimeoutException:
                print("No status found")
                return {"disk_status": "No status found"}
        status_text = status_div.text
        return {"disk_status": "Attention"} if "Attention" in status_text else {"disk_status": status_text}

def fetch_and_send_data(syn_instance):
    data = syn_instance.fetch_send_data()
    syn_instance.notify_api(data)

load_dotenv()

syn_type1_targets = [
    {"url": os.getenv("SYN_TYPE1_URL1"), "username": os.getenv("SYN_TYPE1_USER1"), "password": os.getenv("SYN_TYPE1_PASS1")},
    {"url": os.getenv("SYN_TYPE1_URL2"), "username": os.getenv("SYN_TYPE1_USER2"), "password": os.getenv("SYN_TYPE1_PASS2")},
    {"url": os.getenv("SYN_TYPE1_URL3"), "username": os.getenv("SYN_TYPE1_USER3"), "password": os.getenv("SYN_TYPE1_PASS3")},
    {"url": os.getenv("SYN_TYPE1_URL4"), "username": os.getenv("SYN_TYPE1_USER4"), "password": os.getenv("SYN_TYPE1_PASS4")}
]

for user in syn_type1_targets:
    syn_type1 = SynType1(user["url"], user["username"], user["password"])
    fetch_and_send_data(syn_type1)

syn_type2_users = [
    {"url": os.getenv("SYN_TYPE2_URL1"), "username": os.getenv("SYN_TYPE2_USER1"), "password": os.getenv("SYN_TYPE2_PASS1")},
    {"url": os.getenv("SYN_TYPE2_URL2"), "username": os.getenv("SYN_TYPE2_USER2"), "password": os.getenv("SYN_TYPE2_PASS2")}
]

for user in syn_type2_users:
    syn_type2 = SynType2(user["url"], user["username"], user["password"])
    fetch_and_send_data(syn_type2)

syn_type3_users = [
    {"url": os.getenv("SYN_TYPE3_URL1"), "username": os.getenv("SYN_TYPE3_USER1"), "password": os.getenv("SYN_TYPE3_PASS1")},
    {"url": os.getenv("SYN_TYPE3_URL2"), "username": os.getenv("SYN_TYPE3_USER2"), "password": os.getenv("SYN_TYPE3_PASS2")}
]

for user in syn_type3_users:
    syn_type3 = SynType3(user["url"], user["username"], user["password"])
    fetch_and_send_data(syn_type3)

