import os
import csv
import imaplib
import sqlite3
from dotenv import load_dotenv
from email import message_from_bytes
from bs4 import BeautifulSoup
from datetime import datetime

class EmailIMAPClient:
    def __init__(self, imap_server_url, username, password):
        self.imap_server_url = imap_server_url
        self.username = username
        self.password = password
        self.imap_server = None
    
    def login(self):
        self.imap_server = imaplib.IMAP4(self.imap_server_url)
        self.imap_server.login(self.username, self.password)
    
    def fetch_emails(self, mailbox_folder):
        status, data = self.imap_server.select(mailbox_folder)
        if status != 'OK':
            raise ValueError(f"Failed to select mailbox folder {mailbox_folder}.")
        
        status, email_ids = self.imap_server.search(None, 'ALL')
        if status != 'OK':
            raise ValueError("Failed to search for emails.")
        
        return email_ids[0].split()
    
    def logout(self):
        if self.imap_server:
            self.imap_server.logout()

class EmailContentExtractor:
    @staticmethod
    def parse_email_content(email_data):
        email_message = message_from_bytes(email_data)
        subject = email_message['Subject']
        date_str = email_message['Date']
        date = datetime.strptime(date_str, '%d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d')
        body = email_message.get_payload(decode=True).decode()
        return subject, date, body
    
    @staticmethod
    def extract_information_from_body(body):
        soup = BeautifulSoup(body, 'html.parser')
        fields = ['Start time', 'End time', 'Total size', 'Data read', 'Transferred', 'Duration']
        
        extracted_info = {}
        for field in fields:
            tag = soup.find('td', string=field)
            value = tag.find_next_sibling('td').text.strip() if tag else 'N/A'
            extracted_info[field.lower().replace(' ', '_')] = value
        
        return extracted_info['start_time'], extracted_info['end_time'], extracted_info['total_size'], \
               extracted_info['data_read'], extracted_info['transferred'], extracted_info['duration']
    
    @staticmethod
    def determine_subject(subject):
        subjects = {
            'MAWF': 'MAWF',
            'SECOM': 'SECOM',
            'NAS': 'NAS',
            'IOC_RMA_PDR': 'IOC_RMA_PDR',
            'Configuration': 'Configuration',
            'Mantis': 'Mantis',
            'Jira': 'Jira',
            'MediaWiki': 'MediaWiki',
            'PDM2': 'PDM2',
            'SSRS': 'SSRS',
            'Sales_Portal': 'Sales_Portal',
            'GitLab': 'GitLab',
            'ReverseProxy': 'ReverseProxy',
            'PLM': 'PLM'
        }
        for keyword, label in subjects.items():
            if keyword in subject:
                return label
        return 'ELSE'

class EmailDataSaver:
    def __init__(self, emails_content):
        self.emails_content = emails_content
    
    def save_to_csv(self, csv_filename):
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Subject', 'Date', 'Size', 'Read', 'Transferred', 'Duration']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.emails_content)
    
    def save_to_sqlite(self, db_filename):
        with sqlite3.connect(db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS emails (
                    subject TEXT,
                    date TEXT,
                    size TEXT,
                    read TEXT,
                    transferred TEXT,
                    duration TEXT
                )
            ''')
            for email in self.emails_content:
                cursor.execute('''
                    INSERT INTO emails (subject, date, size, read, transferred, duration)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    email['Subject'],
                    email['Date'],
                    email['Size'],
                    email['Read'],
                    email['Transferred'],
                    email['Duration']
                ))

def convert_to_gb_or_mb(value_with_unit):
    value, unit = value_with_unit.split()
    value = float(value)
    if unit == 'GB':
        return f"{value:.2f} GB"
    else:
        return f"{value / 1000:.2f} GB"

def main():
    load_dotenv()
    
    imap_server_url = os.getenv('IMAP_SERVER_URL')
    imap_username = os.getenv('IMAP_USERNAME')
    imap_password = os.getenv('IMAP_PASSWORD')
    mailbox_folder = os.getenv('MAIL_FOLDER')
    
    client = EmailIMAPClient(imap_server_url, imap_username, imap_password)
    client.login()
    
    email_ids = client.fetch_emails(mailbox_folder)
    
    extractor = EmailContentExtractor()
    emails_content = []
    
    # Fetch emails and parse them
    for email_uid in email_ids:
        try:
            print(f"Fetching email with UID: {email_uid}...")
            status, email_data = client.imap_server.fetch(email_uid, '(RFC822)')
            if status != 'OK':
                print(f"Failed to fetch email with UID {email_uid}.")
                continue
            
            subject, date, body = extractor.parse_email_content(email_data[0][1])
            start_time, end_time, size, read, transferred, duration = extractor.extract_information_from_body(body)
            
            subject_value = extractor.determine_subject(subject)
            size_value = convert_to_gb_or_mb(size)
            read_value = convert_to_gb_or_mb(read)
            transferred_value = convert_to_gb_or_mb(transferred)
            
            email_info = {
                'Subject': subject_value,
                'Date': date,
                'Size': size_value,
                'Read': read_value,
                'Transferred': transferred_value,
                'Duration': duration
            }
            emails_content.append(email_info)
        except Exception as e:
            print(f"Error processing email with UID {email_uid}: {e}")
    
    # Close the connection to the IMAP server
    client.logout()
    
    # Save parsed email content to SQLite database
    db_filename = f"{mailbox_folder.replace('/', '_')}.db"
    data_saver = EmailDataSaver(emails_content)
    data_saver.save_to_sqlite(db_filename)
    print(f"Email content saved to {db_filename}")

if __name__ == "__main__":
    main()

