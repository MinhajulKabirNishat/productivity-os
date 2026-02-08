from fastapi import FastAPI
from app.database import Base, engine
from app.api.auth.routes import router as auth_router
from app.api.tasks.routes import router as task_router

app = FastAPI(title="Productivity OS API")

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(task_router, prefix="/tasks", tags=["Tasks"])
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "status": "running",
        "message": "Welcome to the API"
    }
