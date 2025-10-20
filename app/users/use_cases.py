from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.orm import Session

from .models import User
from .services import UserServiceABC


class CreateUserUseCaseABC(ABC):
    @abstractmethod
    def execute(self, user_data: dict[str, Any], db: Session) -> User:
        pass


class GetUserByIdUseCaseABC(ABC):
    @abstractmethod
    def execute(self, user_id: str, db: Session) -> User | None:
        pass


class CreateUserUseCase(CreateUserUseCaseABC):
    def __init__(self, service: UserServiceABC):
        self.service = service

    def execute(self, user_data: dict[str, Any], db: Session) -> User:
        return self.service.create_user(user_data, db)


class GetUserByIdUseCase(GetUserByIdUseCaseABC):
    def __init__(self, service: UserServiceABC):
        self.service = service

    def execute(self, user_id: str, db: Session) -> User | None:
        return self.service.get_user_by_id(user_id, db)
