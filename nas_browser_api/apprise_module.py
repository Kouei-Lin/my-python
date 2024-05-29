import os
from apprise import Apprise
from dotenv import load_dotenv

load_dotenv()

class NotificationManager:
    def __init__(self):
        self.notification_url = os.getenv("NOTIFICATION_URL")
        self.apprise = Apprise()
        if self.notification_url:
            self.apprise.add(self.notification_url)
        else:
            print("Notification URL not found in environment variables.")

    def send_notification(self, message):
        if self.notification_url:
            self.apprise.notify(body=message)
            print("Notification sent successfully.")
        else:
            print("Notification URL not set. Notification not sent.")

# Example usage:
# notification_manager = NotificationManager()
# notification_manager.send_notification("Test notification message.")

