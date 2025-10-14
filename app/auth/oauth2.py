from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from . import schemas

# TODO: Change SECRET_KEY to a secure random value and keep it secret
# To get a string like this run: openssl rand -hex 32
SECRET_KEY = "7bdb4bcf0b01f00ca206693965b29145611d9419563630525dc848024c38fc08"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict) -> str:
    payload = data.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload.update({"exp": expire_time})

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return _verify_access_token(token, credentials_exception)


# Helper functions


def _verify_access_token(token: str, credentials_exception) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception

        return schemas.TokenData(user_id=user_id)

    except JWTError:
        raise credentials_exception
