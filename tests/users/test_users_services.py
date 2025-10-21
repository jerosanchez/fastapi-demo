from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from app.users.exceptions import EmailAlreadyExistsException
from app.users.models import CreateUserData
from app.users.services import UserService

from ..shared.test_helpers import (
    make_stored_user,
    random_email,
    random_password,
    random_user_id,
)


class TestUserService:
    def setup_method(self):
        self.user_repository_mock = Mock()
        self.sut = UserService(self.user_repository_mock)
        self.db = Mock(spec=Session)

    def test_create_user_happy_path(self):
        """Should return new user when email does not exist."""
        email = random_email()
        password = random_password()
        create_user_request_data = CreateUserData(email=email, password=password)

        new_stored_user = make_stored_user(email=email, password=password)

        self.user_repository_mock.get_user_by_email.return_value = None
        self.user_repository_mock.add_user.return_value = new_stored_user

        returned_user = self.sut.create_user(create_user_request_data, self.db)

        assert returned_user == new_stored_user

    def test_create_user_email_exists(self):
        """Should raise EmailAlreadyExistsException if email already exists."""
        email = random_email()
        password = random_password()
        create_user_request_data = CreateUserData(email=email, password=password)
        stored_user_with_same_email = make_stored_user(email=email)

        self.user_repository_mock.get_user_by_email.return_value = (
            stored_user_with_same_email
        )

        with pytest.raises(EmailAlreadyExistsException):
            self.sut.create_user(create_user_request_data, self.db)

    def test_get_user_by_id_happy_path(self):
        """Should return user when user_id exists."""
        stored_user = make_stored_user()

        self.user_repository_mock.get_user_by_id.return_value = stored_user

        returned_user = self.sut.get_user_by_id(str(stored_user.id), self.db)

        assert returned_user == stored_user

    def test_get_user_by_id_not_found(self):
        """Should return None when user_id does not exist."""
        self.user_repository_mock.get_user_by_id.return_value = None

        user = self.sut.get_user_by_id(random_user_id(), self.db)

        assert user is None
