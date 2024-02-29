from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)
JSON_FILE = 'network_data.json'

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
    with open(JSON_FILE, 'r') as file:
        devices = json.load(file)
    return devices

# Function to write devices to JSON file
def write_devices_to_json(devices):
    with open(JSON_FILE, 'w') as file:
        json.dump(devices, file, indent=4)

# Create a new device
@app.route('/api/mac', methods=['POST'])
def add_device():
    new_device = request.json
    new_device['date'] = request.json.get('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    devices = read_devices_from_json()
    devices.append(new_device)
    write_devices_to_json(devices)
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
        return jsonify({"message": "Device updated successfully"})
    return jsonify({"message": "Device not found"}), 404

# Delete a device by index
@app.route('/api/mac/<int:index>', methods=['DELETE'])
def delete_device(index):
    devices = read_devices_from_json()
    if 0 <= index < len(devices):
        del devices[index]
        write_devices_to_json(devices)
        return jsonify({"message": "Device deleted successfully"})
    return jsonify({"message": "Device not found"}), 404

if __name__ == '__main__':
    create_json_file()
    app.run(host='0.0.0.0', port=5000, debug=True)

