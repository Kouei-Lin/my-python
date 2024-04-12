import os
import json
import time
from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from apprise import Apprise
from pytz import timezone

app = Flask(__name__)
DATABASE = 'nas_data.db'

# Load environment variables from .env file
load_dotenv()

# Function to create SQLite database if not exists
def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS nas_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        url TEXT NOT NULL,
                        disk_status TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

# Create a new NAS data entry
@app.route('/api/nas_browser', methods=['POST'])
def add_nas_data():
    new_data = request.json

    # Convert current datetime to Taipei timezone (UTC+8)
    taipei_timezone = timezone('Asia/Taipei')
    date_taipei = datetime.now(taipei_timezone)
    new_data['date'] = date_taipei.strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO nas_data (date, url, disk_status)
                      VALUES (?, ?, ?)''', (new_data['date'], new_data['url'], new_data['disk_status']))
    conn.commit()
    conn.close()

    # Send detailed notification
    logged_data = f"Logged data:\nDate: {new_data['date']}\nURL: {new_data['url']}\nDisk Status: {new_data['disk_status']}"
    send_notification(logged_data)

    return jsonify({"message": "NAS data added successfully"}), 201

# Get all NAS data with date, url, and disk status columns
@app.route('/api/nas_browser', methods=['GET'])
def get_nas_data():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT date, url, disk_status FROM nas_data")
    data = cursor.fetchall()
    conn.close()

    # Combine column names with data values into dictionaries
    data_with_keys = [{"date": row[0], "url": row[1], "disk_status": row[2]} for row in data]

    return jsonify(data_with_keys)

# Get a single NAS data entry by ID with date, url, and disk status columns
@app.route('/api/nas_browser/<int:id>', methods=['GET'])
def get_nas_data_by_id(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT date, url, disk_status FROM nas_data WHERE id=?", (id,))
    data = cursor.fetchone()
    conn.close()

    if data:
        # Combine column names with data values into a dictionary
        data_with_keys = {"date": data[0], "url": data[1], "disk_status": data[2]}

        return jsonify(data_with_keys)
    return jsonify({"message": "NAS data not found"}), 404

def send_notification(message):
    # Get the notification URL from environment variable
    notification_url = os.getenv("NOTIFICATION_URL")
    if notification_url:
        apprise = Apprise()
        apprise.add(notification_url)
        apprise.notify(body=message)
    else:
        print("Notification URL not found. Notification not sent.")

if __name__ == '__main__':
    create_database()
    app.run(host='0.0.0.0', port=5000, debug=True)

