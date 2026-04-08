from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.export_service import export_library_zip, export_mindmap_mermaid

router = APIRouter(prefix="/api/export", tags=["export"])


@router.get("/library/{library_id}.zip")
def export_zip(library_id: int, db: Session = Depends(get_db)) -> Response:
    try:
        content = export_library_zip(db, library_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return Response(content, media_type="application/zip", headers={"Content-Disposition": f"attachment; filename=library_{library_id}.zip"})


@router.get("/library/{library_id}.mindmap")
def export_mindmap(library_id: int, db: Session = Depends(get_db)) -> Response:
    text = export_mindmap_mermaid(db, library_id)
    return Response(text, media_type="text/plain; charset=utf-8")
