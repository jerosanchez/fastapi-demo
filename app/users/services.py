from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.orm import Session

from .exceptions import EmailAlreadyExistsException
from .models import User
from .utils import hash_password


class UserServiceABC(ABC):
    @abstractmethod
    def create_user(self, user_data: dict[str, Any], db: Session) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str, db: Session) -> User | None:
        pass


class UserService(UserServiceABC):
    def create_user(self, user_data: dict[str, Any], db: Session) -> User:
        if db.query(User).filter(User.email == user_data["email"]).first():
            raise EmailAlreadyExistsException(user_data["email"])

        user_data = user_data.copy()
        user_data["password"] = hash_password(user_data["password"])
        new_user = User(**user_data)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    def get_user_by_id(self, user_id: str, db: Session) -> User | None:
        return db.query(User).filter(User.id == user_id).first()
