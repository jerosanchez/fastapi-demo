from sqlalchemy.orm import Session

from .models import Token, TokenPayload
from .providers import OAuth2TokenProviderProtocol
from .services import AuthServiceProtocol


class AuthenticateUserUseCase:
    def __init__(
        self,
        auth_service: AuthServiceProtocol,
        token_provider: OAuth2TokenProviderProtocol,
    ):
        self.auth_service = auth_service
        self.token_provider = token_provider

    def execute(self, db: Session, username: str, password: str) -> Token:
        user = self.auth_service.authenticate_user(db, username, password)
        access_token = self.token_provider.create_access_token(
            payload=TokenPayload(user_id=user.id)
        )

        return Token(access_token=access_token, token_type="bearer")
