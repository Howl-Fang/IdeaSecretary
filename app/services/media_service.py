import shutil
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.config import settings
from app.models import MediaAsset


def save_media(db: Session, file: UploadFile) -> MediaAsset:
    media_id = str(uuid.uuid4())
    ext = Path(file.filename or "").suffix
    target = settings.media_dir / f"{media_id}{ext}"

    with target.open("wb") as out:
        shutil.copyfileobj(file.file, out)

    media = MediaAsset(
        id=media_id,
        original_name=file.filename or media_id,
        mime_type=file.content_type or "application/octet-stream",
        file_path=str(target),
    )
    db.add(media)
    return media


def soft_delete_media(db: Session, media: MediaAsset) -> MediaAsset:
    source = Path(media.file_path)
    target = settings.media_trash_dir / source.name
    if source.exists():
        source.replace(target)
    media.file_path = str(target)
    media.status = "trashed"
    media.deleted_at = datetime.utcnow()
    return media
