# tests/test_lists.py
"""Tests for list-service API endpoints."""


def test_get_public_lists(app_client):
    """Test getting public lists."""
    response = app_client.get("/api/lists/public")
    assert response.status_code == 200
    data = response.json()
    assert "lists" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data


def test_get_public_lists_with_pagination(app_client):
    """Test getting public lists with pagination params."""
    response = app_client.get("/api/lists/public?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["page_size"] == 10
