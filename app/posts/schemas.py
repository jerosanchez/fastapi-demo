from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.users.schemas import UserOut


class PostSchemaBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None


class PostOut(PostSchemaBase):
    id: UUID
    created_at: datetime
    owner: UserOut

    class Config:
        from_attributes = True


class PostWithVotes(BaseModel):
    Post: PostOut
    votes: int


class PostCreate(PostSchemaBase):
    pass


class PostUpdate(PostSchemaBase):
    pass
