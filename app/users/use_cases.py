from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from .models import CreateUserData, User
from .services import UserServiceABC


class CreateUserUseCaseABC(ABC):
    @abstractmethod
    def execute(self, new_user_data: CreateUserData, db: Session) -> User:
        pass


class GetUserByIdUseCaseABC(ABC):
    @abstractmethod
    def execute(self, user_id: str, db: Session) -> User | None:
        pass


class CreateUserUseCase(CreateUserUseCaseABC):
    def __init__(self, service: UserServiceABC):
        self.service = service

    def execute(self, new_user_data: CreateUserData, db: Session) -> User:
        return self.service.create_user(new_user_data, db)


class GetUserByIdUseCase(GetUserByIdUseCaseABC):
    def __init__(self, service: UserServiceABC):
        self.service = service

    def execute(self, user_id: str, db: Session) -> User | None:
        return self.service.get_user_by_id(user_id, db)
