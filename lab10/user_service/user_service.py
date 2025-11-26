from flask import Flask
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

REQUESTS = Counter("http_request_total", "Total requests")

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": "text/plain; version=0.0.4"
    }

@app.route("/")
def index():
    return {"user": "bob", "role": "admin"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)
