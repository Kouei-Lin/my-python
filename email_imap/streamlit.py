import streamlit as st
import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv
import re

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

# Function to extract numerical value and unit from string
def extract_value(s):
    match = re.match(r'(\d+(\.\d+)?)\s*(\w+)', s)
    if match:
        return float(match.group(1))
    else:
        return None

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

        # Convert column names to lowercase
        data.columns = map(str.lower, data.columns)

        # Extract numerical values from 'size', 'read', and 'transferred' columns if present
        for col in ['size', 'read', 'transferred']:
            if col in data.columns:
                data[col + '_value'] = data[col].apply(extract_value)

                # Drop original column
                data.drop(columns=[col], inplace=True)
            else:
                st.warning(f"Column '{col}' not found in the DataFrame.")

        # Calculate mean of the numerical value columns
        mean_values = data[['size_value', 'read_value', 'transferred_value']].mean()

        # Display the mean values
        st.write("Mean Values:")
        st.write(mean_values)

if __name__ == "__main__":
    main()

