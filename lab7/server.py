from flask import Flask, request
import requests
import base64

app = Flask(__name__)

users = []

@app.route("/register", methods=['POST'])
def register():
    try: 
        username = request.json['username']
        password = request.json['password']
        if username not in [user['username'] for user in users]:
            new_user = {
                'username': username,
                'password': password
            }
            users.append(new_user)
            return {'message': 'done'}, 201
        else: 
            return {'message': 'username unavailable'}, 409
    except:
        return {'message': 'something went wrong'}, 500

# @app.route("/login", methods=['POST'])
# def login():
#     try:
#         username = request.json['username']
#         password = request.json['password']
#         if username not in [user['username'] for user in users]:
#             return {'message': 'no user with that username'}, 404


    
@app.route('/public')
def public_route():
    return '<h1>hello world </h1>'

@app.route("/private")
def private_route():
    try:
        # username = request.json['username']
        # password = request.json['password']
        print(request.headers.get('Authorization'))
        auth = request.headers.get('Authorization')
        base64_string = auth.split("Basic")[1].strip()
        print('string is ', base64_string)
        decoded_data = base64.b64decode(base64_string)
        [username, password] = decoded_data.decode('utf-8').split(':')
        print('username:', username)
        print(password)
        if username not in [user['username'] for user in users]:
            return {'message': 'no user with that username'}, 404
        for user in users:
            if username == user['username'] and password == user['password']:
                return "secret content"

        return {'message': 'wrong credentials'}, 401
    except AttributeError as e:
        return {'message': 'missing Authorization or something'}, 400
    except Exception as e:
        return {'message': str(e)}, 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
