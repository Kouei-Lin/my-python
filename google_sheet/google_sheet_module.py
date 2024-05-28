import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

class GoogleSheetManager:
    def __init__(self, creds_path):
        self.gc = self.authenticate_google_sheets(creds_path)

    # Authenticate with Google Sheets
    def authenticate_google_sheets(self, creds_path):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        return gspread.authorize(credentials)

    # Write DataFrame to Google Sheet
    def write_to_google_sheet(self, dataframe, sheet_name, spreadsheet_id):
        try:
            spreadsheet = self.gc.open_by_key(spreadsheet_id)
            worksheet = spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            # If the sheet doesn't exist, create a new one
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=len(dataframe.columns))

        # Clear existing data in the worksheet
        worksheet.clear()

        # Write new data to the worksheet
        worksheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())

    def update_google_sheet(self, spreadsheet_id, data_dict):
        # Write data to Google Sheet for each key-value pair in data_dict
        for sheet_name, data in data_dict.items():
            dataframe = pd.DataFrame(data)
            self.write_to_google_sheet(dataframe, sheet_name, spreadsheet_id)

