import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Get the API URL from the environment variables
API_URL = os.getenv('API_URL')

# Accept user input for num1 and num2
num1 = int(input("Enter the first number (num1): "))
num2 = int(input("Enter the second number (num2): "))

# Define the JSON data to be sent in the request
data = {'num1': num1, 'num2': num2}

# Make a POST request to the Flask API endpoint
response = requests.post(f'{API_URL}/api/add', json=data)

# Print the response from the server
print(response.json())

