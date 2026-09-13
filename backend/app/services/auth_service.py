from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.preference import UserPreference
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password, create_access_token


def register_new_user(db: Session, user_in: UserCreate) -> User:
    """Registra un nuevo usuario y crea sus preferencias por defecto."""
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya se encuentra registrado."
        )

    # Crear usuario con contraseña cifrada
    db_user = User(
        name=user_in.name,
        email=user_in.email,
        password_hash=get_password_hash(user_in.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Crear preferencias iniciales por defecto
    preferences = UserPreference(user_id=db_user.id)
    db.add(preferences)
    db.commit()

    return db_user


def authenticate_user(db: Session, email: str, password: str) -> dict:
    """Autentica las credenciales y devuelve el token de acceso JWT."""
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
