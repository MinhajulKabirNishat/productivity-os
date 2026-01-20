from fastapi import FastAPI
from app.database import engine
from sqlalchemy import text

app = FastAPI(title="Productivity OS API")

@app.get("/health")
def health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
