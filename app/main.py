from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import Base, engine
from app.routers import chat, export, ideas, libraries, system

app = FastAPI(title=settings.app_name)

Base.metadata.create_all(bind=engine)

app.include_router(system.router)
app.include_router(libraries.router)
app.include_router(ideas.router)
app.include_router(chat.router)
app.include_router(export.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def root() -> FileResponse:
    return FileResponse("app/static/index.html")
