import sqlite3
import os
from dotenv import load_dotenv

class SQLiteQuery:
    def __init__(self, local_db_filename=None, remote_db_filename=None, remote_host=None, remote_port=None, remote_username=None, remote_password=None):
        load_dotenv()
        self.local_db_filename = local_db_filename or os.getenv('LOCAL_DB_FILENAME')
        self.remote_db_filename = remote_db_filename or os.getenv('REMOTE_DB_FILENAME')
        self.remote_host = remote_host or os.getenv('REMOTE_HOST')
        self.remote_port = remote_port or int(os.getenv('REMOTE_PORT'))
        self.remote_username = remote_username or os.getenv('REMOTE_USERNAME')
        self.remote_password = remote_password or os.getenv('REMOTE_PASSWORD')
    
    def query_local_db(self):
        conn = sqlite3.connect(self.local_db_filename)
        cursor = conn.cursor()

        # Example SELECT statement
        cursor.execute('SELECT * FROM emails')
        rows = cursor.fetchall()

        # Print the results
        for row in rows:
            print(row)

        # Close connection
        conn.close()
    
    def query_remote_db(self):
        ssh_conn = sqlite3.connect(f'ssh://{self.remote_username}:{self.remote_password}@{self.remote_host}:{self.remote_port}/{self.remote_db_filename}')
        cursor = ssh_conn.cursor()

        # Example SELECT statement
        cursor.execute('SELECT * FROM emails')
        rows = cursor.fetchall()

        # Print the results
        for row in rows:
            print(row)

        # Close connection
        ssh_conn.close()

# Example usage for local SQLite database
local_query = SQLiteQuery()
local_query.query_local_db()

# Example usage for remote SQLite database via SSH
# remote_query = SQLiteQuery()
# remote_query.query_remote_db()

