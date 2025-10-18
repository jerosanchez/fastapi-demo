from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.providers import JwtOAuth2TokenProvider
from app.core.database import get_db
from app.users.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = JwtOAuth2TokenProvider.verify_access_token(token, credentials_exception)

    user = _fetch_user(payload.user_id, db)

    if not user:
        raise credentials_exception

    return user


# Helper functions


def _fetch_user(user_id: str, db: Session) -> User:
    # TODO: Cache user lookups to avoid hitting the database on
    # every request; use ACCESS_TOKEN_EXPIRE_MINUTES as cache expiry

    return db.query(User).filter(User.id == user_id).first()
