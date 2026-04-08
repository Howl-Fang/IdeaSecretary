from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Idea
from app.schemas import ChatRequest, ChatResponse
from app.services.ai_client import ai_client
from app.services.index_service import search_idea_ids

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    idea_ids = search_idea_ids(db, payload.question, payload.library_id)
    if idea_ids:
        ideas = db.scalars(select(Idea).where(Idea.id.in_(idea_ids))).all()
    else:
        ideas = db.scalars(select(Idea).where(Idea.library_id == payload.library_id).limit(5)).all()

    context = "\n\n".join([f"[{i.title}]\n{i.content_markdown}" for i in ideas]) or "No notes found"
    answer = ai_client.chat(payload.question, context)
    return ChatResponse(answer=answer, references=[idea.id for idea in ideas])
