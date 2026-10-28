import sys
from pathlib import Path

from flask.testing import FlaskClient

# Make the logmind-ai directory importable.
PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from api import app


def test_home_endpoint():
    app.config["TESTING"] = True
    client: FlaskClient = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.json["application"] == "LogMind AI"
    assert response.json["status"] == "running"


def test_health_endpoint():
    app.config["TESTING"] = True
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_analyze_endpoint(monkeypatch):
    app.config["TESTING"] = True
    client = app.test_client()

    def fake_detect_errors(file_path):
        return {
            "total_errors": 3,
            "unique_errors": 2,
            "error_messages": [
                "Database connection failed",
                "Database connection timeout",
            ],
            "error_counts": {
                "Database connection failed": 2,
                "Database connection timeout": 1,
            },
            "repeated_errors": {
                "Database connection failed": 2,
            },
        }

    def fake_ai_analysis(error_messages):
        assert len(error_messages) == 2
        return "Example troubleshooting analysis"

    monkeypatch.setattr(
        "api.detect_repeated_errors",
        fake_detect_errors,
    )
    monkeypatch.setattr(
        "api.analyze_errors",
        fake_ai_analysis,
    )

    response = client.get("/api/v1/analyze")

    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert response.json["total_errors"] == 3
    assert response.json["unique_errors"] == 2
    assert response.json["ai_analysis"] == "Example troubleshooting analysis"