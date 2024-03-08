import json
import requests

# Define the URL of your Flask API endpoint
API_URL = 'http://localhost:5000/api/mac'

# Path to your JSON file containing the data to be added
JSON_FILE = 'data.json'

# Function to read data from JSON file and send POST requests
def add_data_from_json():
    try:
        with open(JSON_FILE, 'r') as file:
            data = json.load(file)
            for entry in data:
                response = requests.post(API_URL, json=entry)
                if response.status_code == 201:
                    print(f"Data added successfully: {entry}")
                else:
                    print(f"Failed to add data: {entry}")
    except FileNotFoundError:
        print(f"File not found: {JSON_FILE}")

if __name__ == '__main__':
    add_data_from_json()

