from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.providers import JwtOAuth2TokenProvider, OAuth2TokenProviderABC
from app.users.models import User

from .database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_token_provider() -> OAuth2TokenProviderABC:
    return JwtOAuth2TokenProvider()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    token_provider: OAuth2TokenProviderABC = Depends(get_token_provider),
) -> User:
    # TODO: Convert to a custom exception class and let the client to handle it
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = token_provider.verify_access_token(token, credentials_exception)
    user = _fetch_user(str(payload.user_id), db)

    if not user:
        raise credentials_exception

    return user


# Helper functions


def _fetch_user(user_id: str, db: Session) -> User:
    # TODO: Cache user lookups to avoid hitting the database on
    # every request; use ACCESS_TOKEN_EXPIRE_MINUTES as cache expiry

    return db.query(User).filter(User.id == user_id).first()
