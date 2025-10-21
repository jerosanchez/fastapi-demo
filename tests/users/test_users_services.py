from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from app.users.exceptions import EmailAlreadyExistsException
from app.users.models import NewUserData, User
from app.users.services import UserService
from tests.shared.helpers import (
    make_user,
    random_email,
    random_password,
    random_user_id,
)


class TestUserService:
    def setup_method(self):
        self.mock_repo = Mock()
        self.service = UserService(self.mock_repo)
        self.db = Mock(spec=Session)

    def test_create_user_happy_path(self):
        """Should return new user when email does not exist."""
        new_user_request_data = make_new_user_data()
        fake_hashed_password = random_password()
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
        new_user_request_data = make_new_user_data()
        fake_hashed_password = random_password()
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
        stored_user = make_user()

        self.mock_repo.get_user_by_id.return_value = stored_user

        retrieved_user = self.service.get_user_by_id(str(stored_user.id), self.db)

        assert retrieved_user == stored_user

    def test_get_user_by_id_not_found(self):
        """Should return None when user_id does not exist."""
        user_id = random_user_id()

        self.mock_repo.get_user_by_id.return_value = None

        user = self.service.get_user_by_id(user_id, self.db)

        assert user is None


# === Helper functions ===


def make_new_user_data(
    email: str = random_email(), password: str = random_password()
) -> NewUserData:
    return NewUserData(email=email, password=password)
