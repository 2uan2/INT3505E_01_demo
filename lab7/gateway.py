from flask import Flask, request, jsonify, redirect, make_response
import requests
import base64
import uuid
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)
client_secret = 'dPhNMXSXaOA4ZbAAdjAGDvbc7Wyo0s7Q'
idp_url = 'http://192.168.100.102:8080'

sessions = {}

@app.route("/login", methods=['GET'])
def login():
    url = f'{idp_url}/realms/test/protocol/openid-connect/auth?client_id=my-flask-client&response_type=code&redirect_uri=http://localhost:5000/callback&scope=openid profile'

    response = make_response()
    response.headers["Location"] = url
    return response, 302

@app.route("/callback", methods=["GET", "POST"])
def callback():
    code = request.args.get('code', 'unknown')
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://localhost:5000/callback',
        'client_id': 'my-flask-client',
        'client_secret': client_secret
    }
    response = requests.request(
        method='POST',
        url=f'{idp_url}/realms/test/protocol/openid-connect/token',
        data=data
    )
    print("respnse in this case is: ", response.text)
    session_id = str(uuid.uuid4())
    sessions[session_id] = { 
        "access_token": response.json().get('access_token') ,
        "refresh_token": response.json().get('refresh_token')
    }

    response = make_response("login successfully")
    response.set_cookie("session_id", session_id)
    return response

@app.route("/api")
def api():
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in sessions:
        return {"message": "Unauthorized"}, 401
    access_token = sessions[session_id]['access_token']
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get("http://localhost:5002/", headers=headers)
    return response.text, response.status_code

@app.route("/logout", methods=['GET'])
def logout():
    try:
        session_id = request.cookies.get('session_id')

        refresh_token = sessions[session_id]['refresh_token']
        del sessions[str(session_id)]

        data = {
            "client_id": "my-flask-client",
            "client_secret": client_secret,
            "refresh_token": refresh_token
        }
        requests.post(
            url=f"{idp_url}/realms/test/protocol/openid-connect/logout", 
            data=data
        )

        response = make_response({"message": "Logged out locally"})
        response.delete_cookie("session_id")

        return response
    except:
        return {'message': 'something went wrong'}, 500

@app.route("/s")
def get_sessions():
    return sessions

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
