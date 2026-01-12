# tests/test_health.py
"""Tests for auth-service health endpoint."""


def test_health(app_client):
    """Test health endpoint returns OK status."""
    response = app_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data
