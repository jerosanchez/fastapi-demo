from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PostSchemaBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None


class PostResponse(PostSchemaBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class PostCreate(PostSchemaBase):
    pass


class PostUpdate(PostSchemaBase):
    pass
