from fastapi import FastAPI
from app.database import engine, Base
from app.api.auth.routes import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Productivity OS API")

app.include_router(auth_router, prefix="/auth", tags=["Auth"])

@app.get("/")
def root():
    return {"status": "running"}
