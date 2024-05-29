import os
from dotenv import load_dotenv
from flask_api_module import create_app
from apprise_module import NotificationManager
from datetime import datetime
from pytz import timezone
from flask import request

# Load environment variables from .env file
load_dotenv()

DATABASE = 'nas_data.db'
TABLE = 'nas_data'
SQL_CREATE_TABLE = f'''CREATE TABLE IF NOT EXISTS {TABLE} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        url TEXT NOT NULL,
                        disk_status TEXT NOT NULL,
                        cpu TEXT NOT NULL,
                        ram TEXT NOT NULL
                    )'''

HOST = '0.0.0.0'
PORT = 5003
DEBUG = True

# Initialize NotificationManager
notification_manager = NotificationManager()

# Create the Flask app with the notification manager's send_notification method
app, create_database = create_app(DATABASE, TABLE, notification_manager.send_notification)
create_database(SQL_CREATE_TABLE)

@app.before_request
def set_date_timezone():
    taipei_timezone = timezone('Asia/Taipei')
    current_time = datetime.now(taipei_timezone)
    request.current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

if _name_ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)

