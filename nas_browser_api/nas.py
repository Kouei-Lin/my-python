import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define a list of tuples containing URL, username, and password
websites = [
    (os.getenv('URL1'), os.getenv('USER1'), os.getenv('PASS1')),
    (os.getenv('URL2'), os.getenv('USER2'), os.getenv('PASS2')),
    (os.getenv('URL3'), os.getenv('USER3'), os.getenv('PASS3')),
    # Add more URLs, usernames, and passwords as needed
]

# Launch Firefox browser
driver = webdriver.Firefox()

# Create a list to store results
results = []

# Loop through each website
for website in websites:
    url, username, password = website

    # Print the URL for debugging purposes
    print("Navigating to URL:", url)
    
    # Navigate to the specified URL
    driver.get(url)
    
    # Wait for the login page to load
    wait = WebDriverWait(driver, 10)
    
    # Find the username input field and input the username
    username_input = wait.until(EC.element_to_be_clickable((By.ID, 'login_username')))
    username_input.send_keys(username)
    
    # Find the password input field and input the password
    password_input = wait.until(EC.element_to_be_clickable((By.ID, 'login_passwd')))
    password_input.send_keys(password)
    
    # Find the login button and click it
    login_button = wait.until(EC.element_to_be_clickable((By.ID, 'login-btn')))
    login_button.click()
    
    # Wait for the dashboard page to load
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'syno-sysinfo-system-health-content-header-normal')))
    
    # Find the div element with class 'syno-sysinfo-system-health-content-header-normal' and extract its text
    status_div = driver.find_element(By.CLASS_NAME, 'syno-sysinfo-system-health-content-header-normal')
    status_text = status_div.text
    print("Status:", status_text)
    
    # Find CPU and RAM elements
    cpu_element = driver.find_element(By.ID, 'ext-gen1153')
    ram_element = driver.find_element(By.ID, 'ext-gen1156')
    
    # Get CPU and RAM values
    cpu_text = cpu_element.text
    ram_text = ram_element.text
    
    # Print CPU and RAM values
    print("CPU:", cpu_text)
    print("RAM:", ram_text)
    
    # Append the result to the list
    results.append({
        "url": url,
        "disk_status": status_text,
        "cpu": cpu_text,
        "ram": ram_text
    })
    
    # Wait for 10 seconds (optional)
    time.sleep(10)

# Close the browser
driver.quit()

# Write results to a JSON file
with open('results.json', 'w') as f:
    json.dump(results, f, indent=4)

print("Results have been saved to results.json")

