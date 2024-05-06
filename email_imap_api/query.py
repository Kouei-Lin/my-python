import sqlite3

def query_data_from_sqlite(db_filename):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # Example SELECT statement
    cursor.execute('SELECT * FROM emails')
    rows = cursor.fetchall()

    # Print the results
    for row in rows:
        print(row)

    # Close connection
    conn.close()

# Example usage
db_filename = 'your_db_name.db'
query_data_from_sqlite(db_filename)

