from flask import Flask
from random import randint
import time
import threading

app = Flask(__name__)
counter = 0

tasks = {}

def long_ahh_task(cur):
    print("not again...")
    time.sleep(10)
    tasks[str(cur)] = randint(1, 10)
    print(tasks)
    print("long task finished...")

@app.route("/")
def queue_job():
    global counter
    threading.Thread(target=long_ahh_task, args=[counter]).start()
    counter += 1
    return {"status": "queued", "id": counter-1}

@app.route("/<task_id>")
def get(task_id: int):
    try: 
        value = tasks[str(task_id)]
        return {"status": "done", "value": value}
    except KeyError:
        return {"status": 'cooking'}

if __name__ == '__main__':
    app.run(debug=True)
