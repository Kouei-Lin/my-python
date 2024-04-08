import requests
import pandas as pd
import openpyxl

# Make a GET request to the Flask API endpoint
api_url = 'http://xxx.xxx.xxx.xxx:port/api/nas'  # Replace with your actual API endpoint
response = requests.get(api_url)

# Check if the request was successful
if response.status_code == 200:
    # Parse JSON response
    data = response.json()

    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Example path where the Excel file is located
    excel_file_path = 'path/to/your/excel/file.xlsx'  # Update this with your actual file path
    
    # Check if sheet exists in the Excel file
    try:
        with pd.ExcelFile(excel_file_path) as xls:
            if 'NAS' in xls.sheet_names:
                # Open the Excel file
                wb = openpyxl.load_workbook(excel_file_path)
                # Delete the existing sheet
                wb.remove(wb['NAS'])
                # Save the changes
                wb.save(excel_file_path)
    except FileNotFoundError:
        pass  # Continue if the file doesn't exist or other errors occur
    
    # Write DataFrame to Excel file, creating a new sheet
    with pd.ExcelWriter(excel_file_path, mode='a', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='NAS', index=False)
        
    print("Data successfully overwritten in Excel file:", excel_file_path)
else:
    print("Failed to fetch data from the API.")

