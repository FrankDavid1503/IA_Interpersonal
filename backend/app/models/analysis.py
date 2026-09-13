import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    situation_id = Column(UUID(as_uuid=True), ForeignKey("situations.id", ondelete="CASCADE"), index=True, nullable=False)
    context_summary = Column(Text, nullable=False)
    detected_emotion = Column(String(100), nullable=False)
    sensitivity_level = Column(String(20), default="low", nullable=False) # low, medium, high
    risk_level = Column(String(20), default="low", nullable=False) # low, medium, high
    recommendation = Column(Text, nullable=False)
    suggested_response = Column(Text, nullable=False)
    model_name = Column(String(100), default="mock-llm", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    situation = relationship("Situation", back_populates="analyses")
    emotions = relationship("AnalysisEmotion", back_populates="analysis", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="analysis", cascade="all, delete-orphan")
