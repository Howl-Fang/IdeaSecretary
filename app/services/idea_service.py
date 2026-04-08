import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Idea
from app.schemas import IdeaCreate, IdeaNode
from app.services.ai_client import ai_client
from app.services.backup_service import tick_operation_and_backup_if_needed
from app.services.index_service import upsert_idea_index


def create_idea(db: Session, payload: IdeaCreate) -> Idea:
    ai_result = ai_client.organize_note(payload.content)
    markdown = f"# {payload.title}\n\n{payload.content}\n\n## AI Summary\n{ai_result.get('summary', '')}"
    idea = Idea(
        id=str(uuid.uuid4()),
        library_id=payload.library_id,
        title=payload.title,
        content_markdown=markdown,
        source_type=payload.source_type,
        source_value=payload.source_value,
        ai_insight=ai_result.get("insight", ""),
        parent_id=payload.parent_id,
    )
    db.add(idea)
    db.flush()

    upsert_idea_index(db, idea)
    tick_operation_and_backup_if_needed(db)
    return idea


def build_tree(db: Session, library_id: int) -> list[IdeaNode]:
    ideas = db.scalars(select(Idea).where(Idea.library_id == library_id)).all()
    nodes = {idea.id: IdeaNode(id=idea.id, title=idea.title, children=[]) for idea in ideas}
    roots: list[IdeaNode] = []

    for idea in ideas:
        node = nodes[idea.id]
        if idea.parent_id and idea.parent_id in nodes:
            nodes[idea.parent_id].children.append(node)
        else:
            roots.append(node)
    return roots
