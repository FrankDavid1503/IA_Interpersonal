def get_auth_token(client, email: str, name: str):
    register_payload = {"name": name, "email": email, "password": "Password123!"}
    client.post("/api/auth/register", json=register_payload)
    login_res = client.post("/api/auth/login/json", json={"email": email, "password": "Password123!"})
    return login_res.json()["access_token"]


def test_create_and_list_situations(client):
    token = get_auth_token(client, "user1@example.com", "User One")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "input_text": "Mi amigo está triste por la pérdida de su mascota.",
        "relationship_type": "amigo",
        "objective": "Saber qué decirle"
    }

    # 1. Crear situación
    create_res = client.post("/api/situations", json=payload, headers=headers)
    assert create_res.status_code == 201
    sit_data = create_res.json()
    assert sit_data["input_text"] == payload["input_text"]
    assert "id" in sit_data

    # 2. Listar situaciones
    list_res = client.get("/api/situations", headers=headers)
    assert list_res.status_code == 200
    items = list_res.json()
    assert len(items) == 1
    assert items[0]["id"] == sit_data["id"]


def test_user_data_isolation(client):
    # User A crea una situación
    token_a = get_auth_token(client, "usera@example.com", "User A")
    headers_a = {"Authorization": f"Bearer {token_a}"}
    create_res = client.post(
        "/api/situations",
        json={
            "input_text": "Discusión con mi hermano por un malentendido.",
            "relationship_type": "familiar",
            "objective": "Aclarar las cosas"
        },
        headers=headers_a
    )
    situation_id = create_res.json()["id"]

    # User B intenta acceder a la situación de User A
    token_b = get_auth_token(client, "userb@example.com", "User B")
    headers_b = {"Authorization": f"Bearer {token_b}"}

    get_res = client.get(f"/api/situations/{situation_id}", headers=headers_b)
    assert get_res.status_code == 403
    assert "no tienes autorización" in get_res.json()["detail"].lower()

    # User B intenta eliminar la situación de User A
    del_res = client.delete(f"/api/situations/{situation_id}", headers=headers_b)
    assert del_res.status_code == 403

    # User A elimina su propia situación
    del_a_res = client.delete(f"/api/situations/{situation_id}", headers=headers_a)
    assert del_a_res.status_code == 200
