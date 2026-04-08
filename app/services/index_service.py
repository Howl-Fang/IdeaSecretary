from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Idea, IdeaIndex


def upsert_idea_index(db: Session, idea: Idea) -> None:
    text = f"{idea.title}\n{idea.content_markdown}\n{idea.ai_insight}".strip()
    existing = db.scalar(select(IdeaIndex).where(IdeaIndex.idea_id == idea.id))
    if existing:
        existing.searchable_text = text
    else:
        db.add(IdeaIndex(idea_id=idea.id, searchable_text=text))


def search_idea_ids(db: Session, keyword: str, library_id: int, limit: int = 10) -> list[str]:
    stmt = (
        select(Idea.id)
        .join(IdeaIndex, Idea.id == IdeaIndex.idea_id)
        .where(Idea.library_id == library_id)
        .where(IdeaIndex.searchable_text.ilike(f"%{keyword}%"))
        .limit(limit)
    )
    return [row[0] for row in db.execute(stmt).all()]
