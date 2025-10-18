from abc import ABC

from sqlalchemy.orm import Session

from .models import Token, TokenPayload
from .providers import OAuth2TokenProviderABC
from .services import AuthServiceABC


class AuthenticateUserUseCaseABC(ABC):
    def execute(self, db: Session, username: str, password: str) -> Token:
        pass


class AuthenticateUserUseCase(AuthenticateUserUseCaseABC):
    def __init__(
        self,
        auth_service: AuthServiceABC,
        token_provider: OAuth2TokenProviderABC,
    ):
        self.auth_service = auth_service
        self.token_provider = token_provider

    def execute(self, db: Session, username: str, password: str) -> Token:
        user = self.auth_service.authenticate_user(db, username, password)
        access_token = self.token_provider.create_access_token(
            payload=TokenPayload(user_id=user.id)
        )

        return Token(access_token=access_token, token_type="bearer")
