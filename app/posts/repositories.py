from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.votes.models import Vote

from .models import Post


class PostRepositoryABC(ABC):
    @abstractmethod
    def get_posts(
        self, page: int, size: int, search: str | None, db: Session
    ) -> Sequence[tuple[Post, int]]:
        pass

    @abstractmethod
    def create_post(self, post: Post, db: Session) -> Post:
        pass

    @abstractmethod
    def get_post_by_id(self, post_id: str, db: Session) -> Post | None:
        pass

    @abstractmethod
    def update_post(self, post: Post, update_data: dict, db: Session) -> Post:
        pass

    @abstractmethod
    def delete_post(self, post: Post, db: Session) -> None:
        pass


class PostRepository(PostRepositoryABC):
    def get_posts(
        self, page: int, size: int, search: str | None, db: Session
    ) -> Sequence[tuple[Post, int]]:
        query = db.query(Post, func.count(Vote.user_id).label("votes")).outerjoin(
            Vote, Vote.post_id == Post.id
        )
        if search:
            query = query.filter(Post.title.ilike(f"%{search}%"))
        query = query.group_by(Post.id)
        query = query.offset((page - 1) * size).limit(size)
        rows = query.all()  # this is the correct value to return
        return [(row[0], row[1]) for row in rows]  # to avoid linting errors

    def create_post(self, post: Post, db: Session) -> Post:
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

    def get_post_by_id(self, post_id: str, db: Session) -> Post | None:
        return db.query(Post).filter(Post.id == post_id).first()

    def update_post(self, post: Post, update_data: dict, db: Session) -> Post:
        db.query(Post).filter(Post.id == post.id).update(update_data)
        db.commit()
        db.refresh(post)
        return post

    def delete_post(self, post: Post, db: Session) -> None:
        db.delete(post)
        db.commit()
