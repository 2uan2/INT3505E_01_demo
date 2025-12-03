from flask import Flask, request
from random import randint
import time
import threading
import requests

app = Flask(__name__)
counter = 0

tasks = {}
webhook = ''

def long_ahh_task(cur):
    print("not again...")
    time.sleep(10)
    tasks[str(cur)] = randint(1, 10)
    print(tasks)
    print("long task finished...")
    print("calling webhook to push notification")
    data = {
        'id': cur,
        'value': tasks[str(cur)]
    }
    requests.post(webhook, json=data)

@app.route("/")
def queue_job():
    global counter
    threading.Thread(target=long_ahh_task, args=[counter]).start()
    counter += 1
    return {"status": "queued", "id": counter-1}

@app.route("/webhook/", methods=['POST'])
def register_webhook():
    global webhook
    print('content of request is')
    print(request.json)
    webhook = request.json.get('callback')
    return f'webhook registered as {webhook}\n'

if __name__ == '__main__':
    app.run(debug=True)
