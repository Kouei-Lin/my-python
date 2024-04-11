import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

class SynType2:
    def __init__(self):
        self.driver = webdriver.Firefox()

    def __del__(self):
        self.driver.quit()

    def fetch_data(self):
        # Load environment variables from .env file
        load_dotenv()

        # Define a list of tuples containing URL, username, and password
        websites = [
            (os.getenv('SYN_TYPE2_URL1'), os.getenv('SYN_TYPE2_USER1'), os.getenv('SYN_TYPE2_PASS1')),
            (os.getenv('SYN_TYPE2_URL2'), os.getenv('SYN_TYPE2_USER2'), os.getenv('SYN_TYPE2_PASS2')),
            # Add more URLs, usernames, and passwords as needed
        ]

        # Create a list to store results
        results = []

        # Loop through each website
        for website in websites:
            url, username, password = website

            # Print the URL for debugging purposes
            print("Navigating to URL:", url)
            
            # Navigate to the specified URL
            self.driver.get(url)
            
            # Wait for the username input field to be clickable
            username_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[syno-id="username"]')))
            # Input the username
            username_input.send_keys(username)
            
            # Click the advance button by class name (SVG element)
            advance_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[syno-id="account-panel-next-btn"]')))
            advance_button.click()
            
            # Find the password input field and input the password
            # Find the password input field using a combination of attributes
            # Wait for the username input field to be clickable
            password_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[syno-id="password"]')))
            # Input the password
            password_input.send_keys(password)
            
            # Click the login button by class name (SVG element)
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[syno-id="password-panel-next-btn"]')))
            login_button.click()
            
            # Wait for 30 seconds after logging in
            time.sleep(30)
            
            # Wait for the dashboard page to load
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'syno-sysinfo-system-health-content-header-normal')))
            
            # Find all div elements containing CPU and RAM information by class name
            cpu_ram_elements = self.driver.find_elements(By.CLASS_NAME, 'percentage-cmp-value')
            
            # Get the text of all elements containing CPU and RAM information
            cpu_values = cpu_ram_elements[0].text
            ram_values = cpu_ram_elements[1].text
            
            # Print CPU and RAM values
            print("CPU:", cpu_values)
            print("RAM:", ram_values)
            
            # Find the div element with class 'syno-sysinfo-system-health-content-header-normal' and extract its text
            status_div = self.driver.find_element(By.CLASS_NAME, 'syno-sysinfo-system-health-content-header-normal')
            status_text = status_div.text
            print("Status:", status_text)
            
            # Append the result to the list
            results.append({
                "url": url,
                "disk_status": status_text,
                "cpu": cpu_values,
                "ram": ram_values
            })

        return results

# Example usage:
syn_type2_instance = SynType2()
data = syn_type2_instance.fetch_data()

# Write results to a JSON file
with open('syn_type2_results.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Results have been saved to syn_type2_results.json")

