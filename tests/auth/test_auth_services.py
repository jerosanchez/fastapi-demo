from unittest.mock import Mock, patch

import pytest
from sqlalchemy.orm import Session

from app.auth.exceptions import PasswordVerificationException, UserNotFoundException
from app.auth.repositories import AuthRepositoryABC
from app.auth.services import AuthService

from ..shared.helpers import make_user, random_password, random_user_id


class TestAuthService:

    def setup_method(self):
        self.mock_repository = Mock(spec=AuthRepositoryABC)
        self.auth_service = AuthService(repository=self.mock_repository)
        self.mock_db = Mock(spec=Session)

    @patch("app.auth.services.verify_password")
    def test_authenticate_user_happy_path(self, mock_verify_password):
        """Should return user object if authentication is successful."""
        existing_user = make_user()

        self.mock_repository.get_user_by_email.return_value = existing_user
        mock_verify_password.return_value = True

        result = self.auth_service.authenticate_user(
            self.mock_db, str(existing_user.id), "correct_password"
        )

        assert result == existing_user

    def test_authenticate_user_not_found(self):
        """Should raise UserNotFoundException if user does not exist."""
        self.mock_repository.get_user_by_email.return_value = None

        with pytest.raises(UserNotFoundException):
            any_user_id = random_user_id()
            any_password = random_password()
            self.auth_service.authenticate_user(
                self.mock_db, str(any_user_id), any_password
            )

    @patch("app.auth.services.verify_password")
    def test_authenticate_user_password_verification_error(self, mock_verify_password):
        """Should raise PasswordVerificationException if password is invalid."""
        existing_user = make_user()

        self.mock_repository.get_user_by_email.return_value = existing_user
        mock_verify_password.return_value = False

        with pytest.raises(PasswordVerificationException):
            any_user_id = random_user_id()
            any_password = random_password()
            self.auth_service.authenticate_user(
                self.mock_db, str(any_user_id), any_password
            )
