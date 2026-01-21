from fastapi import FastAPI
from sqlalchemy import text
from app.database import engine, Base
from app.models import user 
from app.api import auth

app = FastAPI(title="Productivity OS API")
app.include_router(auth.router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
