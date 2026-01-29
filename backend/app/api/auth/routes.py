from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.auth.schemas import RegisterRequest, RegisterResponse, TokenResponse
from app.api.auth.utils import create_user, authenticate_user
from app.models.user import User
from app.core.security import create_access_token

router = APIRouter()

@router.post("/register", response_model=RegisterResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
   
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )

   
    user = create_user(db, payload.email, payload.password)
    return user

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login using Form Data (required for Swagger UI 'Authorize' button).
    OAuth2 uses 'username' as the field name even if you type an email.
    """
    
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    
    token = create_access_token({"sub": str(user.id)})
    
    return {"access_token": token, "token_type": "bearer"}