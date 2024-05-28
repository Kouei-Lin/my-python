import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
from web_driver_module import WebDriverManager
from apprise_module import Apprise

class SynType1:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.web_driver_manager = WebDriverManager()
        self.driver = self.web_driver_manager.get_driver()

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
        self.web_driver_manager.quit_driver()
        return data

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

def fetch_and_send_data(syn_instance):
    data = syn_instance.fetch_send_data()
    Apprise.ntfy(data)

load_dotenv()

def validate_env_variable(var_name):
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"Environment variable {var_name} is not set.")
    return value

syn_type1_targets = [
    {"url": validate_env_variable("SYN_TYPE1_URL1"), "username": validate_env_variable("SYN_TYPE1_USER1"), "password": validate_env_variable("SYN_TYPE1_PASS1")},
    {"url": validate_env_variable("SYN_TYPE1_URL2"), "username": validate_env_variable("SYN_TYPE1_USER2"), "password": validate_env_variable("SYN_TYPE1_PASS2")},
    {"url": validate_env_variable("SYN_TYPE1_URL3"), "username": validate_env_variable("SYN_TYPE1_USER3"), "password": validate_env_variable("SYN_TYPE1_PASS3")},
    {"url": validate_env_variable("SYN_TYPE1_URL4"), "username": validate_env_variable("SYN_TYPE1_USER4"), "password": validate_env_variable("SYN_TYPE1_PASS4")}
]

for user in syn_type1_targets:
    syn_type1 = SynType1(user["url"], user["username"], user["password"])
    fetch_and_send_data(syn_type1)

syn_type2_users = [
    {"url": validate_env_variable("SYN_TYPE2_URL1"), "username": validate_env_variable("SYN_TYPE2_USER1"), "password": validate_env_variable("SYN_TYPE2_PASS1")},
    {"url": validate_env_variable("SYN_TYPE2_URL2"), "username": validate_env_variable("SYN_TYPE2_USER2"), "password": validate_env_variable("SYN_TYPE2_PASS2")}
]

for user in syn_type2_users:
    syn_type2 = SynType2(user["url"], user["username"], user["password"])
    fetch_and_send_data(syn_type2)

syn_type3_users = [
    {"url": validate_env_variable("SYN_TYPE3_URL1"), "username": validate_env_variable("SYN_TYPE3_USER1"), "password": validate_env_variable("SYN_TYPE3_PASS1")},
    {"url": validate_env_variable("SYN_TYPE3_URL2"), "username": validate_env_variable("SYN_TYPE3_USER2"), "password": validate_env_variable("SYN_TYPE3_PASS2")}
]

for user in syn_type3_users:
    syn_type3 = SynType3(user["url"], user["username"], user["password"])
    fetch_and_send_data(syn_type3)

