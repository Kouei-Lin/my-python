from flask import Flask, request

app = Flask(__name__)

@app.route('/api/add', methods=['POST'])
def add_numbers():
    data = request.get_json()
    if 'num1' in data and 'num2' in data:
        num1 = data['num1']
        num2 = data['num2']
        result = num1 + num2
        return {'result': result}  # Directly returning dictionary
    else:
        return {'error': 'Missing parameters'}, 400  # Directly returning dictionary

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

