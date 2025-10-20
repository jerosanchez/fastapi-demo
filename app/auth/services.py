from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.users.models import User

from .exceptions import PasswordVerificationException, UserNotFoundException
from .repositories import AuthRepositoryABC
from .utils import verify_password


class AuthServiceABC(ABC):
    @abstractmethod
    def authenticate_user(self, db, username: str, password: str) -> User:
        pass


class AuthService(AuthServiceABC):
    def __init__(self, repository: AuthRepositoryABC):
        self.repository = repository

    def authenticate_user(self, db: Session, username: str, password: str) -> User:
        user = self.repository.get_user_by_email(db, username)

        if not user:
            raise UserNotFoundException()

        if not verify_password(password, str(user.password)):
            raise PasswordVerificationException()

        return user
