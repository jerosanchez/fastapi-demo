from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.users.models import User

from .models import CreatePostData, Post, UpdatePostData


class PostServiceABC(ABC):
    @abstractmethod
    def get_posts(
        self, page: int, size: int, search: str | None, db: Session
    ) -> list[Post]:
        pass

    @abstractmethod
    def create_post(
        self, post_data: CreatePostData, db: Session, current_user: User
    ) -> Post:
        pass

    @abstractmethod
    def get_post_by_id(self, post_id: str, db: Session) -> Post | None:
        pass

    @abstractmethod
    def update_post(
        self, post_id: str, post_data: UpdatePostData, db: Session, current_user: User
    ) -> Post | None:
        pass

    @abstractmethod
    def delete_post(self, post_id: str, db: Session, current_user: User) -> bool:
        pass


class PostService(PostServiceABC):
    def get_posts(
        self, page: int, size: int, search: str | None, db: Session
    ) -> list[Post]:
        query = db.query(Post)
        if search:
            query = query.filter(Post.title.ilike(f"%{search}%"))
        return query.offset((page - 1) * size).limit(size).all()

    def create_post(
        self, post_data: CreatePostData, db: Session, current_user: User
    ) -> Post:
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

    def get_post_by_id(self, post_id: str, db: Session) -> Post | None:
        return db.query(Post).filter(Post.id == post_id).first()

    def update_post(
        self, post_id: str, post_data: UpdatePostData, db: Session, current_user: User
    ) -> Post | None:
        post_query = db.query(Post).filter(Post.id == post_id)
        post = post_query.first()
        if getattr(post, "owner_id", None) != current_user.id:
            return None
        update_data = self._build_update_data(post_data)
        post_query.update(update_data)
        db.commit()
        db.refresh(post)
        return post

    def delete_post(self, post_id: str, db: Session, current_user: User) -> bool:
        post_query = db.query(Post).filter(Post.id == post_id)
        post = post_query.first()
        if getattr(post, "owner_id", None) != current_user.id:
            return False
        post_query.delete()
        db.commit()
        return True

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
