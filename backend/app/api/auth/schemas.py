
from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterResponse(BaseModel):
    id: int
    email: EmailStr

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str

