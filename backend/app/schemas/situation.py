from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class SituationCreate(BaseModel):
    input_text: str
    relationship_type: str
    objective: str


class SituationResponse(BaseModel):
    id: UUID
    user_id: UUID
    input_text: str
    relationship_type: str
    objective: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
