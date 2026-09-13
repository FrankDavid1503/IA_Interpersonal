import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class SafetyEvent(Base):
    __tablename__ = "safety_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    situation_id = Column(UUID(as_uuid=True), ForeignKey("situations.id", ondelete="CASCADE"), index=True, nullable=False)
    risk_level = Column(String(20), nullable=False) # low, medium, high, critical
    category = Column(String(100), nullable=False) # autolesión, violencia, abuso, etc.
    action_taken = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    situation = relationship("Situation", back_populates="safety_events")
