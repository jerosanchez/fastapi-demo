from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy.orm import Session

from app.users.models import User

from .exceptions import ForbiddenException
from .models import CreatePostData, Post, UpdatePostData
from .policies import PostPolicy
from .repositories import PostRepositoryABC


class PostServiceABC(ABC):
    @abstractmethod
    def get_posts(
        self, page: int, size: int, search: str | None, db: Session, current_user: User
    ) -> Sequence[tuple[Post, int]]:
        pass

    @abstractmethod
    def create_post(
        self, post_data: CreatePostData, db: Session, current_user: User
    ) -> Post:
        pass

    @abstractmethod
    def get_post_by_id(
        self, post_id: str, db: Session, current_user: User
    ) -> Post | None:
        pass

    @abstractmethod
    def update_post(
        self, post_id: str, post_data: UpdatePostData, db: Session, current_user: User
    ) -> Post | None:
        pass

    @abstractmethod
    def delete_post(self, post_id: str, db: Session, current_user: User) -> None:
        pass


class PostService(PostServiceABC):
    def __init__(self, post_repository: PostRepositoryABC, post_policy: PostPolicy):
        self._post_repository = post_repository
        self._post_policy = post_policy

    def get_posts(
        self, page: int, size: int, search: str | None, db: Session, current_user: User
    ) -> Sequence[tuple[Post, int]]:
        posts = self._post_repository.get_posts(page, size, search, db)
        filtered_posts = [
            (post, votes)
            for post, votes in posts
            if self._post_policy.can_view(post, current_user)
        ]
        return filtered_posts

    def create_post(
        self, post_data: CreatePostData, db: Session, current_user: User
    ) -> Post:
        if not self._post_policy.can_create(current_user):
            raise ForbiddenException()

        new_post = Post(
            owner_id=current_user.id,
            title=post_data.title,
            content=post_data.content,
            published=post_data.published,
            rating=post_data.rating,
        )
        return self._post_repository.create_post(new_post, db)

    def get_post_by_id(
        self, post_id: str, db: Session, current_user: User
    ) -> Post | None:
        post = self._post_repository.get_post_by_id(post_id, db)

        if not self._post_policy.can_view(post, current_user):
            raise ForbiddenException()

        return post

    def update_post(
        self, post_id: str, post_data: UpdatePostData, db: Session, current_user: User
    ) -> Post | None:
        post = self._post_repository.get_post_by_id(post_id, db)
        if not post:
            return None
        if not self._post_policy.can_update(post, current_user):
            raise ForbiddenException()
        update_data = self._build_update_data(post_data)
        return self._post_repository.update_post(post, update_data, db)

    def delete_post(self, post_id: str, db: Session, current_user: User) -> None:
        post = self._post_repository.get_post_by_id(post_id, db)
        if not post:
            return None
        if not self._post_policy.can_delete(post, current_user):
            raise ForbiddenException()
        self._post_repository.delete_post(post, db)
        return None

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
