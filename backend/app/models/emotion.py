import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class AnalysisEmotion(Base):
    __tablename__ = "analysis_emotions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("analyses.id", ondelete="CASCADE"), index=True, nullable=False)
    emotion = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False) # Valor entre 0.0 y 1.0
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    analysis = relationship("Analysis", back_populates="emotions")
