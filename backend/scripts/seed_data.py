import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models import Base
from app.models.user import User
from app.models.preference import UserPreference
from app.models.situation import Situation
from app.models.analysis import Analysis
from app.models.emotion import AnalysisEmotion
from app.models.recommendation import Recommendation
from app.core.security import get_password_hash


def get_seed_engine():
    try:
        eng = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
        with eng.connect() as conn:
            pass
        return eng
    except Exception as e:
        print(f"[Seed Notice] No se pudo conectar a PostgreSQL ({settings.DATABASE_URL}). Usando SQLite local (nexo_dev.db): {e}")
        return create_engine("sqlite:///nexo_dev.db", connect_args={"check_same_thread": False})


def seed():
    print("🌱 Poblando base de datos de pruebas para NEXO...")
    engine = get_seed_engine()
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # 1. Crear usuario de prueba demo
        demo_user = db.query(User).filter(User.email == "demo@nexo.ai").first()
        if not demo_user:
            demo_user = User(
                name="Usuario Demo",
                email="demo@nexo.ai",
                password_hash=get_password_hash("Demo1234!")
            )
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)

            # Preferencias demo
            pref = UserPreference(
                user_id=demo_user.id,
                communication_style="empático",
                directness_level="equilibrado",
                preferred_response_length="medio"
            )
            db.add(pref)
            db.commit()
            print("👤 Usuario Demo creado: demo@nexo.ai / Demo1234!")

        # 2. Crear situación demo
        existing_sit = db.query(Situation).filter(Situation.user_id == demo_user.id).first()
        if not existing_sit:
            sit = Situation(
                user_id=demo_user.id,
                input_text="Mi amigo me dijo que falleció su perrito y no sé qué decirle.",
                relationship_type="amigo",
                objective="Ofrecer apoyo sincero sin resultar agobiante"
            )
            db.add(sit)
            db.commit()
            db.refresh(sit)

            # Crear análisis demo
            analysis = Analysis(
                situation_id=sit.id,
                context_summary="El usuario busca brindar consuelo a un amigo cercano ante el duelo por la pérdida de su mascota.",
                detected_emotion="Tristeza",
                sensitivity_level="medium",
                risk_level="low",
                recommendation="Acompañar con empatía, validar su dolor y ofrecer disponibilidad sin presionar por una respuesta inmediata.",
                suggested_response="Siento muchísimo lo de tu perrito. Sé lo especial e importante que era para ti. Si necesitas platicar o solo estar acompañado, sabes que aquí estoy para lo que necesites.",
                model_name="nexo-agent-v1"
            )
            db.add(analysis)
            db.commit()
            db.refresh(analysis)

            # Emociones
            e1 = AnalysisEmotion(analysis_id=analysis.id, emotion="Tristeza", confidence=0.92)
            e2 = AnalysisEmotion(analysis_id=analysis.id, emotion="Soledad", confidence=0.65)
            db.add_all([e1, e2])

            # Recomendaciones
            r1 = Recommendation(
                analysis_id=analysis.id,
                title="Escuchar y validar",
                description="Permitir que la persona exprese sus recuerdos y dolor sin dar consejos vacíos.",
                benefit="Brinda un espacio seguro de desahogo.",
                risk="Requiere tiempo y tolerancia al silencio.",
                priority=1
            )
            r2 = Recommendation(
                analysis_id=analysis.id,
                title="Ofrecer ayuda concreta",
                description="Llevar un detalle sencillo o acompañar en un paseo.",
                benefit="Muestra presencia activa.",
                risk="Puede preferir estar a solas inicialmente.",
                priority=2
            )
            db.add_all([r1, r2])
            db.commit()
            print("📝 Situación y análisis de prueba creados.")

        print("✅ ¡Población de datos semilla completada con éxito!")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
