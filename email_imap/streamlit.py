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
        value = float(match.group(1))
        unit = match.group(3).upper()
        return value, unit
    else:
        return None, None

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

        # Extract numerical values and units from 'size', 'read', and 'transferred' columns if present
        for col in ['size', 'read', 'transferred']:
            if col in data.columns:
                data[f'{col}_value'], data[f'{col}_unit'] = zip(*data[col].apply(extract_value))

                # Convert size to MB if unit is GB
                data.loc[data[f'{col}_unit'] == 'GB', f'{col}_value'] *= 1000

                # Drop original columns
                data.drop(columns=[col, f'{col}_unit'], inplace=True)
            else:
                st.warning(f"Column '{col}' not found in the DataFrame.")

        # Calculate mean of the numerical value columns
        mean_values = data[['size_value', 'read_value', 'transferred_value']].mean()

        # Convert mean values to GB if they are greater than or equal to 1000 MB
        mean_values_gb = mean_values.apply(lambda x: x / 1000 if x >= 1000 else x)

        # Display the mean values side by side
        st.write(f"Avg. Size: {mean_values_gb['size_value']:.2f} {'GB' if mean_values_gb['size_value'] >= 1 else 'MB'}")
        st.write(f"Avg. Read: {mean_values_gb['read_value']:.2f} {'GB' if mean_values_gb['read_value'] >= 1 else 'MB'}")
        st.write(f"Avg. Transferred: {mean_values_gb['transferred_value']:.2f} {'GB' if mean_values_gb['transferred_value'] >= 1 else 'MB'}")

if __name__ == "__main__":
    main()

