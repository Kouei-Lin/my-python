import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from datetime import datetime

class SynType1:
    def __init__(self, driver):
        self.driver = driver

    def fetch_data(self, websites):
        results = []

        for website in websites:
            url, username, password = website

            print("Navigating to URL:", url)
            
            self.driver.get(url)
            
            wait = WebDriverWait(self.driver, 10)
            
            username_input = wait.until(EC.element_to_be_clickable((By.ID, 'login_username')))
            username_input.send_keys(username)
            
            password_input = wait.until(EC.element_to_be_clickable((By.ID, 'login_passwd')))
            password_input.send_keys(password)
            
            login_button = wait.until(EC.element_to_be_clickable((By.ID, 'login-btn')))
            login_button.click()
            
            time.sleep(30)
            
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'syno-sysinfo-system-health-content-header-normal')))
            
            cpu_ram_elements = self.driver.find_elements(By.CLASS_NAME, 'percentage-cmp-value')
            cpu_values = cpu_ram_elements[0].text
            ram_values = cpu_ram_elements[1].text
            
            status_div = self.driver.find_element(By.CLASS_NAME, 'syno-sysinfo-system-health-content-header-normal')
            status_text = status_div.text
            
            results.append({
                "url": url,
                "disk_status": status_text,
                "cpu": cpu_values,
                "ram": ram_values
            })

        return results

class SynType2:
    def __init__(self, driver):
        self.driver = driver

    def fetch_data(self, websites):
        results = []

        for website in websites:
            url, username, password = website

            print("Navigating to URL:", url)
            
            self.driver.get(url)
            
            username_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[syno-id="username"]')))
            username_input.send_keys(username)
            
            advance_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[syno-id="account-panel-next-btn"]')))
            advance_button.click()
            
            password_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[syno-id="password"]')))
            password_input.send_keys(password)
            
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[syno-id="password-panel-next-btn"]')))
            login_button.click()
            
            time.sleep(30)
            
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'syno-sysinfo-system-health-content-header-normal')))
            
            cpu_ram_elements = self.driver.find_elements(By.CLASS_NAME, 'percentage-cmp-value')
            cpu_values = cpu_ram_elements[0].text
            ram_values = cpu_ram_elements[1].text
            
            status_div = self.driver.find_element(By.CLASS_NAME, 'syno-sysinfo-system-health-content-header-normal')
            status_text = status_div.text
            
            results.append({
                "url": url,
                "disk_status": status_text,
                "cpu": cpu_values,
                "ram": ram_values
            })

        return results

# Load environment variables from .env file
load_dotenv()

# Get user data from .env file
user_data = {
    "syn_type1": [],
    "syn_type2": []
}

# Retrieve user data for SynType1
for i in range(1, 6):
    url_key = f"SYN_TYPE1_URL{i}"
    user_key = f"SYN_TYPE1_USER{i}"
    pass_key = f"SYN_TYPE1_PASS{i}"
    url = os.getenv(url_key)
    user = os.getenv(user_key)
    password = os.getenv(pass_key)
    if url and user and password:
        user_data["syn_type1"].append((url, user, password))

# Retrieve user data for SynType2
for i in range(1, 3):
    url_key = f"SYN_TYPE2_URL{i}"
    user_key = f"SYN_TYPE2_USER{i}"
    pass_key = f"SYN_TYPE2_PASS{i}"
    url = os.getenv(url_key)
    user = os.getenv(user_key)
    password = os.getenv(pass_key)
    if url and user and password:
        user_data["syn_type2"].append((url, user, password))

# Set up browser instance
driver = webdriver.Firefox()

# Fetch data for SynType1 users
syn_type1_instance = SynType1(driver)
all_results = []
for user in user_data["syn_type1"]:
    data = syn_type1_instance.fetch_data([user])
    all_results.extend(data)

# Fetch data for SynType2 users
syn_type2_instance = SynType2(driver)
for user in user_data["syn_type2"]:
    data = syn_type2_instance.fetch_data([user])
    all_results.extend(data)

# Get today's date in YYYY-MM-DD format
today_date = datetime.now().strftime("%Y-%m-%d")

# Construct the JSON file name with today's date
json_file = f'nas_data_{today_date}.json'

# Check if the JSON file exists
if os.path.exists(json_file):
    # If the file exists, load existing data
    with open(json_file, 'r') as f:
        existing_results = json.load(f)
else:
    # If the file doesn't exist, create an empty list
    existing_results = []

# Append new results to the existing data
existing_results.extend(all_results)

# Write combined results to the JSON file
with open(json_file, 'w') as f:
    json.dump(existing_results, f, indent=4)

# Close the browser
driver.quit()

print(f"Results have been appended to {json_file} and the browser has been closed.")

