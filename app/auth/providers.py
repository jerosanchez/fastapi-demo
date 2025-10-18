from abc import ABC, abstractmethod
from dataclasses import asdict
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import settings

from .models import TokenPayload


class OAuth2TokenProviderABC(ABC):
    @abstractmethod
    def create_access_token(self, payload: TokenPayload) -> str:
        pass

    @abstractmethod
    def verify_access_token(self, token: str, credentials_exception) -> TokenPayload:
        pass


class JwtOAuth2TokenProvider(OAuth2TokenProviderABC):
    @staticmethod
    def create_access_token(payload: TokenPayload) -> str:
        payload = asdict(payload)
        expire_time = datetime.now(timezone.utc) + timedelta(
            minutes=settings.oauth_token_ttl
        )
        payload["exp"] = expire_time

        return jwt.encode(
            payload, settings.oauth_hash_key, algorithm=settings.oauth_algorithm
        )

    @staticmethod
    def verify_access_token(token: str, credentials_exception) -> TokenPayload:
        try:
            payload = jwt.decode(
                token,
                settings.oauth_hash_key,
                algorithms=[settings.oauth_algorithm],
            )

            user_id = payload.get("user_id")
            if user_id is None:
                raise credentials_exception

            return TokenPayload(user_id=user_id)

        except JWTError:
            raise credentials_exception
