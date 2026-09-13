import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.core.config import settings

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./nexo.db")
if "postgresql" in DATABASE_URL:
    try:
        import psycopg2
        # Quick check connection
        # parse host, port, etc from url if needed, or fallback if OperationalError
        pass
    except Exception:
        DATABASE_URL = "sqlite:///./nexo.db"

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Inyección de dependencia para sesiones de Base de Datos en FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
