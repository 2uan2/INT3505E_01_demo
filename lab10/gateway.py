from flask import Flask, request, jsonify, redirect, make_response
import requests
import logging
import redis

app = Flask(__name__)
cache = redis.Redis(host="redis", port=6379)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

@app.before_request
def log_request():
    app.logger.info(f"{request.remote_addr} {request.method} {request.path}")
    cache.incr("total_request")

@app.errorhandler(Exception)
def err(e):
    app.logger.exception("Unhandled exception")
    return {"error": f"Server error {e}"}, 500

@app.route("/metrics")
def metrics():
    total = cache.get("total_request") or 0
    total = int(total)
    lines = [
        "# HELP http_requests_total Total number of requests",
        "# TYPE http_requests_total counter",
        f"http_requests_total {total}"
    ]
    return "\n".join(lines) + "\n", 200, {"Content-Type": "text/plain; version=0.0.4"}

# @app.route("/metrics")
# def metrics():
#     return generate_latest(), 200, {
#         "Content-Type": "text/plain; version=0.0.4"
#     }

@app.route("/user")
def user_service():
    response = requests.get("http://user_service:5001/")
    return response.text, response.status_code

@app.route("/counter")
def counter_service():
    response = requests.get("http://counter_service:5002")
    return response.text, response.status_code

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
