from unittest.mock import Mock, patch

import pytest
from sqlalchemy.orm import Session

from app.auth.exceptions import PasswordVerificationException, UserNotFoundException
from app.auth.repositories import AuthRepositoryABC
from app.auth.services import AuthService
from app.users.models import User


class TestAuthService:

    def setup_method(self):
        self.mock_repository = Mock(spec=AuthRepositoryABC)
        self.auth_service = AuthService(repository=self.mock_repository)
        self.mock_db = Mock(spec=Session)

    @patch("app.auth.services.verify_password")
    def test_authenticate_user_happy_path(self, mock_verify_password):
        """Should return user object if authentication is successful."""
        username = "user@example.com"
        password = "correct_password"
        mock_user = Mock(spec=User)
        mock_user.password = "hashed_password"
        mock_user.email = username
        mock_user.id = "user-123"

        self.mock_repository.get_user_by_email.return_value = mock_user
        mock_verify_password.return_value = True

        result = self.auth_service.authenticate_user(self.mock_db, username, password)

        assert result == mock_user

        self.mock_repository.get_user_by_email.assert_called_once_with(
            self.mock_db, username
        )
        mock_verify_password.assert_called_once_with(password, "hashed_password")

    def test_authenticate_user_not_found(self):
        """Should raise UserNotFoundException if user does not exist."""
        username = "nonexistent@example.com"
        password = "any_password"
        self.mock_repository.get_user_by_email.return_value = None

        with pytest.raises(UserNotFoundException):
            self.auth_service.authenticate_user(self.mock_db, username, password)

        self.mock_repository.get_user_by_email.assert_called_once_with(
            self.mock_db, username
        )

    @patch("app.auth.services.verify_password")
    def test_authenticate_user_password_verification_error(self, mock_verify_password):
        """Should raise PasswordVerificationException if password is invalid."""
        username = "user@example.com"
        password = "wrong_password"
        mock_user = Mock(spec=User)
        mock_user.password = "hashed_password"

        self.mock_repository.get_user_by_email.return_value = mock_user
        mock_verify_password.return_value = False

        with pytest.raises(PasswordVerificationException):
            self.auth_service.authenticate_user(self.mock_db, username, password)

        self.mock_repository.get_user_by_email.assert_called_once_with(
            self.mock_db, username
        )
        mock_verify_password.assert_called_once_with(password, "hashed_password")
