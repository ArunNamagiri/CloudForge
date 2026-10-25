import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import app


def test_home():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert response.json["application"] == "CloudForge"


def test_health():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_readiness():
    response = app.test_client().get("/ready")
    assert response.status_code == 200
    assert response.json["status"] == "ready"


def test_info():
    response = app.test_client().get("/api/v1/info")
    assert response.status_code == 200
    assert response.json["version"] == "1.0.0"
