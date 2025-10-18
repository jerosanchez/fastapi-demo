from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.utils.passwords import verify_password

from .exceptions import PasswordVerificationException, UserNotFoundException
from .models import Token, TokenPayload
from .oauth2 import create_access_token
from .repository import AuthRepositoryProtocol


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

    def create_token(self, user: TokenPayload) -> Token:
        access_token = create_access_token(payload=user)

        return Token(access_token=access_token, token_type="bearer")
