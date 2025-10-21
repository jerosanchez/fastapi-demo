from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from app.auth.exceptions import PasswordVerificationException, UserNotFoundException
from app.auth.models import Token
from app.auth.use_cases import AuthenticateUserUseCase
from tests.shared.test_helpers import random_password, random_string, random_user_id


class TestAuthenticateUserUseCase:
    def setup_method(self):
        self.auth_service_mock = Mock()
        self.token_provider_mock = Mock()
        self.sut = AuthenticateUserUseCase(
            self.auth_service_mock, self.token_provider_mock
        )

        self.mock_db = Mock(spec=Session)

    def test_execute_happy_path(self):
        """Should return a Token when authentication succeeds."""
        user_id = random_user_id()
        correct_password = random_password()
        created_token = random_string()

        self.token_provider_mock.create_access_token.return_value = created_token

        result = self.sut.execute(self.mock_db, str(user_id), correct_password)

        self.auth_service_mock.authenticate_user.assert_called_once_with(
            self.mock_db, str(user_id), correct_password
        )

        assert result == Token(access_token=created_token, token_type="bearer")

        self.token_provider_mock.create_access_token.assert_called_once()

    def test_execute_user_not_found(self):
        """Should raise UserNotFoundException if user does not exist."""
        non_existent_user_id = random_user_id()

        self.auth_service_mock.authenticate_user.side_effect = UserNotFoundException

        with pytest.raises(UserNotFoundException):
            self.sut.execute(self.mock_db, non_existent_user_id, random_password())

        self.token_provider_mock.create_access_token.assert_not_called()

    def test_execute_password_verification_error(self):
        """Should raise PasswordVerificationException if password is invalid."""
        wrong_password = random_password()

        self.auth_service_mock.authenticate_user.side_effect = (
            PasswordVerificationException
        )

        with pytest.raises(PasswordVerificationException):
            self.sut.execute(self.mock_db, random_user_id(), wrong_password)

        self.token_provider_mock.create_access_token.assert_not_called()
