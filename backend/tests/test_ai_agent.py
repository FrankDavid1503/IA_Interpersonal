from app.ai.agent import analyze_situation_with_llm
from app.ai.parser import parse_and_validate_llm_json, AIAnalysisSchema
from tests.test_situations import get_auth_token


def test_analyze_situation_with_llm_mock():
    analysis = analyze_situation_with_llm(
        input_text="Mi amigo perdió a su perrito.",
        relationship_type="amigo",
        objective="Apoyarlo"
    )
    assert isinstance(analysis, AIAnalysisSchema)
    assert len(analysis.detected_emotion) > 0
    assert len(analysis.alternatives) >= 2


def test_parse_json_from_llm():
    sample_json = """
    {
      "context_summary": "Pérdida de mascota",
      "detected_emotion": "Tristeza",
      "emotions": [{"emotion": "Tristeza", "confidence": 0.9}],
      "sensitivity_level": "medium",
      "risk_level": "low",
      "recommendation": "Escuchar",
      "suggested_response": "Siento mucho tu pérdida",
      "alternatives": [
        {
          "title": "Acompañar",
          "description": "Estar presente",
          "benefit": "Apoyo",
          "risk": "Ninguno",
          "priority": 1
        }
      ]
    }
    """
    res = parse_and_validate_llm_json(sample_json)
    assert res.detected_emotion == "Tristeza"
    assert res.emotions[0].confidence == 0.9
    assert res.alternatives[0].title == "Acompañar"


def test_post_analyze_situation_e2e(client):
    token = get_auth_token(client, "aitest@example.com", "AI User")
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Crear situación
    create_sit = client.post(
        "/api/situations",
        json={
            "input_text": "Discusión con un compañero sobre la entrega del proyecto.",
            "relationship_type": "compañero",
            "objective": "Llegar a un acuerdo pacífico"
        },
        headers=headers
    )
    sit_id = create_sit.json()["id"]

    # 2. Ejecutar análisis de IA
    analyze_res = client.post(f"/api/situations/{sit_id}/analyze", headers=headers)
    assert analyze_res.status_code == 201
    data = analyze_res.json()
    assert data["situation_id"] == sit_id
    assert len(data["detected_emotion"]) > 0
    assert len(data["emotions"]) > 0
    assert len(data["recommendations"]) > 0

    # 3. Consultar el análisis guardado por ID
    analysis_id = data["id"]
    get_analysis = client.get(f"/api/analyses/{analysis_id}", headers=headers)
    assert get_analysis.status_code == 200
    assert get_analysis.json()["id"] == analysis_id


def test_post_analyze_high_risk_situation(client):
    token = get_auth_token(client, "risktest@example.com", "Risk User")
    headers = {"Authorization": f"Bearer {token}"}

    # Crear situación con palabra de crisis
    create_sit = client.post(
        "/api/situations",
        json={
            "input_text": "Quiero desaparecer para siempre y quitarme la vida.",
            "relationship_type": "personal",
            "objective": "no sé"
        },
        headers=headers
    )
    sit_id = create_sit.json()["id"]

    # Ejecutar análisis
    analyze_res = client.post(f"/api/situations/{sit_id}/analyze", headers=headers)
    assert analyze_res.status_code == 201
    data = analyze_res.json()
    assert data["risk_level"] in ["high", "critical"]
    assert data["safety_warning"] is not None
    assert "reemplaza la atención de un profesional" in data["safety_warning"]
