import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models import (
    User,
    UserPreference,
    Situation,
    Analysis,
    AnalysisEmotion,
    Recommendation,
    SafetyEvent,
)

# Base de datos SQLite temporal en memoria para pruebas rápidas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def test_create_user_and_preference(db_session):
    user = User(
        name="Juan Pérez",
        email="juan@example.com",
        password_hash="hashed_secret"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.email == "juan@example.com"

    pref = UserPreference(
        user_id=user.id,
        communication_style="directo",
        directness_level="cuidadoso",
        preferred_response_length="corto"
    )
    db_session.add(pref)
    db_session.commit()
    db_session.refresh(pref)

    assert user.preferences is not None
    assert user.preferences.communication_style == "directo"


def test_full_analysis_workflow(db_session):
    # 1. Crear usuario
    user = User(name="Maria", email="maria@example.com", password_hash="hash123")
    db_session.add(user)
    db_session.commit()

    # 2. Crear situación
    situation = Situation(
        user_id=user.id,
        input_text="Mi amigo está triste por la pérdida de su mascota.",
        relationship_type="amigo",
        objective="Saber qué decirle"
    )
    db_session.add(situation)
    db_session.commit()
    db_session.refresh(situation)

    assert len(user.situations) == 1

    # 3. Crear análisis
    analysis = Analysis(
        situation_id=situation.id,
        context_summary="Pérdida de mascota",
        detected_emotion="Tristeza",
        sensitivity_level="medium",
        risk_level="low",
        recommendation="Escuchar y acompañar",
        suggested_response="Siento mucho tu pérdida...",
        model_name="mock-llm"
    )
    db_session.add(analysis)
    db_session.commit()
    db_session.refresh(analysis)

    # 4. Crear emociones secundarias
    emotion1 = AnalysisEmotion(analysis_id=analysis.id, emotion="Tristeza", confidence=0.9)
    emotion2 = AnalysisEmotion(analysis_id=analysis.id, emotion="Soledad", confidence=0.6)
    db_session.add_all([emotion1, emotion2])

    # 5. Crear recomendaciones / alternativas
    rec1 = Recommendation(
        analysis_id=analysis.id,
        title="Escuchar activamente",
        description="Acompañar en silencio y validar dolor",
        benefit="Sentimiento de apoyo",
        risk="Requiere tiempo",
        priority=1
    )
    db_session.add(rec1)
    db_session.commit()

    # 6. Evento de seguridad
    safety = SafetyEvent(
        situation_id=situation.id,
        risk_level="low",
        category="general",
        action_taken="Análisis de IA ejecutado normalmente"
    )
    db_session.add(safety)
    db_session.commit()

    # Verificaciones
    assert len(analysis.emotions) == 2
    assert len(analysis.recommendations) == 1
    assert len(situation.safety_events) == 1
    assert analysis.recommendations[0].title == "Escuchar activamente"
