from flask import Flask, request
import requests
import time

app = Flask(__name__)

@app.route("/")
def get_result():
    response = requests.get("http://localhost:5000")
    return response.json()

@app.route("/callback", methods = ['POST'])
def callback():
    webhook_value = request.json.get('value')
    job_id = request.json.get('id')
    print(f"recieved webhook notification of job {job_id} with value of {webhook_value}")
    return f"recieved webhook notification of job {job_id} with value of {webhook_value}", 200



if __name__ == "__main__":
    app.run(port=5001, debug=True)
