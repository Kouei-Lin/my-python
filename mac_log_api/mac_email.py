import os
import sqlite3
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, receiver_email, subject, body, smtp_server, smtp_port, smtp_username, smtp_password):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def get_latest_date_and_success_count_from_db(db_filename):
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()

    # Get the latest date
    cursor.execute("SELECT MAX(date) FROM your_table_name")  # Replace 'your_table_name' with your actual table name
    latest_date = cursor.fetchone()[0]

    # Count occurrences of "Success" in the internet column
    cursor.execute("SELECT COUNT(*) FROM your_table_name WHERE internet = 'Success'")  # Replace 'your_table_name' with your actual table name
    success_count = cursor.fetchone()[0]

    connection.close()

    return latest_date, success_count

# Load environment variables from .env file
load_dotenv()

# Get environment variables
sender_email = os.getenv("SENDER_EMAIL")
recipient_email = os.getenv("RECIPIENT_EMAIL")
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT"))
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD")
db_filename = os.getenv("DB_FILENAME")  # Assuming you have a variable named DB_FILENAME in your .env file

# Get the latest date and success count from the database
latest_date, success_count = get_latest_date_and_success_count_from_db(db_filename)

# Example usage
subject = "Latest Date and Success Count from Database"
body = f"The latest date from the database is: {latest_date}\n"
body += f"The count of 'Success' in the 'internet' column is: {success_count}"

# Send the email
send_email(sender_email, recipient_email, subject, body, smtp_server, smtp_port, smtp_username, smtp_password)

