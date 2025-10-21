import uuid
from datetime import datetime, timezone

from app.users.models import User


def random_string(length: int = 6) -> str:
    import random
    import string

    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def random_user_id() -> str:
    return str(uuid.uuid4())


def random_password() -> str:
    return random_string(20)


def random_email() -> str:
    return f"{random_string()}@example.com"


def now_with_tz():
    return datetime.now(timezone.utc)


def make_stored_user(
    id: str = random_user_id(),
    email: str = random_email(),
    password: str = random_password(),
    is_active: bool = True,
    created_at: str = str(now_with_tz()),
) -> User:
    return User(
        id=id,
        email=email,
        password=password,
        is_active=is_active,
        created_at=created_at,
    )
