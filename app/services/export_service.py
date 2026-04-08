from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Idea, Library


def export_library_zip(db: Session, library_id: int) -> bytes:
    library = db.scalar(select(Library).where(Library.id == library_id))
    ideas = db.scalars(select(Idea).where(Idea.library_id == library_id)).all()
    if not library:
        raise ValueError("Library not found")

    buffer = BytesIO()
    with ZipFile(buffer, "w", compression=ZIP_DEFLATED) as zf:
        zf.writestr("library.txt", f"Library: {library.name}\nDescription: {library.description}\n")
        for idea in ideas:
            filename = Path(f"ideas/{idea.id}_{idea.title[:50]}.md")
            zf.writestr(str(filename), idea.content_markdown)
    return buffer.getvalue()


def export_mindmap_mermaid(db: Session, library_id: int) -> str:
    ideas = db.scalars(select(Idea).where(Idea.library_id == library_id)).all()
    lines = ["mindmap", f"  root((Library {library_id}))"]
    for idea in ideas:
        safe_title = idea.title.replace("\n", " ").strip()
        if idea.parent_id:
            lines.append(f"  {idea.parent_id}[{idea.parent_id}] --> {idea.id}[{safe_title}]")
        else:
            lines.append(f"  root --> {idea.id}[{safe_title}]")
    return "\n".join(lines)
