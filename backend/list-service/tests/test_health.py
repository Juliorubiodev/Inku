# tests/test_health.py
"""Tests for list-service health endpoint."""


def test_health(app_client):
    """Test health endpoint returns OK status."""
    response = app_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "list-service"


def test_root(app_client):
    """Test root endpoint returns API info."""
    response = app_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "List Service" in data["message"]
