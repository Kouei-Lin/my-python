import os
import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

# Load environment variables from .env file
load_dotenv()

# Define API endpoints
api_endpoints = {
    'MAC': os.getenv('API_MAC'),
    'DISK': os.getenv('API_DISK'),
    'NAS': os.getenv('API_NAS'),
    'NAS_Browser': os.getenv('API_NAS_BROWSER')
}

# Define Google Sheets authentication
def authenticate_google_sheets(creds_path):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    return gspread.authorize(credentials)

# Fetch data from API and return as DataFrame
def fetch_data(api_url):
    response = requests.get(api_url)
    response.raise_for_status()  # Raise error for non-200 response
    return pd.DataFrame(response.json())

# Write DataFrame to Google Sheet
def write_to_google_sheet(dataframe, sheet_name, gc, spreadsheet_id):
    try:
        spreadsheet = gc.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet(sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        # If the sheet doesn't exist, create a new one
        worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=10)
    
    # Clear existing data
    worksheet.clear()

    # Update worksheet with data
    worksheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())

# Function to fetch and write data for a single API endpoint
def process_api(api_name, api_url, creds_path, spreadsheet_id):
    try:
        print(f"Fetching data from {api_name} API...")
        dataframe = fetch_data(api_url)
        
        # Authenticate with Google Sheets
        gc = authenticate_google_sheets(creds_path)

        # Write data to Google Sheet
        write_to_google_sheet(dataframe, api_name, gc, spreadsheet_id)

        print(f"Data from {api_name} API successfully saved to Google Sheet '{api_name}'.")
    except Exception as e:
        print(f"An error occurred while processing {api_name} API:", e)

# Authenticate with Google Sheets
creds_path = os.getenv('GOOGLE_AUTH_JSON_PATH')
spreadsheet_id = os.getenv('SPREADSHEET_ID')

# Create thread pool executor
with ThreadPoolExecutor(max_workers=10) as executor:
    # Submit tasks for each API endpoint
    futures = []
    for api_name, api_url in api_endpoints.items():
        futures.append(executor.submit(process_api, api_name, api_url, creds_path, spreadsheet_id))

    # Wait for all tasks to complete
    for future in futures:
        future.result()  # Ensure exceptions in threads are raised

