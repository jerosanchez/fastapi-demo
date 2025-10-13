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


def create_random_posts(count: int) -> list[PostOut]:
    return [
        PostOut(
            id=uuid4(),
            title=f"Random Post {i}",
            content=f"This is the content of random post {i}",
            published=random.choice([True, False]),
            rating=random.randint(1, 5) if random.choice([True, False]) else None,
        )
        for i in range(count)
    ]
