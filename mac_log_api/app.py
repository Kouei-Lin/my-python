from flask import Flask, request, jsonify
import json
from datetime import datetime
from dotenv import load_dotenv
import os
from apprise import Apprise
from pytz import timezone
import sqlite3

app = Flask(__name__)
DATABASE = 'network_data.db'

# Load environment variables from .env file
load_dotenv()

# Function to create SQLite database if not exists
def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS devices (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        name TEXT NOT NULL,
                        mac_address TEXT NOT NULL,
                        appear_before TEXT NOT NULL,
                        interface TEXT NOT NULL,
                        internet TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

# Create a new device
@app.route('/api/mac', methods=['POST'])
def add_device():
    new_device = request.json
    
    # Convert current datetime to Taipei timezone (UTC+8)
    taipei_timezone = timezone('Asia/Taipei')
    date_taipei = datetime.now(taipei_timezone)
    new_device['date'] = date_taipei.strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO devices (date, name, mac_address, appear_before, interface, internet)
                      VALUES (?, ?, ?, ?, ?, ?)''', (new_device['date'], new_device['name'], new_device['mac_address'], new_device['appear_before'], new_device['interface'], new_device['internet']))
    conn.commit()
    conn.close()

    # Send notification using Apprise
    send_notification(f"New device added: {new_device}")

    return jsonify({"message": "Device added successfully"}), 201

# Get all devices with column names
@app.route('/api/mac', methods=['GET'])
def get_devices():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices")
    devices = cursor.fetchall()
    conn.close()

    # Extract column names from the cursor description
    columns = [col[0] for col in cursor.description]

    # Combine column names with device values into dictionaries
    devices_with_keys = [{columns[i]: device[i] for i in range(len(columns))} for device in devices]

    return jsonify(devices_with_keys)

# Get a single device by ID with column names
@app.route('/api/mac/<int:index>', methods=['GET'])
def get_device(index):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices WHERE id=?", (index,))
    device = cursor.fetchone()
    conn.close()

    if device:
        # Extract column names from the cursor description
        columns = [col[0] for col in cursor.description]

        # Combine column names with device values into a dictionary
        device_with_keys = {columns[i]: device[i] for i in range(len(columns))}

        return jsonify(device_with_keys)
    return jsonify({"message": "Device not found"}), 404

# Update a device by ID
@app.route('/api/mac/<int:index>', methods=['PUT'])
def update_device(index):
    updated_device = request.json
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices WHERE id=?", (index,))
    device = cursor.fetchone()
    if device:
        cursor.execute('''UPDATE devices SET date=?, name=?, mac_address=?, appear_before=?, interface=?, internet=? WHERE id=?''',
                       (updated_device['date'], updated_device['name'], updated_device['mac_address'], updated_device['appear_before'], updated_device['interface'], updated_device['internet'], index))
        conn.commit()
        conn.close()

        # Send notification using Apprise
        send_notification(f"Device updated: {updated_device}")

        return jsonify({"message": "Device updated successfully"})
    return jsonify({"message": "Device not found"}), 404

# Delete a device by ID
@app.route('/api/mac/<int:index>', methods=['DELETE'])
def delete_device(index):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices WHERE id=?", (index,))
    device = cursor.fetchone()
    if device:
        cursor.execute("DELETE FROM devices WHERE id=?", (index,))
        conn.commit()
        conn.close()

        # Send notification using Apprise
        send_notification("Device deleted")

        return jsonify({"message": "Device deleted successfully"})
    return jsonify({"message": "Device not found"}), 404

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

