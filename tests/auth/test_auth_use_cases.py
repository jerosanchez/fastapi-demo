from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from app.auth.exceptions import PasswordVerificationException, UserNotFoundException
from app.auth.models import Token, TokenPayload
from app.auth.use_cases import AuthenticateUserUseCase


class TestAuthenticateUserUseCase:
    def setup_method(self):
        self.mock_auth_service = Mock()
        self.mock_token_provider = Mock()
        self.mock_db = Mock(spec=Session)

    def test_execute_happy_path(self):
        """Should return a Token when authentication succeeds."""
        use_case = AuthenticateUserUseCase(
            self.mock_auth_service, self.mock_token_provider
        )

        mock_user = Mock()
        mock_user.id = "user-123"
        self.mock_auth_service.authenticate_user.return_value = mock_user
        self.mock_token_provider.create_access_token.return_value = "access-token"

        result = use_case.execute(self.mock_db, "user@example.com", "password")

        assert isinstance(result, Token)
        assert result.access_token == "access-token"
        assert result.token_type == "bearer"
        self.mock_auth_service.authenticate_user.assert_called_once_with(
            self.mock_db, "user@example.com", "password"
        )
        self.mock_token_provider.create_access_token.assert_called_once_with(
            payload=TokenPayload(user_id="user-123")
        )

    def test_execute_user_not_found(self):
        """Should raise UserNotFoundException if user does not exist."""
        use_case = AuthenticateUserUseCase(
            self.mock_auth_service, self.mock_token_provider
        )
        self.mock_auth_service.authenticate_user.side_effect = UserNotFoundException

        with pytest.raises(UserNotFoundException):
            use_case.execute(self.mock_db, "nouser@example.com", "password")
        self.mock_auth_service.authenticate_user.assert_called_once()
        self.mock_token_provider.create_access_token.assert_not_called()

    def test_execute_password_verification_error(self):
        """Should raise PasswordVerificationException if password is invalid."""
        use_case = AuthenticateUserUseCase(
            self.mock_auth_service, self.mock_token_provider
        )
        self.mock_auth_service.authenticate_user.side_effect = (
            PasswordVerificationException
        )

        with pytest.raises(PasswordVerificationException):
            use_case.execute(self.mock_db, "user@example.com", "wrongpassword")
        self.mock_auth_service.authenticate_user.assert_called_once()
        self.mock_token_provider.create_access_token.assert_not_called()
