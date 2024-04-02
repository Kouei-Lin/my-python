import webbrowser
import os
import cv2
import pytesseract
import glob
import pyautogui
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

def detect_good_status(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Define the region of interest (ROI) based on provided coordinates
    roi = image[550:780, 1500:1850]  # Defined by Y, X coordinates

    # Convert the ROI to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to obtain binary image
    _, binary_roi = cv2.threshold(gray_roi, 200, 255, cv2.THRESH_BINARY)

    # Perform OCR on the ROI
    text = pytesseract.image_to_string(binary_roi, lang='chi_tra')

    # Check if the "良好" text is present in the OCR result
    if "良好" in text:
        return True
    else:
        return False

# Get the image directory from environment variable
image_dir = os.getenv("IMAGE_DIR")

# List of URLs you want to open
urls = ['https://www.google.com', 'https://en.wikipedia.org']

# Open each URL in the default browser
for url in urls:
    webbrowser.open(url)
    time.sleep(3)  # Adding a delay to allow the page to fully load before taking a screenshot
    # Take a screenshot and save it
    screenshot_path = f"screenshot_{urls.index(url)}.png"
    pyautogui.screenshot(screenshot_path)
    # Check if the screenshot has the desired status
    is_good_status = detect_good_status(screenshot_path)
    print(f"良好 status detected in screenshot for {url}: {is_good_status}")
    # Optionally, you may want to delete the screenshot file after checking it
    os.remove(screenshot_path)

