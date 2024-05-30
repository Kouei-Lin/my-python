import os
from dotenv import load_dotenv
from flask_api_module import FlaskAPIModule  # Make sure to import the correct class
from apprise_module import NotificationManager
from datetime import datetime
from pytz import timezone
from flask import request

# Load environment variables from .env file
load_dotenv()

DATABASE = os.getenv('DATABASE', 'disk_data.db')
TABLE = os.getenv('TABLE', 'disks')
SQL_CREATE_TABLE = f'''CREATE TABLE IF NOT EXISTS {TABLE} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        device_id TEXT NOT NULL,
                        volume_name TEXT NOT NULL,
                        size INTEGER NOT NULL,
                        free_space INTEGER NOT NULL,
                        used_space INTEGER NOT NULL,
                        ip TEXT NOT NULL
                    )'''
HOST = '0.0.0.0'
PORT = 5001
DEBUG = True

# Initialize NotificationManager
notification_manager = NotificationManager()

class CustomFlaskApp(FlaskAPIModule):
    def __init__(self, database, table, send_notification):
        super().__init__(database, table, send_notification)
        self.app.before_request(self.set_date_timezone)
    
    def set_date_timezone(self):
        taipei_timezone = timezone('Asia/Taipei')
        current_time = datetime.now(taipei_timezone)
        request.current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

# Create an instance of CustomFlaskApp
custom_flask_app = CustomFlaskApp(DATABASE, TABLE, notification_manager.send_notification)
app = custom_flask_app.app
custom_flask_app.create_database(SQL_CREATE_TABLE)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)

