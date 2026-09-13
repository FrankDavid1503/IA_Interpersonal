import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class EmotionResponse(BaseModel):
    id: uuid.UUID
    emotion: str
    confidence: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RecommendationResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    benefit: Optional[str] = None
    risk: Optional[str] = None
    priority: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnalysisResponse(BaseModel):
    id: uuid.UUID
    situation_id: uuid.UUID
    context_summary: str
    detected_emotion: str
    sensitivity_level: str
    risk_level: str
    recommendation: str
    suggested_response: str
    model_name: str
    created_at: datetime
    emotions: List[EmotionResponse] = []
    recommendations: List[RecommendationResponse] = []
    safety_warning: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
