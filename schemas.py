import random
from uuid import UUID, uuid4

from pydantic import BaseModel


class PostOut(BaseModel):
    id: UUID
    title: str
    content: str
    published: bool = True
    rating: int | None = None


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None
    rating: int | None = None
