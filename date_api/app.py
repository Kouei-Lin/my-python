from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/current_date_time', methods=['GET'])
def get_current_date_time():
    current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({'current_date_time': current_date_time})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

