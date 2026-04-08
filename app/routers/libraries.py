from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Library
from app.schemas import LibraryCreate, LibraryRead

router = APIRouter(prefix="/api/libraries", tags=["libraries"])


@router.get("", response_model=list[LibraryRead])
def list_libraries(db: Session = Depends(get_db)) -> list[Library]:
    return db.scalars(select(Library).order_by(Library.created_at.desc())).all()


@router.post("", response_model=LibraryRead)
def create_library(payload: LibraryCreate, db: Session = Depends(get_db)) -> Library:
    item = Library(name=payload.name.strip(), description=payload.description.strip())
    db.add(item)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Library name already exists") from exc

    db.refresh(item)
    return item
