from flask import Flask, request
from jose import jwt
import requests

app = Flask(__name__)
jwks = requests.get('http://192.168.100.102:8080/realms/test/protocol/openid-connect/certs').json()

@app.route('/')
def root():
    bearer = request.headers.get('Authorization')
    if not bearer:
        return 'no token??', 401

    token = bearer.split()[1]
    claims = jwt.decode(token, jwks, algorithms=["RS256"], audience="account")


    return f"secret for {claims.get('name')}\n"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
