import os
import csv
import imaplib
from dotenv import load_dotenv
from email import message_from_bytes
from bs4 import BeautifulSoup
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get IMAP server URL, username, and password from environment variables
imap_server_url = os.getenv('IMAP_SERVER_URL')
imap_username = os.getenv('IMAP_USERNAME')
imap_password = os.getenv('IMAP_PASSWORD')
mailbox_folder = os.getenv('MAIL_FOLDER')

def login_to_imap_server(imap_server_url, username, password):
    # Login to the IMAP server.
    imap_server = imaplib.IMAP4(imap_server_url)
    imap_server.login(username, password)
    return imap_server

def fetch_emails(imap_server, mailbox_folder):
    # Fetch emails from the specified mailbox folder.
    status, data = imap_server.select(mailbox_folder)
    if status != 'OK':
        raise ValueError(f"Failed to select mailbox folder {mailbox_folder}.")
    
    status, email_ids = imap_server.search(None, 'ALL')
    if status != 'OK':
        raise ValueError("Failed to search for emails.")
    
    return email_ids[0].split()

def parse_email_content(email_data):
    # Parse email content and extract date.
    email_message = message_from_bytes(email_data)
    subject = email_message['Subject']
    date_str = email_message['Date']
    date = datetime.strptime(date_str, '%d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d')
    body = email_message.get_payload(decode=True).decode()
    return subject, date, body

def extract_information_from_body(body):
    # Extract required information from the email body.
    soup = BeautifulSoup(body, 'html.parser')
    
    # Initialize variables to store extracted information
    start_time = soup.find('td', string='Start time').find_next_sibling('td').text.strip() if soup.find('td', string='Start time') else 'N/A'
    end_time = soup.find('td', string='End time').find_next_sibling('td').text.strip() if soup.find('td', string='End time') else 'N/A'
    size = soup.find('td', string='Total size').find_next_sibling('td').text.strip() if soup.find('td', string='Total size') else 'N/A'
    read = soup.find('td', string='Data read').find_next_sibling('td').text.strip() if soup.find('td', string='Data read') else 'N/A'
    transferred = soup.find('td', string='Transferred').find_next_sibling('td').text.strip() if soup.find('td', string='Transferred') else 'N/A'
    duration = soup.find('td', string='Duration').find_next_sibling('td').text.strip() if soup.find('td', string='Duration') else 'N/A'
    
    return start_time, end_time, size, read, transferred, duration

def determine_subject(subject):
    # Determine the value for the 'Subject' column.
    if 'MAWF' in subject:
        return 'MAWF'
    elif 'SECOM' in subject:
        return 'SECOM'
    elif 'NAS' in subject:
        return 'NAS'
    elif 'IOC_RMA_PDR' in subject:
        return 'IOC_RMA_PDR'
    elif 'Configuration' in subject:
        return 'Configuration'
    elif 'Mantis' in subject:
        return 'Mantis'
    elif 'Jira' in subject:
        return 'Jira'
    elif 'MediaWiki' in subject:
        return 'MediaWiki'
    elif 'PDM2' in subject:
        return 'PDM2'
    elif 'SSRS' in subject:
        return 'SSRS'
    elif 'Sales_Portal' in subject:
        return 'Sales_Portal'
    elif 'GitLab' in subject:
        return 'GitLab'
    elif 'ReverseProxy' in subject:
        return 'ReverseProxy'
    elif 'PLM' in subject:
        return 'PLM'
    else:
        return 'ELSE'

def save_to_csv(emails_content, csv_filename):
    # Save email content to a CSV file.
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Subject', 'Date', 'Start Time', 'End Time', 'Size', 'Read', 'Transferred', 'Duration']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for email_content in emails_content:
            writer.writerow(email_content)

def main():
    # Login to the IMAP server
    imap_server = login_to_imap_server(imap_server_url, imap_username, imap_password)
    
    # Fetch emails from the specified mailbox folder
    email_ids = fetch_emails(imap_server, mailbox_folder)
    
    # Initialize a list to store email content
    emails_content = []

    # Iterate through each email in the folder
    for email_uid in email_ids:
        try:
            print(f"Fetching email with UID: {email_uid}...")
            # Fetch the email using its UID
            status, email_data = imap_server.fetch(email_uid, '(RFC822)')
            if status != 'OK':
                print(f"Failed to fetch email with UID {email_uid}.")
                continue
            
            # Parse the email data
            subject, date, body = parse_email_content(email_data[0][1])

            # Get required information from the email body
            start_time, end_time, size, read, transferred, duration = extract_information_from_body(body)

            # Determine the value for the 'Subject' column
            subject_value = determine_subject(subject)

            # Append email content to the list
            emails_content.append({
                'Subject': subject_value,
                'Date': date,
                'Start Time': start_time,
                'End Time': end_time,
                'Size': size,
                'Read': read,
                'Transferred': transferred,
                'Duration': duration
            })
        except Exception as e:
            print(f"Error processing email with UID {email_uid}: {e}")

    # Save email content to a CSV file with the same name as the mailbox folder
    csv_filename = f"{mailbox_folder.replace('/', '_')}.csv"
    save_to_csv(emails_content, csv_filename)

    # Print a message to confirm that the CSV file has been created
    print(f"Email content saved to {csv_filename}")

    # Don't forget to close the connection when done
    imap_server.logout()

if __name__ == "__main__":
    main()

