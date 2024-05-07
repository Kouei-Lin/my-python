import os
import csv
import imaplib
import sqlite3
from dotenv import load_dotenv
from email import message_from_bytes
from bs4 import BeautifulSoup
from datetime import datetime

class EmailClient:
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
    SUBJECT_KEYWORDS = {
        'MAWF': ['MAWF'],
        'SECOM': ['SECOM'],
        'NAS': ['NAS'],
        'IOC_RMA_PDR': ['IOC_RMA_PDR'],
        'Configuration': ['Configuration'],
        'Mantis': ['Mantis'],
        'Jira': ['Jira'],
        'MediaWiki': ['MediaWiki'],
        'PDM2': ['PDM2'],
        'SSRS': ['SSRS'],
        'Sales_Portal': ['Sales_Portal'],
        'GitLab': ['GitLab'],
        'ReverseProxy': ['ReverseProxy'],
        'PLM': ['PLM']
    }

    @staticmethod
    def determine_subject(subject):
        for key, keywords in EmailContentExtractor.SUBJECT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in subject:
                    return key
        return 'ELSE'
    
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
        start_time = soup.find('td', string='Start time').find_next_sibling('td').text.strip() if soup.find('td', string='Start time') else 'N/A'
        end_time = soup.find('td', string='End time').find_next_sibling('td').text.strip() if soup.find('td', string='End time') else 'N/A'
        size = soup.find('td', string='Total size').find_next_sibling('td').text.strip() if soup.find('td', string='Total size') else 'N/A'
        read = soup.find('td', string='Data read').find_next_sibling('td').text.strip() if soup.find('td', string='Data read') else 'N/A'
        transferred = soup.find('td', string='Transferred').find_next_sibling('td').text.strip() if soup.find('td', string='Transferred') else 'N/A'
        duration = soup.find('td', string='Duration').find_next_sibling('td').text.strip() if soup.find('td', string='Duration') else 'N/A'
        return start_time, end_time, size, read, transferred, duration

class EmailDataSaver:
    @staticmethod
    def save_to_csv(emails_content, csv_filename):
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Subject', 'Date', 'Start Time', 'End Time', 'Size', 'Read', 'Transferred', 'Duration']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for email_content in emails_content:
                writer.writerow(email_content)
    
    @staticmethod
    def save_to_sqlite(emails_content, db_filename):
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        
        # Create table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT,
                date TEXT,
                start_time TEXT,
                end_time TEXT,
                size TEXT,
                read TEXT,
                transferred TEXT,
                duration TEXT
            )
        ''')
        
        # Insert data
        for email_content in emails_content:
            cursor.execute('''
                INSERT INTO emails (subject, date, start_time, end_time, size, read, transferred, duration)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (email_content['Subject'], email_content['Date'], email_content['Start Time'], email_content['End Time'], email_content['Size'], email_content['Read'], email_content['Transferred'], email_content['Duration']))
        
        # Commit changes and close connection
        conn.commit()
        conn.close()

def main():
    load_dotenv()
    
    imap_server_url = os.getenv('IMAP_SERVER_URL')
    imap_username = os.getenv('IMAP_USERNAME')
    imap_password = os.getenv('IMAP_PASSWORD')
    mailbox_folder = os.getenv('MAIL_FOLDER')
    
    client = EmailClient(imap_server_url, imap_username, imap_password)
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
    
    # Close the connection to the IMAP server
    client.logout()
    
    # Save parsed email content to SQLite database
    db_filename = f"{mailbox_folder.replace('/', '_')}.db"
    EmailDataSaver.save_to_sqlite(emails_content, db_filename)
    print(f"Email content saved to {db_filename}")

if __name__ == "__main__":
    main()
