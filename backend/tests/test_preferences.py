from tests.test_situations import get_auth_token


def test_get_and_update_preferences(client):
    token = get_auth_token(client, "preftest@example.com", "Pref User")
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Obtener preferencias iniciales
    get_res = client.get("/api/preferences", headers=headers)
    assert get_res.status_code == 200
    pref = get_res.json()
    assert pref["communication_style"] == "empático"

    # 2. Actualizar preferencias
    update_payload = {
        "communication_style": "directo",
        "directness_level": "directo",
        "preferred_response_length": "corto"
    }
    put_res = client.put("/api/preferences", json=update_payload, headers=headers)
    assert put_res.status_code == 200
    updated = put_res.json()
    assert updated["communication_style"] == "directo"
    assert updated["directness_level"] == "directo"
    assert updated["preferred_response_length"] == "corto"
