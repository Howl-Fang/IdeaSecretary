from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.config import settings

Base = declarative_base()


def ensure_directories() -> None:
    for path in [settings.data_dir, settings.media_dir, settings.media_trash_dir, settings.backup_dir]:
        Path(path).mkdir(parents=True, exist_ok=True)


ensure_directories()
engine = create_engine(f"sqlite:///{settings.sqlite_path}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
