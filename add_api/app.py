from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/add', methods=['POST'])
def add_numbers():
    data = request.get_json()
    if 'num1' in data and 'num2' in data:
        num1 = data['num1']
        num2 = data['num2']
        result = num1 + num2
        return jsonify({'result': result})
    else:
        return jsonify({'error': 'Missing parameters'}), 400

if __name__ == '__main__':
    app.run(debug=True)

