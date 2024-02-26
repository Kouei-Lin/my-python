from flask import Flask
from datetime import datetime
import pytz
import json

app = Flask(__name__)

@app.route('/current_date_time', methods=['GET'])
def get_current_date_time():
    # Get the current time in UTC
    current_time_utc = datetime.now(pytz.utc)

    # Convert the UTC time to the desired timezone (UTC+8)
    target_timezone = pytz.timezone('Asia/Shanghai')  # UTC+8
    current_time_utc_8 = current_time_utc.astimezone(target_timezone)

    # Format the time as a string
    current_date_time = current_time_utc_8.strftime("%Y-%m-%d %H:%M:%S")

    # Create a dictionary to hold the response data
    response_data = {'current_date_time': current_date_time}

    # Serialize the response data to JSON format
    json_response = json.dumps(response_data)

    # Return the JSON response
    return json_response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

