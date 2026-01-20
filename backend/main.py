from fastapi import FastAPI

app = FastAPI(title="Productivity OS API")

@app.get("/health")
def health_check():
    return {"status": "ok"}
