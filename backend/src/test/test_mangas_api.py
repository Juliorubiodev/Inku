def test_list_mangas(app_client):
    r = app_client.get("/api/mangas")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    # Ahora el endpoint devuelve ["m1", ...]
    assert "m1" in data
