from flask import Flask, request, jsonify
import csv

app = Flask(__name__)
CSV_FILE = 'network_data.csv'

# Create CSV file if not exists
def create_csv_file():
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'name', 'mac_address', 'appear_before', 'interface', 'internet'])

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
        fieldnames = ['id', 'name', 'mac_address', 'appear_before', 'interface', 'internet']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for device in devices:
            writer.writerow(device)

# Create a new device
@app.route('/api/mac', methods=['POST'])
def add_device():
    new_device = request.json
    devices = read_devices_from_csv()
    new_device['id'] = len(devices) + 1
    devices.append(new_device)
    write_devices_to_csv(devices)
    return jsonify({"message": "Device added successfully"}), 201

# Get all devices
@app.route('/api/mac', methods=['GET'])
def get_devices():
    devices = read_devices_from_csv()
    return jsonify(devices)

# Get a single device by ID
@app.route('/api/mac/<int:id>', methods=['GET'])
def get_device(id):
    devices = read_devices_from_csv()
    for device in devices:
        if int(device['id']) == id:
            return jsonify(device)
    return jsonify({"message": "Device not found"}), 404

# Update a device by ID
@app.route('/api/mac/<int:id>', methods=['PUT'])
def update_device(id):
    updated_device = request.json
    devices = read_devices_from_csv()
    for device in devices:
        if int(device['id']) == id:
            device.update(updated_device)
            write_devices_to_csv(devices)
            return jsonify({"message": "Device updated successfully"})
    return jsonify({"message": "Device not found"}), 404

# Delete a device by ID
@app.route('/api/mac/<int:id>', methods=['DELETE'])
def delete_device(id):
    devices = read_devices_from_csv()
    for device in devices:
        if int(device['id']) == id:
            devices.remove(device)
            write_devices_to_csv(devices)
            return jsonify({"message": "Device deleted successfully"})
    return jsonify({"message": "Device not found"}), 404

if __name__ == '__main__':
    create_csv_file()
    app.run(host='0.0.0.0', port=5000, debug=True)

