import os
import sqlite3
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_email(sender_email, receiver_email, subject, body, smtp_server, smtp_port, smtp_username, smtp_password):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def get_todays_date_and_success_count_from_db(db_filename):
    today_date = datetime.now().strftime('%Y-%m-%d')

    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()

    # Count occurrences of "Success" for today in the internet column
    cursor.execute("SELECT COUNT(*) FROM your_table_name WHERE date(date) = ? AND internet = 'Success'", (today_date,))
    success_count = cursor.fetchone()[0]

    connection.close()

    return today_date, success_count

# Load environment variables from .env file
load_dotenv()

# Get environment variables
sender_email = os.getenv("SENDER_EMAIL")
recipient_email = os.getenv("RECIPIENT_EMAIL")
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT"))
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD")
db_filename = os.getenv("DB_FILENAME")

# Get today's date and success count from the database
today_date, success_count = get_todays_date_and_success_count_from_db(db_filename)

# Example usage
subject = f"{today_date} Internet Check"
body = f"Date: {today_date}"
body += f"Success: {success_count}"

# Send the email
send_email(sender_email, recipient_email, subject, body, smtp_server, smtp_port, smtp_username, smtp_password)

