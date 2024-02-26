import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Get the API URL from the environment variables
API_URL = os.getenv('API_URL')

# Make a GET request to the API endpoint
response = requests.get(f'{API_URL}/api/disk-usage')

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Print the disk usage information returned by the API
    data = response.json()
    print("Total disk space:", data['total'])
    print("Used disk space:", data['used'])
    print("Free disk space:", data['free'])
else:
    # Print an error message if the request was not successful
    print("Error:", response.status_code)

