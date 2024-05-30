from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
from pytz import timezone

class FlaskAPIModule:
    def __init__(self, database, table, send_notification):
        self.app = Flask(__name__)
        self.app.config['DATABASE'] = database
        self.app.config['TABLE'] = table
        self.send_notification = send_notification

        # Define routes
        self.app.add_url_rule('/api/item', 'add_item', self.add_item, methods=['POST'])
        self.app.add_url_rule('/api/item', 'get_items', self.get_items, methods=['GET'])
        self.app.add_url_rule('/api/item/<int:id>', 'get_item', self.get_item, methods=['GET'])
        self.app.add_url_rule('/api/item/<int:id>', 'update_item', self.update_item, methods=['PUT'])
        self.app.add_url_rule('/api/item/<int:id>', 'delete_item', self.delete_item, methods=['DELETE'])

    def create_database(self, sql_create_table):
        conn = sqlite3.connect(self.app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute(sql_create_table)
        conn.commit()
        conn.close()

    def add_item(self):
        new_item = request.json

        # Set current datetime in Taipei timezone if not provided
        if 'date' not in new_item:
            taipei_timezone = timezone('Asia/Taipei')
            new_item['date'] = datetime.now(taipei_timezone).strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect(self.app.config['DATABASE'])
        cursor = conn.cursor()
        columns = ', '.join(new_item.keys())
        placeholders = ', '.join('?' for _ in new_item)
        values = tuple(new_item.values())
        cursor.execute(f'INSERT INTO {self.app.config["TABLE"]} ({columns}) VALUES ({placeholders})', values)
        conn.commit()
        conn.close()

        self.send_notification(f"New item added: {new_item}")
        return jsonify({"message": "Item added successfully"}), 201

    def get_items(self):
        conn = sqlite3.connect(self.app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.app.config['TABLE']}")
        items = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        conn.close()

        items_with_keys = [{columns[i]: item[i] for i in range(len(columns))} for item in items]
        return jsonify(items_with_keys)

    def get_item(self, id):
        conn = sqlite3.connect(self.app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.app.config['TABLE']} WHERE id=?", (id,))
        item = cursor.fetchone()
        conn.close()

        if item:
            columns = [col[0] for col in cursor.description]
            item_with_keys = {columns[i]: item[i] for i in range(len(columns))}
            return jsonify(item_with_keys)
        return jsonify({"message": "Item not found"}), 404

    def update_item(self, id):
        updated_item = request.json
        conn = sqlite3.connect(self.app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.app.config['TABLE']} WHERE id=?", (id,))
        item = cursor.fetchone()
        if item:
            columns = ', '.join(f'{k}=?' for k in updated_item.keys())
            values = tuple(updated_item.values()) + (id,)
            cursor.execute(f'UPDATE {self.app.config["TABLE"]} SET {columns} WHERE id=?', values)
            conn.commit()
            conn.close()

            self.send_notification(f"Item updated: {updated_item}")
            return jsonify({"message": "Item updated successfully"})
        return jsonify({"message": "Item not found"}), 404

    def delete_item(self, id):
        conn = sqlite3.connect(self.app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.app.config['TABLE']} WHERE id=?", (id,))
        item = cursor.fetchone()
        if item:
            cursor.execute(f"DELETE FROM {self.app.config['TABLE']} WHERE id=?", (id,))
            conn.commit()
            conn.close()

            self.send_notification("Item deleted")
            return jsonify({"message": "Item deleted successfully"})
        return jsonify({"message": "Item not found"}), 404

