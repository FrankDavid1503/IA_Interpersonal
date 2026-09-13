import uuid
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.situation import Situation
from app.schemas.situation import SituationCreate


def create_user_situation(db: Session, user_id: uuid.UUID, situation_in: SituationCreate) -> Situation:
    """Crea una nueva situación asociada al usuario autenticado."""
    situation = Situation(
        user_id=user_id,
        input_text=situation_in.input_text,
        relationship_type=situation_in.relationship_type,
        objective=situation_in.objective
    )
    db.add(situation)
    db.commit()
    db.refresh(situation)
    return situation


def get_user_situations(db: Session, user_id: uuid.UUID) -> List[Situation]:
    """Retorna la lista de situaciones pertenecientes al usuario."""
    return db.query(Situation).filter(Situation.user_id == user_id).order_by(Situation.created_at.desc()).all()


def get_user_situation_by_id(db: Session, user_id: uuid.UUID, situation_id: uuid.UUID) -> Situation:
    """Consulta una situación verificando el aislamiento por usuario."""
    situation = db.query(Situation).filter(Situation.id == situation_id).first()
    if not situation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La situación solicitada no existe."
        )
    if situation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes autorización para acceder a esta situación."
        )
    return situation


def delete_user_situation(db: Session, user_id: uuid.UUID, situation_id: uuid.UUID) -> dict:
    """Elimina una situación verificando la propiedad del usuario."""
    situation = get_user_situation_by_id(db=db, user_id=user_id, situation_id=situation_id)
    db.delete(situation)
    db.commit()
    return {"message": "Situación eliminada correctamente.", "id": str(situation_id)}
