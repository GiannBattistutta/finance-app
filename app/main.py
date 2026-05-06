from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import engine
from app import models
from app.routes import auth, transactions
import os

app = FastAPI(
    title="Finance API",
    description="Personal finance management API",
    version="1.0.0"
)

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(transactions.router)

frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def index():
    return FileResponse(os.path.join(frontend_path, "index.html"))