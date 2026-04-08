from datetime import datetime

from pydantic import BaseModel, Field


class LibraryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str = ""


class LibraryRead(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime

    model_config = {"from_attributes": True}


class IdeaCreate(BaseModel):
    library_id: int
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    source_type: str = Field(default="text")
    source_value: str = ""
    parent_id: str | None = None


class IdeaRead(BaseModel):
    id: str
    library_id: int
    title: str
    content_markdown: str
    source_type: str
    source_value: str
    ai_insight: str
    parent_id: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class IdeaNode(BaseModel):
    id: str
    title: str
    children: list["IdeaNode"] = []


class ChatRequest(BaseModel):
    library_id: int
    question: str = Field(min_length=1)


class ChatResponse(BaseModel):
    answer: str
    references: list[str]


class MediaUploadResponse(BaseModel):
    media_id: str
    media_path: str
