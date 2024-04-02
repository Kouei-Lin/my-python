import webbrowser
import os
import cv2
import pytesseract
import pyautogui
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def detect_keyword(image_path, keyword):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply OCR on the grayscale image
    text = pytesseract.image_to_string(gray_image, lang='eng')

    # Check if the keyword is present in the OCR result
    if keyword in text:
        return True
    else:
        return False

# List of URLs you want to open
urls = ['https://www.google.com', 'https://en.wikipedia.org']

# Open each URL in the default browser
for url in urls:
    webbrowser.open(url)

# Wait for pages to load before taking screenshots
time.sleep(5)

# Take screenshots of the opened pages and check for keywords
for i, url in enumerate(urls):
    screenshot_path = f"screenshot_{i}.png"
    pyautogui.screenshot(screenshot_path)
    if detect_keyword(screenshot_path, "良好"):
        print(f"良好 status detected in screenshot for {url}")
    else:
        print(f"良好 status not detected in screenshot for {url}")
    os.remove(screenshot_path)  # Optionally, you may want to delete the screenshot file after checking it

