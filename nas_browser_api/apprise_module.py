import os
import requests
from dotenv import load_dotenv

load_dotenv()

class Apprise:
    @staticmethod
    def ntfy(data):
        api_endpoint = os.getenv('API_ENDPOINT')
        if api_endpoint:
            response = requests.post(api_endpoint, json=data)
            if response.status_code == 201:
                print(f"Data sent successfully for URL: {data['url']}")
            else:
                print(f"Failed to send data for URL: {data['url']}. Status code: {response.status_code}")
        else:
            print("API_ENDPOINT not found in the environment variables.")

