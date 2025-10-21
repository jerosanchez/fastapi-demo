from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from app.users.exceptions import EmailAlreadyExistsException
from app.users.models import NewUserData, User
from app.users.services import UserService


class TestUserService:
    def setup_method(self):
        self.mock_repo = Mock()
        self.service = UserService(self.mock_repo)
        self.db = Mock(spec=Session)

    def test_create_user_happy_path(self):
        """Should return new user when email does not exist."""
        new_user_request_data = _make_new_user_data()
        fake_hashed_password = _random_string()
        expected_user = User(
            email=new_user_request_data.email,
            password=fake_hashed_password,
            is_active=True,
        )

        self.mock_repo.get_user_by_email.return_value = None
        self.mock_repo.add_user.return_value = expected_user

        created_user = self.service.create_user(new_user_request_data, self.db)

        assert created_user == expected_user

    def test_create_user_email_exists(self):
        """Should raise EmailAlreadyExistsException if email already exists."""
        new_user_request_data = _make_new_user_data()
        fake_hashed_password = _random_string()
        stored_user_with_same_email = User(
            email=new_user_request_data.email,  # not necessary, for doc purposes
            password=fake_hashed_password,
            is_active=True,
        )

        self.mock_repo.get_user_by_email.return_value = stored_user_with_same_email

        with pytest.raises(EmailAlreadyExistsException):
            self.service.create_user(new_user_request_data, self.db)

    def test_get_user_by_id_happy_path(self):
        """Should return user when user_id exists."""
        stored_user = _make_user()
        user_id = _random_string()

        self.mock_repo.get_user_by_id.return_value = stored_user

        retrieved_user = self.service.get_user_by_id(user_id, self.db)

        assert retrieved_user == stored_user

    def test_get_user_by_id_not_found(self):
        """Should return None when user_id does not exist."""
        user_id = _random_string()

        self.mock_repo.get_user_by_id.return_value = None

        user = self.service.get_user_by_id(user_id, self.db)

        assert user is None


# === Helper methods


def _random_string(length: int = 6) -> str:
    import random
    import string

    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def _make_new_user_data(
    email: str = f"{_random_string()}@example.com", password: str = _random_string()
) -> NewUserData:
    return NewUserData(email=email, password=password)


def _make_user(
    email: str = f"{_random_string()}@example.com",
    password: str = _random_string(),
    is_active: bool = True,
) -> User:
    return User(email=email, password=password, is_active=is_active)
