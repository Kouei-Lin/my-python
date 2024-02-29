from flask import Flask, request, jsonify
import csv
from datetime import datetime, timedelta

app = Flask(__name__)
CSV_FILE = 'network_data.csv'

# Create CSV file if not exists or is empty
def create_csv_file():
    try:
        with open(CSV_FILE, 'r') as file:
            if len(file.read().strip()) == 0:
                with open(CSV_FILE, 'a', newline='') as new_file:
                    writer = csv.writer(new_file)
                    writer.writerow(['date', 'name', 'mac_address', 'appear_before', 'interface', 'internet'])
    except FileNotFoundError:
        with open(CSV_FILE, 'a', newline='') as new_file:
            writer = csv.writer(new_file)
            writer.writerow(['date', 'name', 'mac_address', 'appear_before', 'interface', 'internet'])

# Function to read devices from CSV file
def read_devices_from_csv():
    devices = []
    with open(CSV_FILE, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            devices.append(row)
    return devices

# Function to write devices to CSV file
def write_devices_to_csv(devices):
    with open(CSV_FILE, 'w', newline='') as file:
        fieldnames = ['date', 'name', 'mac_address', 'appear_before', 'interface', 'internet']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for device in devices:
            writer.writerow(device)

# Convert UTC to UTC+8
def convert_utc_to_utc_plus_8(utc_time):
    utc_plus_8_time = datetime.strptime(utc_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
    return utc_plus_8_time.strftime('%Y-%m-%d %H:%M:%S')

# Create a new device
@app.route('/api/mac', methods=['POST'])
def add_device():
    new_device = request.json
    new_device['date'] = request.json.get('date', convert_utc_to_utc_plus_8(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))
    devices = read_devices_from_csv()
    devices.append(new_device)
    write_devices_to_csv(devices)
    return jsonify({"message": "Device added successfully"}), 201

# Get all devices
@app.route('/api/mac', methods=['GET'])
def get_devices():
    devices = read_devices_from_csv()
    return jsonify(devices)

# Get a single device by row index
@app.route('/api/mac/<int:index>', methods=['GET'])
def get_device(index):
    devices = read_devices_from_csv()
    if 0 <= index < len(devices):
        return jsonify(devices[index])
    return jsonify({"message": "Device not found"}), 404

# Update a device by row index
@app.route('/api/mac/<int:index>', methods=['PUT'])
def update_device(index):
    updated_device = request.json
    devices = read_devices_from_csv()
    if 0 <= index < len(devices):
        devices[index].update(updated_device)
        write_devices_to_csv(devices)
        return jsonify({"message": "Device updated successfully"})
    return jsonify({"message": "Device not found"}), 404

# Delete a device by row index
@app.route('/api/mac/<int:index>', methods=['DELETE'])
def delete_device(index):
    devices = read_devices_from_csv()
    if 0 <= index < len(devices):
        del devices[index]
        write_devices_to_csv(devices)
        return jsonify({"message": "Device deleted successfully"})
    return jsonify({"message": "Device not found"}), 404

if __name__ == '__main__':
    create_csv_file()
    app.run(host='0.0.0.0', port=5000, debug=True)

