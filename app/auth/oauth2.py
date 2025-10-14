from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

# TODO: Change SECRET_KEY to a secure random value and keep it secret
# To get a string like this run: openssl rand -hex 32
SECRET_KEY = "7bdb4bcf0b01f00ca206693965b29145611d9419563630525dc848024c38fc08"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    payload = data.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload.update({"exp": expire_time})

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
