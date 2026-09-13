from app.ai.safety import evaluate_safety
from app.services.safety_service import check_and_record_safety
from app.models.situation import Situation
from app.models.user import User


def test_evaluate_safety_safe_text():
    text = "Mi amigo está triste porque falleció su perrito y no sé qué decirle."
    res = evaluate_safety(text)
    assert res.is_safe is True
    assert res.risk_level == "low"
    assert res.safety_message is None


def test_evaluate_safety_crisis_text():
    text = "Siento que ya no puedo más y estoy pensando en hacerme daño o quitarme la vida."
    res = evaluate_safety(text)
    assert res.is_safe is False
    assert res.risk_level in ["high", "critical"]
    assert res.category == "autolesion"
    assert "reemplaza la atención de un profesional" in res.safety_message


def test_check_and_record_safety_db(client):
    from conftest import TestingSessionLocal
    db = TestingSessionLocal()

    user = User(name="Test User", email="safetytest@example.com", password_hash="hash")
    db.add(user)
    db.commit()

    situation = Situation(
        user_id=user.id,
        input_text="Tengo mucho estrés laboral.",
        relationship_type="compañero",
        objective="Manejar el estrés"
    )
    db.add(situation)
    db.commit()

    res = check_and_record_safety(db, situation.id, situation.input_text)
    assert res.is_safe is True

    # Verificar que el evento quedó persistido
    assert len(situation.safety_events) == 1
    assert situation.safety_events[0].risk_level == "low"
    db.close()
