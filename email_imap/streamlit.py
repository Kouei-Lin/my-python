import streamlit as st
import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to connect to SQLite database and execute query
def query_emails(subject):
    try:
        db_filename = os.getenv("LOCAL_DB_FILENAME")
        conn = sqlite3.connect(db_filename)
        query = f"SELECT * FROM emails WHERE Subject = '{subject}' ORDER BY Date DESC"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except FileNotFoundError:
        st.error(f"Database file '{db_filename}' not found.")
        return None
    except Exception as e:
        st.error(f"An error occurred while querying the database: {e}")
        return None

# Function to calculate average values
def calculate_average(data):
    # Remove the unit from size, read, and transferred columns and convert to numeric
    data['size'] = data['size'].str.replace(' GB', '').astype(float)
    data['read'] = data['read'].str.replace(' GB', '').astype(float)
    data['transferred'] = data['transferred'].str.replace(' GB', '').astype(float)
    
    # Convert duration to seconds
    data['duration'] = pd.to_timedelta(data['duration']).dt.total_seconds()
    
    avg_size = data['size'].mean()
    avg_read = data['read'].mean()
    avg_transferred = data['transferred'].mean()
    avg_duration_seconds = data['duration'].mean()
    
    # Convert average duration from seconds to hh:mm:ss format
    avg_duration_hms = pd.to_timedelta(avg_duration_seconds, unit='s')
    avg_duration_str = str(avg_duration_hms).split()[2]  # Extracting hh:mm:ss from timedelta
    
    return avg_size, avg_read, avg_transferred, avg_duration_str

# Streamlit code for the web app
def main():
    st.title("Email Data Viewer")

    # Select subject
    selected_subject = st.selectbox("Select Subject:", ["MAWF", "SECOM"])

    # Execute query to fetch data based on selected subject
    data = query_emails(selected_subject)

    # Display the queried data
    if data is not None:
        st.write(f"Email Data for {selected_subject}, ordered by Date (latest first):")
        st.write(data)

        # Calculate average values
        avg_size, avg_read, avg_transferred, avg_duration = calculate_average(data)

        # Display average values
        st.write(f"Avg. size: {avg_size:.2f} GB")
        st.write(f"Avg. read: {avg_read:.2f} GB")
        st.write(f"Avg. transferred: {avg_transferred:.2f} GB")
        st.write(f"Avg. duration: {avg_duration}")

if __name__ == "__main__":
    main()

