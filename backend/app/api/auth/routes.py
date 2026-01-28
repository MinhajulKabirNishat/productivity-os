from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.auth.schemas import RegisterRequest, RegisterResponse
from app.api.auth.utils import create_user
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=RegisterResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = create_user(db, payload.email, payload.password)
    return user
