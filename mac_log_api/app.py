import os
from dotenv import load_dotenv
from flask_api_module import FlaskAPIModule
from apprise_module import NotificationManager
from datetime import datetime
from pytz import timezone
from flask import request

# Load environment variables from .env file
load_dotenv()

DATABASE = 'network_data.db'
TABLE = 'devices'
SQL_CREATE_TABLE = f'''CREATE TABLE IF NOT EXISTS {TABLE} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        name TEXT NOT NULL,
                        mac_address TEXT NOT NULL,
                        appear_before TEXT NOT NULL,
                        interface TEXT NOT NULL,
                        internet TEXT NOT NULL
                    )'''
HOST = '0.0.0.0'
PORT = 5000
DEBUG = True

class CustomFlaskApp(FlaskAPIModule, NotificationManager):
    def __init__(self, database, table):
        FlaskAPIModule.__init__(self, database, table, self.send_notification)
        NotificationManager.__init__(self)
        self.app.before_request(self.set_date_timezone)
    
    def set_date_timezone(self):
        taipei_timezone = timezone('Asia/Taipei')
        current_time = datetime.now(taipei_timezone)
        request.current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

# Create an instance of CustomFlaskApp
custom_flask_app = CustomFlaskApp(DATABASE, TABLE)
app = custom_flask_app.app
custom_flask_app.create_database(SQL_CREATE_TABLE)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)

