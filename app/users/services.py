from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from .exceptions import EmailAlreadyExistsException
from .models import NewUserData, User
from .repositories import UserRepositoryABC
from .utils import hash_password


class UserServiceABC(ABC):
    @abstractmethod
    def create_user(self, new_user_data: NewUserData, db: Session) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str, db: Session) -> User | None:
        pass


class UserService(UserServiceABC):
    def __init__(self, repository: UserRepositoryABC):
        self.repository = repository

    def create_user(self, new_user_data: NewUserData, db: Session) -> User:
        if self.repository.get_user_by_email(db, new_user_data.email):
            raise EmailAlreadyExistsException(new_user_data.email)

        hashed_password = hash_password(new_user_data.password)
        new_user = User(
            email=new_user_data.email, password=hashed_password, is_active=True
        )

        return self.repository.add_user(db, new_user)

    def get_user_by_id(self, user_id: str, db: Session) -> User | None:
        return self.repository.get_user_by_id(db, user_id)
