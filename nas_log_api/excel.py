import requests
import pandas as pd
import openpyxl

# Define API endpoints and corresponding sheet names
api_endpoints = {
    'NAS': 'http://xxx.xxx.xxx.xxx:port/api/nas',
    'API2': 'http://xxx.xxx.xxx.xxx:port/api/api2',
    'API3': 'http://xxx.xxx.xxx.xxx:port/api/api3'
}

# Example path where the Excel file is located
excel_file_path = 'path/to/your/excel/file.xlsx'

# Function to fetch data from API and save to Excel sheet
def fetch_and_save_to_sheet(api_name, api_url, excel_file_path):
    try:
        # Make a GET request to the API endpoint
        response = requests.get(api_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()

            # Convert data to DataFrame
            df = pd.DataFrame(data)

            # Check if sheet exists in the Excel file
            with pd.ExcelWriter(excel_file_path, mode='a', if_sheet_exists="replace", engine='openpyxl') as writer:
                # Write DataFrame to Excel file, creating a new sheet
                df.to_excel(writer, sheet_name=api_name, index=False)
            
            print(f"Data from {api_name} API successfully saved to Excel sheet.")
        else:
            print(f"Failed to fetch data from {api_name} API.")
    except Exception as e:
        print(f"An error occurred while fetching data from {api_name} API:", e)

# Iterate through API endpoints and fetch data for each
for api_name, api_url in api_endpoints.items():
    fetch_and_save_to_sheet(api_name, api_url, excel_file_path)
