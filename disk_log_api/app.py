from flask import Flask, request, jsonify
import json
from datetime import datetime
from dotenv import load_dotenv
import os
from apprise import Apprise
from pytz import timezone
import sqlite3

app = Flask(__name__)
DATABASE = 'disk_data.db'

# Load environment variables from .env file
load_dotenv()

# Function to create SQLite database if not exists
def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS disks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        device_id TEXT NOT NULL,
                        volume_name TEXT NOT NULL,
                        size INTEGER NOT NULL,
                        free_space INTEGER NOT NULL,
                        used_space INTEGER NOT NULL
                    )''')
    conn.commit()
    conn.close()

# Create a new disk entry
@app.route('/api/disk', methods=['POST'])
def add_disk():
    new_disk = request.json
    
    # Convert current datetime to Taipei timezone (UTC+8)
    taipei_timezone = timezone('Asia/Taipei')
    date_taipei = datetime.now(taipei_timezone)
    new_disk['date'] = date_taipei.strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO disks (date, device_id, volume_name, size, free_space, used_space)
                      VALUES (?, ?, ?, ?, ?, ?)''', (new_disk['date'], new_disk['device_id'], new_disk['volume_name'], new_disk['size'], new_disk['free_space'], new_disk['used_space']))
    conn.commit()
    conn.close()

    # Send notification using Apprise
    send_notification(f"New disk entry added: {new_disk}")

    return jsonify({"message": "Disk entry added successfully"}), 201

# Get all disk entries with column names
@app.route('/api/disk', methods=['GET'])
def get_disks():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM disks")
    disks = cursor.fetchall()
    conn.close()

    # Extract column names from the cursor description
    columns = [col[0] for col in cursor.description]

    # Combine column names with disk entry values into dictionaries
    disks_with_keys = [{columns[i]: disk[i] for i in range(len(columns))} for disk in disks]

    return jsonify(disks_with_keys)

# Get a single disk entry by ID with column names
@app.route('/api/disk/<int:index>', methods=['GET'])
def get_disk(index):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM disks WHERE id=?", (index,))
    disk = cursor.fetchone()
    conn.close()

    if disk:
        # Extract column names from the cursor description
        columns = [col[0] for col in cursor.description]

        # Combine column names with disk entry values into a dictionary
        disk_with_keys = {columns[i]: disk[i] for i in range(len(columns))}

        return jsonify(disk_with_keys)
    return jsonify({"message": "Disk entry not found"}), 404

# Update a disk entry by ID
@app.route('/api/disk/<int:index>', methods=['PUT'])
def update_disk(index):
    updated_disk = request.json
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM disks WHERE id=?", (index,))
    disk = cursor.fetchone()
    if disk:
        cursor.execute('''UPDATE disks SET date=?, device_id=?, volume_name=?, size=?, free_space=?, used_space=? WHERE id=?''',
                       (updated_disk['date'], updated_disk['device_id'], updated_disk['volume_name'], updated_disk['size'], updated_disk['free_space'], updated_disk['used_space'], index))
        conn.commit()
        conn.close()

        # Send notification using Apprise
        send_notification(f"Disk entry updated: {updated_disk}")

        return jsonify({"message": "Disk entry updated successfully"})
    return jsonify({"message": "Disk entry not found"}), 404

# Delete a disk entry by ID
@app.route('/api/disk/<int:index>', methods=['DELETE'])
def delete_disk(index):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM disks WHERE id=?", (index,))
    disk = cursor.fetchone()
    if disk:
        cursor.execute("DELETE FROM disks WHERE id=?", (index,))
        conn.commit()
        conn.close()

        # Send notification using Apprise
        send_notification("Disk entry deleted")

        return jsonify({"message": "Disk entry deleted successfully"})
    return jsonify({"message": "Disk entry not found"}), 404

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

