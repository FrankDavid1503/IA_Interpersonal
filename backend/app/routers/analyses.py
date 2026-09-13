import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.analysis import AnalysisResponse
from app.services.analysis_service import run_analysis_for_situation, get_analysis_by_id

router = APIRouter(prefix="/api", tags=["Análisis de IA"])


@router.post("/situations/{situation_id}/analyze", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
def analyze_situation(
    situation_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Ejecuta el análisis del agente de IA para una situación específica del usuario."""
    return run_analysis_for_situation(db=db, user_id=current_user.id, situation_id=situation_id)


@router.get("/analyses/{analysis_id}", response_model=AnalysisResponse)
def read_analysis(
    analysis_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene el resultado completo de un análisis guardado previamente."""
    return get_analysis_by_id(db=db, user_id=current_user.id, analysis_id=analysis_id)
