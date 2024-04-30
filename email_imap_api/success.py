import os
import csv
import imaplib
from dotenv import load_dotenv
from email import message_from_bytes
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

# Get IMAP server URL, username, and password from environment variables
imap_server_url = os.getenv('IMAP_SERVER_URL')
imap_username = os.getenv('IMAP_USERNAME')
imap_password = os.getenv('IMAP_PASSWORD')
mailbox_folder = os.getenv('SUCCESS_FOLDER')

# Connect to the IMAP server without SSL/TLS encryption
imap_server = imaplib.IMAP4(imap_server_url)

# Log in to the account
imap_server.login(imap_username, imap_password)

# Select the mailbox folder specified in the .env file
imap_server.select(mailbox_folder)

# Search for emails in the selected folder (e.g., all emails)
status, data = imap_server.search(None, 'ALL')

# Initialize a list to store email content
emails_content = []

# Iterate through each email in the folder
for email_uid in data[0].split():
    try:
        print(f"Fetching email with UID: {email_uid}...")
        # Fetch the email using its UID
        status, email_data = imap_server.fetch(email_uid, '(RFC822)')
        
        # Parse the email data
        email_message = message_from_bytes(email_data[0][1])
        
        # Get email content (e.g., subject, body, etc.)
        subject = email_message['Subject']
        body = email_message.get_payload(decode=True).decode()

        # Use BeautifulSoup to parse the XML body
        soup = BeautifulSoup(body, 'html.parser')

        # Get required information from the email body
        start_time = soup.find('td', string='Start time').find_next_sibling('td').text.strip() if soup.find('td', string='Start time') else 'N/A'
        end_time = soup.find('td', string='End time').find_next_sibling('td').text.strip() if soup.find('td', string='End time') else 'N/A'
        size = soup.find('td', string='Total size').find_next_sibling('td').text.strip() if soup.find('td', string='Total size') else 'N/A'
        read = soup.find('td', string='Data read').find_next_sibling('td').text.strip() if soup.find('td', string='Data read') else 'N/A'
        transferred = soup.find('td', string='Transferred').find_next_sibling('td').text.strip() if soup.find('td', string='Transferred') else 'N/A'
        duration = soup.find('td', string='Duration').find_next_sibling('td').text.strip() if soup.find('td', string='Duration') else 'N/A'

        # Determine the value for the 'Subject' column
        if 'MAWF' in subject:
            subject_value = 'MAWF'
        elif 'SECOM' in subject:
            subject_value = 'SECOM'
        elif 'NAS' in subject:
            subject_value = 'NAS'
        elif 'MediaWiki' in subject:
            subject_value = 'WiKi'
        elif 'Mantis' in subject:
            subject_value = 'Mantis'
        elif 'IOC_RMA_PDR' in subject:
            subject_value = 'IOC_RMA_PDR'
        elif 'Gitlab' in subject:
            subject_value = 'Gitlab'
        elif 'Jira' in subject:
            subject_value = 'Jira'
        elif 'PLM' in subject:
            subject_value = 'PLM'
        elif 'PDM2' in subject:
            subject_value = 'PDM2'
        elif 'SSRS' in subject:
            subject_value = 'SSRS'
        elif 'Sales_Portal' in subject:
            subject_value = 'Sales_Portal'
        else:
            subject_value = 'ELSE'

        # Append email content to the list
        emails_content.append({
            'Subject': subject_value,
            'Start Time': start_time,
            'End Time': end_time,
            'Size': size,
            'Read': read,
            'Transferred': transferred,
            'Duration': duration
        })
    except Exception as e:
        print(f"Error processing email with UID {email_uid}: {e}")

# Save email content to a CSV file
csv_filename = 'success.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Subject', 'Start Time', 'End Time', 'Size', 'Read', 'Transferred', 'Duration']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for email_content in emails_content:
        writer.writerow(email_content)

# Print a message to confirm that the CSV file has been created
print(f"Email content saved to {csv_filename}")

# Don't forget to close the connection when done
imap_server.logout()

        else:
            subject_value = 'ELSE'

        # Append email content to the list
        emails_content.append({
            'Subject': subject_value,
            'Start Time': start_time,
            'End Time': end_time,
            'Size': size,
            'Read': read,
            'Transferred': transferred,
            'Duration': duration
        })
    except Exception as e:
        print(f"Error processing email with UID {email_uid}: {e}")

# Save email content to a CSV file
csv_filename = 'success.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Subject', 'Start Time', 'End Time', 'Size', 'Read', 'Transferred', 'Duration']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for email_content in emails_content:
        writer.writerow(email_content)

# Print a message to confirm that the CSV file has been created
print(f"Email content saved to {csv_filename}")

# Don't forget to close the connection when done
imap_server.logout()

