import os
from flask import Flask, jsonify
import redis

app = Flask(__name__)
cache = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    socket_connect_timeout=2,
)


@app.route("/")
def home():
    try:
        count = cache.incr("visits")
        return f"Hello! You are visitor number {count} (v1)\n"
    except redis.exceptions.RedisError:
        return jsonify(error="Redis not reachable"), 503


@app.route("/health")
def health():
    return jsonify(status="UP")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
