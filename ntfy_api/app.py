from flask import Flask, request, jsonify
from apprise import Apprise
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize Apprise
apobj = Apprise()

# Add notification service from environment variable
ntfy_url = os.getenv('NTFY_URL')
if ntfy_url:
    apobj.add(ntfy_url)
else:
    raise ValueError("NTFY_URL is not defined in the .env file")

# Route to receive messages via POST
@app.route('/api/ntfy', methods=['POST'])
def send_notification():
    data = request.get_json()
    if 'message' in data:
        message = data['message']
        
        # Send notification using Apprise
        apobj.notify(body=message)
        
        return jsonify({'success': True, 'message': 'Notification sent successfully'})
    else:
        return jsonify({'success': False, 'error': 'Message not provided'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

