import json
from typing import List
from pydantic import BaseModel, Field, ValidationError


class EmotionDetail(BaseModel):
    emotion: str
    confidence: float = Field(ge=0.0, le=1.0)


class AlternativeDetail(BaseModel):
    title: str
    description: str
    benefit: str
    risk: str
    priority: int = Field(default=1, ge=1)


class AIAnalysisSchema(BaseModel):
    context_summary: str
    detected_emotion: str
    emotions: List[EmotionDetail]
    sensitivity_level: str = Field(default="medium", description="low, medium, high")
    risk_level: str = Field(default="low", description="low, medium, high")
    recommendation: str
    suggested_response: str
    alternatives: List[AlternativeDetail]


def parse_and_validate_llm_json(raw_text: str) -> AIAnalysisSchema:
    """Parsea una cadena JSON recibida del LLM y valida la estructura mediante Pydantic."""
    clean_text = raw_text.strip()
    if clean_text.startswith("```json"):
        clean_text = clean_text[7:]
    if clean_text.endswith("```"):
        clean_text = clean_text[:-3]
    clean_text = clean_text.strip()

    try:
        data = json.loads(clean_text)
        return AIAnalysisSchema.model_validate(data)
    except (json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"Error de parseo o validación en la respuesta del LLM: {str(e)}")
