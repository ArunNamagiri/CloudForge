from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)

START_TIME = datetime.now(timezone.utc)


@app.get("/")
def home():
    return jsonify({
        "application": "CloudForge",
        "description": "Cloud-Native DevOps Automation Platform",
        "status": "running"
    }), 200


@app.get("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "CloudForge"
    }), 200


@app.get("/ready")
def readiness():
    return jsonify({
        "status": "ready",
        "application": "CloudForge"
    }), 200


@app.get("/api/v1/info")
def info():
    return jsonify({
        "application": "CloudForge",
        "version": "1.0.0",
        "environment": app.config.get("ENVIRONMENT", "development"),
        "started_at": START_TIME.isoformat()
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
