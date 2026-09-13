import uuid
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.situation import SituationCreate, SituationResponse
from app.services.situation_service import (
    create_user_situation,
    get_user_situations,
    get_user_situation_by_id,
    delete_user_situation
)

router = APIRouter(prefix="/api/situations", tags=["Situaciones"])


@router.post("", response_model=SituationResponse, status_code=status.HTTP_201_CREATED)
def create_situation(
    situation_in: SituationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crea una nueva situación para el usuario autenticado."""
    return create_user_situation(db=db, user_id=current_user.id, situation_in=situation_in)


@router.get("", response_model=List[SituationResponse])
def list_situations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene el historial de situaciones del usuario autenticado."""
    return get_user_situations(db=db, user_id=current_user.id)


@router.get("/{situation_id}", response_model=SituationResponse)
def get_situation(
    situation_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Consulta una situación específica del usuario."""
    return get_user_situation_by_id(db=db, user_id=current_user.id, situation_id=situation_id)


@router.delete("/{situation_id}")
def delete_situation(
    situation_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Elimina una situación propia del usuario."""
    return delete_user_situation(db=db, user_id=current_user.id, situation_id=situation_id)
