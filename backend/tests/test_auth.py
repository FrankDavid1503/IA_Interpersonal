def test_register_user_success(client):
    payload = {
        "name": "Carlos Gomez",
        "email": "carlos@example.com",
        "password": "Password123!"
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "carlos@example.com"
    assert data["name"] == "Carlos Gomez"
    assert "id" in data
    assert "password" not in data


def test_register_duplicate_email(client):
    payload = {
        "name": "Carlos Gomez",
        "email": "carlos@example.com",
        "password": "Password123!"
    }
    client.post("/api/auth/register", json=payload)
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 400
    assert "registrado" in response.json()["detail"].lower()


def test_login_and_access_protected_me_route(client):
    # 1. Registrar usuario
    register_payload = {
        "name": "Ana Lopez",
        "email": "ana@example.com",
        "password": "SecurePassword123"
    }
    client.post("/api/auth/register", json=register_payload)

    # 2. Login con JSON
    login_payload = {
        "email": "ana@example.com",
        "password": "SecurePassword123"
    }
    login_res = client.post("/api/auth/login/json", json=login_payload)
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    token = token_data["access_token"]

    # 3. Acceder a /api/auth/me con token válido
    headers = {"Authorization": f"Bearer {token}"}
    me_res = client.get("/api/auth/me", headers=headers)
    assert me_res.status_code == 200
    me_data = me_res.json()
    assert me_data["email"] == "ana@example.com"
    assert me_data["name"] == "Ana Lopez"


def test_access_protected_route_without_token(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401
