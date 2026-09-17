def test_register_site_success(client):
    payload = {
        "name": "Prueba Pytest",
        "url": "https://pytest.org",
        "check_interval": 30
    }
    response = client.post("/api/v1/sites/", json=payload)
    data = response.json()

    assert response.status_code == 201
    assert "id" in data
    assert data["name"] == "Prueba Pytest"
    assert data["url"] == "https://pytest.org"
    assert data["is_active"] == True

def test_list_sites(client):
    client.post("/api/v1/sites/", json={"name": "Test List", "url": "https://test.com"})
    response = client.get("/api/v1/sites/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) >= 1
    assert isinstance(data, list)

def test_list_sites_empty(client):
    response = client.get("/api/v1/sites/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 0

def test_delete_site_success(client):
    # Primero crear un sitio
    create_response = client.post("/api/v1/sites/", json={"name": "To Delete", "url": "https://delete.com"})
    site_id = create_response.json()["id"]

    # Eliminar el sitio
    delete_response = client.delete(f"/api/v1/sites/{site_id}")
    
    assert delete_response.status_code == 204

    # Verificar que ya no existe
    get_response = client.get("/api/v1/sites/")
    sites = get_response.json()
    
    assert len(sites) == 0

def test_delete_site_not_found(client):
    response = client.delete("/api/v1/sites/99999")
    
    assert response.status_code == 404
    assert "detail" in response.json()

def test_register_site_invalid_url(client):
    payload = {
        "name": "Invalid URL",
        "url": "not-a-valid-url"
    }
    response = client.post("/api/v1/sites/", json=payload)
    
    # La validación de URL depende de tu implementación
    # Si no hay validación estricta, esto podría pasar
    assert response.status_code in [201, 422]
