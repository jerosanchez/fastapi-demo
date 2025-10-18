from dataclasses import asdict
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.users.models import User

from .models import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(payload: TokenPayload) -> str:
    payload = asdict(payload)
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=settings.oauth_token_ttl)
    payload["exp"] = expire_time

    return jwt.encode(
        payload, settings.oauth_hash_key, algorithm=settings.oauth_algorithm
    )


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = _verify_access_token(token, credentials_exception)

    user = _fetch_user(payload.user_id, db)

    if not user:
        raise credentials_exception

    return user


# Helper functions


def _verify_access_token(token: str, credentials_exception) -> TokenPayload:
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


def _fetch_user(user_id: str, db: Session) -> User:
    # TODO: Cache user lookups to avoid hitting the database on
    # every request; use ACCESS_TOKEN_EXPIRE_MINUTES as cache expiry

    return db.query(User).filter(User.id == user_id).first()
