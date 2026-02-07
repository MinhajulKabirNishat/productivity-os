from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.database import get_db
from app.models.user import User
from app.models.token_blacklist import TokenBlacklist
from app.api.auth.schemas import RegisterRequest, RegisterResponse, TokenResponse, UserUpdate, PasswordUpdate
from app.api.auth.utils import create_user, authenticate_user, verify_password, hash_password
from app.core.dependencies import get_current_user 
from app.core.security import create_access_token, create_refresh_token
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=RegisterResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    return create_user(db, payload.email, payload.password)

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access = create_access_token({"sub": str(user.id)})
    refresh = create_refresh_token({"sub": str(user.id)})
    return {"access_token": access, "refresh_token": refresh}

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token")
        if db.query(TokenBlacklist).filter_by(token=refresh_token).first():
            raise HTTPException(status_code=401, detail="Token revoked")
        
        user_id = payload.get("sub")
        return {
            "access_token": create_access_token({"sub": user_id}),
            "refresh_token": create_refresh_token({"sub": user_id})
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    blacklisted = TokenBlacklist(token=refresh_token)
    db.add(blacklisted)
    db.commit()
    return {"message": "Logged out successfully"}

@router.get("/users/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/users/me")
def update_me(data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if data.name: current_user.name = data.name
    if data.email: current_user.email = data.email
    db.commit()
    db.refresh(current_user)
    return {"message": "Profile updated successfully"}

@router.patch("/users/password")
def change_password(data: PasswordUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not verify_password(data.current_password, current_user.password):
        raise HTTPException(status_code=400, detail="Wrong current password")
    current_user.password = hash_password(data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

@router.delete("/users/me")
def delete_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.delete(current_user)
    db.commit()
    return {"message": "User deleted successfully"}