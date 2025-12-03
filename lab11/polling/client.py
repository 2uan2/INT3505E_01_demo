from flask import Flask
import requests
import time

app = Flask(__name__)

@app.route("/")
def get_result():
    response = requests.get("http://localhost:5000")
    id = response.json()['id']
    while response.json()['status'] != 'done':
        time.sleep(3)
        print(f"polling again for job id {id}")
        response: requests.Response = requests.get(f"http://localhost:5000/{id}")
    return response.json()

if __name__ == "__main__":
    app.run(port=5001, debug=True)
