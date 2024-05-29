import os
from dotenv import load_dotenv
from flask_api_module import create_app
from apprise_module import NotificationManager
from datetime import datetime
from pytz import timezone
from flask import request

# Load environment variables from .env file
load_dotenv()

DATABASE = 'disk_data.db'
TABLE = 'disks'
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
PORT = 5000
DEBUG = True

notification_manager = NotificationManager()
app, create_database = create_app(DATABASE, TABLE, notification_manager.send_notification)
create_database(SQL_CREATE_TABLE)

@app.before_request
def set_date_timezone():
    taipei_timezone = timezone('Asia/Taipei')
    current_time = datetime.now(taipei_timezone)
    request.current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

if _name_ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)

