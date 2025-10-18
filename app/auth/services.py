from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.utils.passwords import verify_password

from .exceptions import PasswordVerificationException, UserNotFoundException
from .repositories import AuthRepositoryProtocol


class AuthServiceProtocol(ABC):
    @abstractmethod
    def authenticate_user(self, db, username: str, password: str):
        pass


class AuthService(AuthServiceProtocol):
    def __init__(self, repository: AuthRepositoryProtocol):
        self.repository = repository

    def authenticate_user(self, db: Session, username: str, password: str):
        user = self.repository.get_user_by_email(db, username)

        if not user:
            raise UserNotFoundException()
        if not verify_password(password, user.password):
            raise PasswordVerificationException()

        return user
