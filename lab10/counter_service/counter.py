import time
from prometheus_client import Counter, generate_latest
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)
REQUESTS = Counter("http_request_total", "Total requests")

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": "text/plain; version=0.0.4"
    }

@app.route('/')
def hello():
    count = get_hit_count()
    return f'Hello World! I have been seen {count} times.\n'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
