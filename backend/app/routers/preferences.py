from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.preference import UserPreference
from app.schemas.preference import UserPreferenceUpdate, UserPreferenceResponse

router = APIRouter(prefix="/api/preferences", tags=["Preferencias de Usuario"])


@router.get("", response_model=UserPreferenceResponse)
def get_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Consulta las preferencias del usuario autenticado actual."""
    pref = db.query(UserPreference).filter(UserPreference.user_id == current_user.id).first()
    if not pref:
        # Fallback si no existen preferencias asociadas
        pref = UserPreference(user_id=current_user.id)
        db.add(pref)
        db.commit()
        db.refresh(pref)
    return pref


@router.put("", response_model=UserPreferenceResponse)
def update_preferences(
    pref_in: UserPreferenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualiza el estilo de comunicación y nivel de franqueza preferido por el usuario."""
    pref = db.query(UserPreference).filter(UserPreference.user_id == current_user.id).first()
    if not pref:
        pref = UserPreference(user_id=current_user.id)
        db.add(pref)

    pref.communication_style = pref_in.communication_style
    pref.directness_level = pref_in.directness_level
    pref.preferred_response_length = pref_in.preferred_response_length

    db.commit()
    db.refresh(pref)
    return pref
