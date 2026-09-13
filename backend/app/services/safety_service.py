import uuid
from sqlalchemy.orm import Session

from app.models.safety_event import SafetyEvent
from app.ai.safety import evaluate_safety, SafetyResult


def check_and_record_safety(db: Session, situation_id: uuid.UUID, input_text: str) -> SafetyResult:
    """Evalúa la seguridad del texto y registra el evento en la base de datos si es necesario."""
    result = evaluate_safety(input_text)

    # Registrar evento en safety_events
    safety_event = SafetyEvent(
        situation_id=situation_id,
        risk_level=result.risk_level,
        category=result.category,
        action_taken=result.action_taken
    )
    db.add(safety_event)
    db.commit()

    return result
