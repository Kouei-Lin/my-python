from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

user_list = []

class User(Resource):
    def get(self, username):
        for user in user_list:
            if user['username'] == username:
                return user
        return {'username': None}, 404

    def post(self, username):
        user = {
            'username': username,
            'email': request.get_json().get('email')
        }
        user_list.append(user)
        return user

    def delete(self, username):
        for ind, user in enumerate(user_list):
            if user['username'] == username:
                deleted_user = user_list.pop(ind)
                return {'note': 'successfully delete'}

    def put(self, username):
        for user in user_list:
            if user['username'] == username:
                user['email'] = request.get_json().get('email')
                return user
        return {'username': None}, 404

class UserList(Resource):
    """List"""
    def get(self):
        return {'user_list': user_list}

api.add_resource(User, '/api/user/<string:username>')
api.add_resource(UserList, '/api/users')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

