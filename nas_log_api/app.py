from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import os
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
                        ip TEXT,
                        disk_usage REAL NOT NULL,
                        cpu_usage REAL NOT NULL,
                        ram_usage REAL NOT NULL
                    )''')
    conn.commit()
    conn.close()

# Create a new NAS data entry
@app.route('/api/nas', methods=['POST'])
def add_nas_data():
    new_data = request.json

    # Convert current datetime to Taipei timezone (UTC+8)
    taipei_timezone = timezone('Asia/Taipei')
    date_taipei = datetime.now(taipei_timezone)
    new_data['date'] = date_taipei.strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO nas_data (date, ip, disk_usage, cpu_usage, ram_usage)
                      VALUES (?, ?, ?, ?, ?)''', (new_data['date'], new_data['ip'], new_data['disk_usage'], new_data['cpu_usage'], new_data['ram_usage']))
    conn.commit()
    conn.close()

    # Send detailed notification
    logged_data = f"Logged data:\nDate: {new_data['date']}\nIP: {new_data['ip']}\nDisk Usage: {new_data['disk_usage']}%\nCPU Usage: {new_data['cpu_usage']}%\nRAM Usage: {new_data['ram_usage']}%"
    send_notification(logged_data)

    return jsonify({"message": "NAS data added successfully"}), 201

# Get all NAS data with column names
@app.route('/api/nas', methods=['GET'])
def get_nas_data():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nas_data")
    data = cursor.fetchall()
    conn.close()

    # Extract column names from the cursor description
    columns = [col[0] for col in cursor.description]

    # Combine column names with data values into dictionaries
    data_with_keys = [{columns[i]: row[i] for i in range(len(columns))} for row in data]

    return jsonify(data_with_keys)

# Get a single NAS data entry by ID with column names
@app.route('/api/nas/<int:id>', methods=['GET'])
def get_nas_data_by_id(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nas_data WHERE id=?", (id,))
    data = cursor.fetchone()
    conn.close()

    if data:
        # Extract column names from the cursor description
        columns = [col[0] for col in cursor.description]

        # Combine column names with data values into a dictionary
        data_with_keys = {columns[i]: data[i] for i in range(len(columns))}

        return jsonify(data_with_keys)
    return jsonify({"message": "NAS data not found"}), 404

# Update a NAS data entry by ID
@app.route('/api/nas/<int:id>', methods=['PUT'])
def update_nas_data(id):
    updated_data = request.json
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nas_data WHERE id=?", (id,))
    data = cursor.fetchone()
    if data:
        cursor.execute('''UPDATE nas_data SET date=?, ip=?, disk_usage=?, cpu_usage=?, ram_usage=? WHERE id=?''',
                       (updated_data['date'], updated_data['ip'], updated_data['disk_usage'], updated_data['cpu_usage'], updated_data['ram_usage'], id))
        conn.commit()
        conn.close()

        # Send detailed notification
        logged_data = f"Logged data updated for ID {id}:\nDate: {updated_data['date']}\nIP: {updated_data['ip']}\nDisk Usage: {updated_data['disk_usage']}%\nCPU Usage: {updated_data['cpu_usage']}%\nRAM Usage: {updated_data['ram_usage']}%"
        send_notification(logged_data)

        return jsonify({"message": "NAS data updated successfully"})
    return jsonify({"message": "NAS data not found"}), 404

# Delete a NAS data entry by ID
@app.route('/api/nas/<int:id>', methods=['DELETE'])
def delete_nas_data(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nas_data WHERE id=?", (id,))
    data = cursor.fetchone()
    if data:
        cursor.execute("DELETE FROM nas_data WHERE id=?", (id,))
        conn.commit()
        conn.close()

        # Send notification using Apprise
        send_notification("NAS data deleted")

        return jsonify({"message": "NAS data deleted successfully"})
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
