import os
import requests
import pandas as pd
from google_sheet_module import update_google_sheet

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Fetch data from API and return as DataFrame
def fetch_data(api_url):
    response = requests.get(api_url)
    response.raise_for_status()  # Raise error for non-200 response
    return pd.DataFrame(response.json())

if _name_ == "__main__":
    # Define API endpoints
    api_endpoints = {
        'MAC_API': os.getenv('API_MAC'),
        'DISK_API': os.getenv('API_DISK'),
        'NAS_Browser_API': os.getenv('API_NAS_BROWSER')
    }

    # Fetch data for each API endpoint and store in data_dict
    data_dict = {}
    for api_name, api_url in api_endpoints.items():
        print(f"Fetching data from {api_name} API...")
        data_dict[api_name] = fetch_data(api_url)
    
    # Update Google Sheet
    creds_path = os.getenv('GOOGLE_AUTH_JSON_PATH')
    spreadsheet_id = os.getenv('SPREADSHEET_ID')
    update_google_sheet(creds_path, spreadsheet_id, data_dict)

