# query_db.py

import os
import sqlite3
from datetime import date
from google_sheet_module import update_google_sheet

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Connect to SQLite database
def connect_to_database(database_path):
    return sqlite3.connect(database_path)

# Execute SQL query with parameters and return result as DataFrame
def execute_sql_query(connection, query, params=None):
    cursor = connection.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    return {columns[i]: [row[i] for row in data] for i in range(len(columns))}

# Function to fetch data from SQLite database for today's date
def fetch_data_from_database(database_path, query):
    connection = connect_to_database(database_path)
    today = date.today().strftime('%Y-%m-%d')
    data_dict = execute_sql_query(connection, query, (today,))
    connection.close()
    return data_dict

if _name_ == "__main__":
    # Define SQLite database paths and queries
    db_endpoints = {
        'MAC': (os.getenv('MAC_DB_PATH'), "SELECT date, name, internet FROM devices WHERE date(date) = ?"),
        'DISK': (os.getenv('DISK_DB_PATH'), "SELECT date, ip, device_id, free_space FROM disks WHERE date(date) = ?"),
        'NAS': (os.getenv('NAS_BROWSER_DB_PATH'), "SELECT date, url, disk_status FROM nas_data WHERE date(date) = ?")
    }

    # Fetch data for each database endpoint and store in data_dict
    data_dict = {}
    for api_name, (database_path, query) in db_endpoints.items():
        print(f"Fetching data from {api_name} database for today's date...")
        data_dict[api_name] = fetch_data_from_database(database_path, query)

    # Update Google Sheet
    creds_path = os.getenv('GOOGLE_AUTH_JSON_PATH')
    spreadsheet_id = os.getenv('SPREADSHEET_ID')
    update_google_sheet(creds_path, spreadsheet_id, data_dict)

