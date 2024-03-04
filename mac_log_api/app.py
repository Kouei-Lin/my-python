from flask import Flask, request, jsonify
import json
from datetime import datetime
from dotenv import load_dotenv
import os
from apprise import Apprise
from pytz import timezone

app = Flask(__name__)
JSON_FILE = 'network_data.json'

# Load environment variables from .env file
load_dotenv()

# Function to create JSON file if not exists
def create_json_file():
    try:
        with open(JSON_FILE, 'r') as file:
            json_data = json.load(file)
    except FileNotFoundError:
        with open(JSON_FILE, 'w') as new_file:
            json.dump([], new_file)

# Function to read devices from JSON file
def read_devices_from_json():
    try:
        with open(JSON_FILE, 'r') as file:
            devices = json.load(file)
    except FileNotFoundError:
        devices = []
    return devices

# Function to write devices to JSON file
def write_devices_to_json(devices):
    with open(JSON_FILE, 'w') as file:
        json.dump(devices, file, indent=4)

# Create a new device
@app.route('/api/mac', methods=['POST'])
def add_device():
    new_device = request.json
    
    # Convert current datetime to UTC+8
    utc_8 = timezone('Asia/Taipei')
    date_utc_8 = datetime.now(pytz.utc).astimezone(utc_8)
    new_device['date'] = date_utc_8.strftime('%Y-%m-%d %H:%M:%S')

    devices = read_devices_from_json()

    # Add index to the new device
    new_device['index'] = len(devices)

    devices.append(new_device)
    write_devices_to_json(devices)

    # Send notification using Apprise
    send_notification(f"New device added: {new_device}")

    return jsonify({"message": "Device added successfully"}), 201

# Get all devices
@app.route('/api/mac', methods=['GET'])
def get_devices():
    devices = read_devices_from_json()
    return jsonify(devices)

# Get a single device by index
@app.route('/api/mac/<int:index>', methods=['GET'])
def get_device(index):
    devices = read_devices_from_json()
    if 0 <= index < len(devices):
        return jsonify(devices[index])
    return jsonify({"message": "Device not found"}), 404

# Update a device by index
@app.route('/api/mac/<int:index>', methods=['PUT'])
def update_device(index):
    updated_device = request.json
    devices = read_devices_from_json()
    if 0 <= index < len(devices):
        devices[index] = updated_device
        write_devices_to_json(devices)

        # Send notification using Apprise
        send_notification(f"Device updated: {updated_device}")

        return jsonify({"message": "Device updated successfully"})
    return jsonify({"message": "Device not found"}), 404

# Delete a device by index
@app.route('/api/mac/<int:index>', methods=['DELETE'])
def delete_device(index):
    devices = read_devices_from_json()
    if 0 <= index < len(devices):
        del devices[index]
        write_devices_to_json(devices)

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
    create_json_file()
    app.run(host='0.0.0.0', port=5000, debug=True)

