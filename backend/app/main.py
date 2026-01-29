from fastapi import FastAPI, Depends, HTTPException, status
from app.database import engine, Base
from app.api.auth.routes import router as auth_router
from app.core.dependencies import get_current_user
from app.models.user import User


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Productivity OS API")

app.include_router(auth_router, prefix="/auth", tags=["Auth"])

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }
