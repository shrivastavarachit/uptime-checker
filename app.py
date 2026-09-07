import time
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/check")
def check():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "url query parameter is required"}), 400

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    start = time.time()
    try:
        resp = requests.get(url, timeout=5)
        latency_ms = round((time.time() - start) * 1000, 2)
        return jsonify({
            "url": url,
            "status": "up" if resp.status_code < 400 else "down",
            "http_code": resp.status_code,
            "latency_ms": latency_ms,
        }), 200
    except requests.exceptions.RequestException:
        latency_ms = round((time.time() - start) * 1000, 2)
        return jsonify({
            "url": url,
            "status": "down",
            "error": str(err),
            "latency_ms": latency_ms,
        }), 200


if __name__ == "__main__":
    app.run(port=8080)