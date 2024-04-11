import os
import json
import requests

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Get the JSON file name
json_file = 'nas_data.json'

# Check if the JSON file exists
if os.path.exists(json_file):
    # Load data from the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Send data to the Flask API
    for item in data:
        response = requests.post('http://xxx.xxx.xxx.xxx/api/nas_browser', json=item)
        if response.status_code == 201:
            print(f"Data sent successfully for URL: {item['url']}")
        else:
            print(f"Failed to send data for URL: {item['url']}. Status code: {response.status_code}")
else:
    print(f"JSON file '{json_file}' not found.")

