import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

class SynType1:
    def __init__(self):
        self.driver = webdriver.Firefox()

    def __del__(self):
        self.driver.quit()

    def fetch_data(self):
        # Load environment variables from .env file
        load_dotenv()

        # Define a list of tuples containing URL, username, and password
        websites = [
            (os.getenv('SYN_TYPE1_URL1'), os.getenv('SYN_TYPE1_USER1'), os.getenv('SYN_TYPE1_PASS1')),
            (os.getenv('SYN_TYPE1_URL2'), os.getenv('SYN_TYPE1_USER2'), os.getenv('SYN_TYPE1_PASS2')),
            (os.getenv('SYN_TYPE1_URL3'), os.getenv('SYN_TYPE1_USER3'), os.getenv('SYN_TYPE1_PASS3')),
            (os.getenv('SYN_TYPE1_URL4'), os.getenv('SYN_TYPE1_USER4'), os.getenv('SYN_TYPE1_PASS4')),
            (os.getenv('SYN_TYPE1_URL5'), os.getenv('SYN_TYPE1_USER5'), os.getenv('SYN_TYPE1_PASS5')),
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

            # Wait for the login page to load
            wait = WebDriverWait(self.driver, 10)

            # Find the username input field and input the username
            username_input = wait.until(EC.element_to_be_clickable((By.ID, 'login_username')))
            username_input.send_keys(username)

            # Find the password input field and input the password
            password_input = wait.until(EC.element_to_be_clickable((By.ID, 'login_passwd')))
            password_input.send_keys(password)

            # Find the login button and click it
            login_button = wait.until(EC.element_to_be_clickable((By.ID, 'login-btn')))
            login_button.click()

            # Wait for 30 seconds after logging in
            time.sleep(30)

            # Wait for the dashboard page to load
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
syn_type1_instance = SynType1()
data = syn_type1_instance.fetch_data()

# Write results to a JSON file
with open('syn_type1_results.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Results have been saved to syn_type1_results.json")
