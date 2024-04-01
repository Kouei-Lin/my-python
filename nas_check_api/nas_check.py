import os
import cv2
import pytesseract
import glob
from dotenv import load_dotenv

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
    text = pytesseract.image_to_string(binary_roi, lang='chi_sim')
    
    # Check if the "良好" text is present in the OCR result
    if "良好" in text:
        return True
    else:
        return False

# Get the image directory from environment variable
image_dir = os.getenv("IMAGE_DIR")

# Get a list of all image paths matching the pattern
image_paths = glob.glob(image_dir)

# Iterate over each image and check for "良好" status
for image_path in image_paths:
    is_good_status = detect_good_status(image_path)
    print(f"良好 status detected in {image_path}: {is_good_status}")

