from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to establish database connection
def get_db_connection():
    conn = sqlite3.connect('network_data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create SQLite database table if not exists
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            mac_address TEXT NOT NULL UNIQUE,
            appear_before TEXT NOT NULL,
            interface TEXT NOT NULL,
            internet TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Create a new device
@app.route('/api/mac', methods=['POST'])
def add_device():
    new_device = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO devices (name, mac_address, appear_before, interface, internet)
        VALUES (?, ?, ?, ?, ?)
    ''', (new_device['name'], new_device['mac_address'], new_device['appear_before'], new_device['interface'], new_device['internet']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Device added successfully"}), 201

# Get all devices
@app.route('/api/mac', methods=['GET'])
def get_devices():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM devices')
    devices = cursor.fetchall()
    conn.close()

    devices_list = []
    for device in devices:
        # Convert Row object to dictionary
        device_dict = dict(device)
        devices_list.append(device_dict)

    return jsonify(devices_list)

# Get a single device by ID
@app.route('/api/mac/<int:id>', methods=['GET'])
def get_device(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM devices WHERE id = ?', (id,))
    device = cursor.fetchone()
    conn.close()

    if device:
        device_dict = dict(device)
        return jsonify(device_dict)
    else:
        return jsonify({"message": "Device not found"}), 404

# Update a device by ID
@app.route('/api/mac/<int:id>', methods=['PUT'])
def update_device(id):
    updated_device = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE devices
        SET name = ?, mac_address = ?, appear_before = ?, interface = ?, internet = ?
        WHERE id = ?
    ''', (updated_device['name'], updated_device['mac_address'], updated_device['appear_before'], updated_device['interface'], updated_device['internet'], id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Device updated successfully"})

# Delete a device by ID
@app.route('/api/mac/<int:id>', methods=['DELETE'])
def delete_device(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM devices WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Device deleted successfully"})

if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', port=5000, debug=True)

