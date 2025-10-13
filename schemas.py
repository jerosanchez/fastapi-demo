import random
from uuid import UUID, uuid4

from pydantic import BaseModel


class PostSchemaBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None


class PostOut(PostSchemaBase):
    id: UUID


class PostCreate(PostSchemaBase):
    pass


class PostUpdate(PostSchemaBase):
    pass
