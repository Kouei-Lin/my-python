from flask import Flask, jsonify
import psutil

app = Flask(__name__)

@app.route('/api/disk-usage', methods=['GET'])
def get_disk_usage():
    disk_usage = psutil.disk_usage('/')
    return jsonify({
        'total': disk_usage.total,
        'used': disk_usage.used,
        'free': disk_usage.free
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

