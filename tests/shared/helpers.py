import uuid

from app.users.models import User


def _random_string(length: int = 6) -> str:
    import random
    import string

    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def random_user_id() -> str:
    return str(uuid.uuid4())


def random_password() -> str:
    return _random_string(20)


def random_email() -> str:
    return f"{_random_string()}@example.com"


def make_user(
    id: str = random_user_id(),
    email: str = random_email(),
    password: str = random_password(),
    is_active: bool = True,
) -> User:
    return User(id=id, email=email, password=password, is_active=is_active)
