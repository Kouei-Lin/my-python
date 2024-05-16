import streamlit as st
import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Function to connect to SQLite database and execute query
def query_emails(selected_date):
    try:
        db_filename = os.getenv("LOCAL_DB_FILENAME")
        conn = sqlite3.connect(db_filename)
        query = f"SELECT * FROM emails WHERE Date >= '{selected_date}' ORDER BY Date DESC"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except FileNotFoundError:
        st.error(f"Database file '{db_filename}' not found.")
        return None
    except Exception as e:
        st.error(f"An error occurred while querying the database: {e}")
        return None

# Streamlit code for the web app
def main():
    st.title("Email Data Viewer")

    # Date selection widget
    selected_date = st.date_input("Select a date", datetime.now())

    # Execute query to fetch data based on selected date
    data = query_emails(selected_date.strftime('%Y-%m-%d'))

    # Display the queried data
    if data is not None:
        st.write("All Email Data from Selected Date onwards, ordered by Date (latest first):")
        st.write(data)

        # Calculate counts of Success, Failed, Retry, and Warning for the selected date
        if not data.empty:
            note_counts = data['note'].value_counts()
            st.write("Counts of Note Types from Selected Date onwards:")
            st.write("- Success:", note_counts.get("Success", 0))
            st.write("- Failed:", note_counts.get("Failed", 0))
            st.write("- Retry:", note_counts.get("Retry", 0))
            st.write("- Warning:", note_counts.get("Warning", 0))
        else:
            st.write("No emails found from the selected date onwards.")

if __name__ == "__main__":
    main()

