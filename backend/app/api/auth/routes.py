from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.database import get_db
from app.models.user import User
from app.models.token_blacklist import TokenBlacklist
from app.api.auth.schemas import RegisterRequest, RegisterResponse, TokenResponse
from app.api.auth.utils import create_user, authenticate_user
from app.core.security import create_access_token, create_refresh_token
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=RegisterResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    return create_user(db, payload.email, payload.password)


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access = create_access_token({"sub": str(user.id)})
    refresh = create_refresh_token({"sub": str(user.id)})

    return {
        "access_token": access,
        "refresh_token": refresh
    }

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token")

      
        if db.query(TokenBlacklist).filter_by(token=refresh_token).first():
            raise HTTPException(status_code=401, detail="Token revoked")

        user_id = payload.get("sub")

        access = create_access_token({"sub": user_id})
        new_refresh = create_refresh_token({"sub": user_id})

        return {
            "access_token": access,
            "refresh_token": new_refresh
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    blacklisted = TokenBlacklist(token=refresh_token)
    db.add(blacklisted)
    db.commit()
    return {"message": "Logged out successfully"}
