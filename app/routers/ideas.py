from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Idea, Library, MediaAsset
from app.schemas import IdeaCreate, IdeaNode, IdeaRead, MediaUploadResponse
from app.services.idea_service import build_tree, create_idea
from app.services.media_service import save_media, soft_delete_media

router = APIRouter(prefix="/api/ideas", tags=["ideas"])


@router.post("", response_model=IdeaRead)
def create_idea_item(payload: IdeaCreate, db: Session = Depends(get_db)) -> Idea:
    exists = db.scalar(select(Library).where(Library.id == payload.library_id))
    if not exists:
        raise HTTPException(status_code=404, detail="Library not found")

    idea = create_idea(db, payload)
    db.commit()
    db.refresh(idea)
    return idea


@router.get("/library/{library_id}", response_model=list[IdeaRead])
def list_ideas(library_id: int, db: Session = Depends(get_db)) -> list[Idea]:
    return db.scalars(select(Idea).where(Idea.library_id == library_id)).all()


@router.get("/library/{library_id}/tree", response_model=list[IdeaNode])
def get_idea_tree(library_id: int, db: Session = Depends(get_db)) -> list[IdeaNode]:
    return build_tree(db, library_id)


@router.post("/media", response_model=MediaUploadResponse)
def upload_media(file: UploadFile = File(...), db: Session = Depends(get_db)) -> MediaUploadResponse:
    media = save_media(db, file)
    db.commit()
    return MediaUploadResponse(media_id=media.id, media_path=media.file_path)


@router.delete("/media/{media_id}")
def delete_media(media_id: str, db: Session = Depends(get_db)) -> dict[str, str]:
    media = db.scalar(select(MediaAsset).where(MediaAsset.id == media_id))
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    soft_delete_media(db, media)
    db.commit()
    return {"status": "trashed"}
