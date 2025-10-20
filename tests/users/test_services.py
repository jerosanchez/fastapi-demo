from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from app.users.exceptions import EmailAlreadyExistsException
from app.users.models import NewUserData, User
from app.users.services import UserService


class TestUserService:
    def setup_method(self):
        """Set up UserService with a mock repository for each test."""
        self.mock_repo = Mock()
        self.service = UserService(self.mock_repo)
        self.db = Mock(spec=Session)
        self.new_email = "new@example.com"
        self.existing_email = "existing@example.com"
        self.password = "password"
        self.hashed_password = "hashed_password"
        self.user_id = "user-123"

    def test_create_user_happy_path(self):
        """Should create a new user when email does not exist."""
        new_user_data = NewUserData(email=self.new_email, password=self.password)
        self.mock_repo.get_user_by_email.return_value = None
        expected_user = User(
            email=self.new_email, password=self.hashed_password, is_active=True
        )
        self.mock_repo.add_user.return_value = expected_user

        created_user = self.service.create_user(new_user_data, self.db)

        assert created_user == expected_user

    def test_create_user_email_exists(self):
        """Should raise EmailAlreadyExistsException if email already exists."""
        new_user_data = NewUserData(email=self.existing_email, password=self.password)
        self.mock_repo.get_user_by_email.return_value = User(
            email=self.existing_email, password=self.hashed_password, is_active=True
        )

        with pytest.raises(EmailAlreadyExistsException):
            self.service.create_user(new_user_data, self.db)

    def test_get_user_by_id_happy_path(self):
        """Should return user when user_id exists."""
        expected_user = User(
            email=self.existing_email, password=self.hashed_password, is_active=True
        )
        self.mock_repo.get_user_by_id.return_value = expected_user

        retrieved_user = self.service.get_user_by_id(self.user_id, self.db)

        assert retrieved_user == expected_user

    def test_get_user_by_id_not_found(self):
        """Should return None when user_id does not exist."""
        self.mock_repo.get_user_by_id.return_value = None

        user = self.service.get_user_by_id(self.user_id, self.db)

        assert user is None
