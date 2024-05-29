from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
from pytz import timezone

def create_app(database, table, send_notification):
    app = Flask(__name__)
    app.config['DATABASE'] = database
    app.config['TABLE'] = table

    def create_database(sql_create_table):
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute(sql_create_table)
        conn.commit()
        conn.close()

    @app.route('/api/item', methods=['POST'])
    def add_item():
        new_item = request.json

        # Set current datetime in Taipei timezone if not provided
        if 'date' not in new_item:
            taipei_timezone = timezone('Asia/Taipei')
            new_item['date'] = datetime.now(taipei_timezone).strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        columns = ', '.join(new_item.keys())
        placeholders = ', '.join('?' for _ in new_item)
        values = tuple(new_item.values())
        cursor.execute(f'INSERT INTO {app.config["TABLE"]} ({columns}) VALUES ({placeholders})', values)
        conn.commit()
        conn.close()

        send_notification(f"New item added: {new_item}")
        return jsonify({"message": "Item added successfully"}), 201

    @app.route('/api/item', methods=['GET'])
    def get_items():
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {app.config['TABLE']}")
        items = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        conn.close()

        items_with_keys = [{columns[i]: item[i] for i in range(len(columns))} for item in items]
        return jsonify(items_with_keys)

    @app.route('/api/item/<int:id>', methods=['GET'])
    def get_item(id):
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {app.config['TABLE']} WHERE id=?", (id,))
        item = cursor.fetchone()
        conn.close()

        if item:
            columns = [col[0] for col in cursor.description]
            item_with_keys = {columns[i]: item[i] for i in range(len(columns))}
            return jsonify(item_with_keys)
        return jsonify({"message": "Item not found"}), 404

    @app.route('/api/item/<int:id>', methods=['PUT'])
    def update_item(id):
        updated_item = request.json
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {app.config['TABLE']} WHERE id=?", (id,))
        item = cursor.fetchone()
        if item:
            columns = ', '.join(f'{k}=?' for k in updated_item.keys())
            values = tuple(updated_item.values()) + (id,)
            cursor.execute(f'UPDATE {app.config["TABLE"]} SET {columns} WHERE id=?', values)
            conn.commit()
            conn.close()

            send_notification(f"Item updated: {updated_item}")
            return jsonify({"message": "Item updated successfully"})
        return jsonify({"message": "Item not found"}), 404

    @app.route('/api/item/<int:id>', methods=['DELETE'])
    def delete_item(id):
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {app.config['TABLE']} WHERE id=?", (id,))
        item = cursor.fetchone()
        if item:
            cursor.execute(f"DELETE FROM {app.config['TABLE']} WHERE id=?", (id,))
            conn.commit()
            conn.close()

            send_notification("Item deleted")
            return jsonify({"message": "Item deleted successfully"})
        return jsonify({"message": "Item not found"}), 404

    return app, create_database
