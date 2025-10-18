from sqlalchemy.orm import Session

from app.auth.oauth2 import create_access_token
from app.auth.service import AuthServiceProtocol

from .models import Token, TokenPayload


class AuthenticateUserUseCase:
    def __init__(self, auth_service: AuthServiceProtocol):
        self.auth_service = auth_service

    def execute(self, db: Session, username: str, password: str) -> Token:
        user = self.auth_service.authenticate_user(db, username, password)
        access_token = create_access_token(payload=TokenPayload(user_id=user.id))

        return Token(access_token=access_token, token_type="bearer")
