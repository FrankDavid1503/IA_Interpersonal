import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserPreferenceUpdate(BaseModel):
    communication_style: str  # empático, directo, analítico
    directness_level: str     # directo, equilibrado, cuidadoso
    preferred_response_length: str # corto, medio, largo


class UserPreferenceResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    communication_style: str
    directness_level: str
    preferred_response_length: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
