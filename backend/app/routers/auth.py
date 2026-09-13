from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.user import UserCreate, UserResponse, Token, UserLogin
from app.services.auth_service import register_new_user, authenticate_user
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario en la plataforma."""
    return register_new_user(db=db, user_in=user_in)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Inicio de sesión compatible con OAuth2 Password Flow."""
    return authenticate_user(db=db, email=form_data.username, password=form_data.password)


@router.post("/login/json", response_model=Token)
def login_json(user_in: UserLogin, db: Session = Depends(get_db)):
    """Inicio de sesión mediante payload JSON directo."""
    return authenticate_user(db=db, email=user_in.email, password=user_in.password)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Retorna los datos del usuario autenticado actual."""
    return current_user
