from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.orm import Session

from .exceptions import EmailAlreadyExistsException
from .models import User
from .utils import hash_password


class CreateUserABC(ABC):
    @abstractmethod
    def execute(self, user_data: dict[str, Any], db: Session) -> User:
        pass


class GetUserByIdABC(ABC):
    @abstractmethod
    def execute(self, user_id: str, db: Session) -> User | None:
        pass


class CreateUser(CreateUserABC):
    def execute(self, user_data: dict[str, Any], db: Session) -> User:
        if db.query(User).filter(User.email == user_data["email"]).first():
            raise EmailAlreadyExistsException(user_data["email"])

        user_data = user_data.copy()
        user_data["password"] = hash_password(user_data["password"])
        new_user = User(**user_data)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user


class GetUserById(GetUserByIdABC):
    def execute(self, user_id: str, db: Session) -> User | None:
        return db.query(User).filter(User.id == user_id).first()
