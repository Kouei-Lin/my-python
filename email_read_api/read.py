import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

class WebMail:
    def __init__(self, user):
        self.url = user["url"]
        self.username = user["username"]
        self.password = user["password"]
        self.driver = webdriver.Firefox()

    def login(self):
        print("Navigating to URL:", self.url)
        self.driver.get(self.url)

        wait = WebDriverWait(self.driver, 60)
        username_input = wait.until(EC.element_to_be_clickable((By.ID, 'rcmloginuser')))
        username_input.send_keys(self.username)

        password_input = wait.until(EC.element_to_be_clickable((By.ID, 'rcmloginpwd')))
        password_input.send_keys(self.password)

        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.button.mainaction')))
        login_button.click()

    def quit_driver(self):
        self.driver.quit()

    def fetch_data(self):
        self.login()

        data = []

        next_page_clicks = 0  # Counter for the number of times the next page button is clicked

        while next_page_clicks < 50:
            # Wait for the replication folder to load
            wait = WebDriverWait(self.driver, 60)
            replication_folder_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Replication")]')))
            replication_folder_link.click()

            # Wait for the folder to load
            wait.until(EC.presence_of_element_located((By.XPATH, '//td[@class="date"]')))

            # Extract all dates, sizes, and subjects
            date_elements = self.driver.find_elements(By.XPATH, '//td[@class="date"]')
            size_elements = self.driver.find_elements(By.XPATH, '//td[@class="size"]')
            subject_links = self.driver.find_elements(By.XPATH, '//td[@class="subject"]/a')

            for date_element, size_element, subject_link in zip(date_elements, size_elements, subject_links):
                date = date_element.text
                size = size_element.text
                subject = subject_link.text

                # Check if the subject contains MAWF or SECOM
                if "MAWF" in subject:
                    subject = "MAWF"
                elif "SECOM" in subject:
                    subject = "SECOM"

                data.append((subject, date, size))

            # Check if there's a next page
            next_page_button = self.driver.find_element(By.ID, 'rcmbtn112')
            if "disabled" in next_page_button.get_attribute("class"):
                break  # No more pages to scrape

            # Click next page button
            next_page_button.click()

            next_page_clicks += 1  # Increment the counter

        # Quit the driver
        self.quit_driver()

        return data

# Load environment variables from .env file
load_dotenv()

# Test user for WebMail
webmail_user = {
    "url": os.getenv("WEBMAIL_URL1"),
    "username": os.getenv("WEBMAIL_USER1"),
    "password": os.getenv("WEBMAIL_PASS1")
}

# Create WebMail instance and fetch data
webmail_instance = WebMail(webmail_user)
data = webmail_instance.fetch_data()

# Save data to CSV file
csv_file = "data.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Subject", "Date", "Size"])
    writer.writerows(data)

print(f"Data saved to {csv_file}.")

