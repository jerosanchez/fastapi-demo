from abc import ABC, abstractmethod

from sqlalchemy import Row
from sqlalchemy.orm import Session

from app.users.models import User

from .models import CreatePostData, Post, UpdatePostData
from .services import PostServiceABC

# Type hint alias for a row containing a Post and its vote count
PostWithVotes = Row[tuple[Post, int]]


class GetPostsUseCaseABC(ABC):
    @abstractmethod
    def execute(
        self, page: int, size: int, search: str | None, db: Session
    ) -> list[Post]:
        pass


class GetPostsUseCase(GetPostsUseCaseABC):
    def __init__(self, service: PostServiceABC):
        self._service = service

    def execute(
        self, page: int, size: int, search: str | None, db: Session
    ) -> list[Post]:
        return self._service.get_posts(page, size, search, db)


class CreatePostUseCaseABC(ABC):
    @abstractmethod
    def execute(
        self, post_data: CreatePostData, db: Session, current_user: User
    ) -> Post:
        pass


class CreatePostUseCase(CreatePostUseCaseABC):
    def __init__(self, service: PostServiceABC):
        self._service = service

    def execute(self, post_data: CreatePostData, db: Session, current_user: User):
        return self._service.create_post(post_data, db, current_user)


class GetPostByIdUseCaseABC(ABC):
    @abstractmethod
    def execute(self, post_id: str, db: Session) -> object:
        pass


class GetPostByIdUseCase(GetPostByIdUseCaseABC):
    def __init__(self, service: PostServiceABC):
        self._service = service

    def execute(self, post_id: str, db: Session):
        return self._service.get_post_by_id(post_id, db)


class UpdatePostUseCaseABC(ABC):
    @abstractmethod
    def execute(
        self, post_id: str, post_data: UpdatePostData, db: Session, current_user: User
    ) -> object:
        pass


class UpdatePostUseCase(UpdatePostUseCaseABC):
    def __init__(self, service: PostServiceABC):
        self._service = service

    def execute(
        self, post_id: str, post_data: UpdatePostData, db: Session, current_user: User
    ):
        return self._service.update_post(post_id, post_data, db, current_user)


class DeletePostUseCaseABC(ABC):
    @abstractmethod
    def execute(self, post_id: str, db: Session, current_user: User) -> bool:
        pass


class DeletePostUseCase(DeletePostUseCaseABC):
    def __init__(self, service: PostServiceABC):
        self._service = service

    def execute(self, post_id: str, db: Session, current_user: User):
        return self._service.delete_post(post_id, db, current_user)
