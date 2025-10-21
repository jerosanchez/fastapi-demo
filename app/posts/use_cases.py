# Use case ABCs and implementations for posts feature
from abc import ABC, abstractmethod

from sqlalchemy import Row, func
from sqlalchemy.orm import Session

from app.users.models import User
from app.votes.models import Vote

from .models import CreatePostData, Post, UpdatePostData

# Type hint alias for a row containing a Post and its vote count
PostWithVotes = Row[tuple[Post, int]]


class GetPostsUseCaseABC(ABC):
    @abstractmethod
    def execute(
        self, page: int, size: int, search: str | None, db: Session
    ) -> list[PostWithVotes]:
        pass


class GetPostsUseCase(GetPostsUseCaseABC):
    def execute(
        self, page: int, size: int, search: str | None, db: Session
    ) -> list[PostWithVotes]:
        query = self._fetch_posts_with_votes_query(db)
        if search:
            query = query.filter(Post.title.ilike(f"%{search}%"))
        return query.offset((page - 1) * size).limit(size).all()

    def _fetch_posts_with_votes_query(self, db: Session):
        return (
            db.query(Post, func.count(Vote.post_id).label("votes"))
            .join(Vote, Vote.post_id == Post.id, isouter=True)
            .group_by(Post.id)
        )


class CreatePostUseCaseABC(ABC):
    @abstractmethod
    def execute(
        self, post_data: CreatePostData, db: Session, current_user: User
    ) -> Post:
        pass


class CreatePostUseCase(CreatePostUseCaseABC):
    def execute(self, post_data: CreatePostData, db: Session, current_user: User):
        new_post = Post(
            owner_id=current_user.id,
            title=post_data.title,
            content=post_data.content,
            published=post_data.published,
            rating=post_data.rating,
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post


class GetPostByIdUseCaseABC(ABC):
    @abstractmethod
    def execute(self, post_id: str, db: Session) -> object:
        pass


class GetPostByIdUseCase(GetPostByIdUseCaseABC):
    def execute(self, post_id: str, db: Session):
        query = (
            db.query(Post, func.count(Vote.post_id).label("votes"))
            .join(Vote, Vote.post_id == Post.id, isouter=True)
            .group_by(Post.id)
        )
        post = query.filter(Post.id == post_id).first()
        return post


class UpdatePostUseCaseABC(ABC):
    @abstractmethod
    def execute(
        self, post_id: str, post_data: UpdatePostData, db: Session, current_user: User
    ) -> object:
        pass


class UpdatePostUseCase(UpdatePostUseCaseABC):
    def execute(
        self, post_id: str, post_data: UpdatePostData, db: Session, current_user: User
    ):
        post_query = db.query(Post).filter(Post.id == post_id)
        post = post_query.first()
        if getattr(post, "owner_id", None) != current_user.id:
            return None
        update_data = self._build_update_data(post_data)
        post_query.update(update_data)
        db.commit()
        db.refresh(post)
        return post

    def _build_update_data(self, post_data: UpdatePostData):
        update_data = {}
        if post_data.title is not None:
            update_data[getattr(Post, "title")] = post_data.title
        if post_data.content is not None:
            update_data[getattr(Post, "content")] = post_data.content
        if post_data.published is not None:
            update_data[getattr(Post, "published")] = post_data.published
        if post_data.rating is not None:
            update_data[getattr(Post, "rating")] = post_data.rating
        return update_data


class DeletePostUseCaseABC(ABC):
    @abstractmethod
    def execute(self, post_id: str, db: Session, current_user: User) -> bool:
        pass


class DeletePostUseCase(DeletePostUseCaseABC):
    def execute(self, post_id: str, db: Session, current_user: User):
        post_query = db.query(Post).filter(Post.id == post_id)
        post = post_query.first()
        if getattr(post, "owner_id", None) != current_user.id:
            return False
        post_query.delete()
        db.commit()
        return True
