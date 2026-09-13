import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class Situation(Base):
    __tablename__ = "situations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    input_text = Column(Text, nullable=False)
    relationship_type = Column(String(50), nullable=False) # amigo, familiar, compañero, pareja, etc.
    objective = Column(String(255), nullable=False) # ej: "saber qué decirle"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    user = relationship("User", back_populates="situations")
    analyses = relationship("Analysis", back_populates="situation", cascade="all, delete-orphan")
    safety_events = relationship("SafetyEvent", back_populates="situation", cascade="all, delete-orphan")
