from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PostSchemaBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None


class PostOut(PostSchemaBase):
    id: UUID
    created_at: datetime
    owner_id: UUID

    class Config:
        from_attributes = True


class PostCreate(PostSchemaBase):
    pass


class PostUpdate(PostSchemaBase):
    pass
