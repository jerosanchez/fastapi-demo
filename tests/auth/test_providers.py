from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest
from jose import jwt

from app.auth.models import TokenPayload
from app.auth.providers import JwtOAuth2TokenProvider


class DummyCredentialsException(Exception):
    pass


class TestJwtOAuth2TokenProvider:
    def setup_method(self):
        self.payload = TokenPayload(user_id="user-123")
        self.key = "test-secret-key"
        self.algorithm = "HS256"
        self.ttl = 15
        self.settings_patch = patch("app.auth.providers.settings")
        self.mock_settings = self.settings_patch.start()
        self.mock_settings.oauth_hash_key = self.key
        self.mock_settings.oauth_algorithm = self.algorithm
        self.mock_settings.oauth_token_ttl = self.ttl

    def teardown_method(self):
        self.settings_patch.stop()

    @patch("app.auth.providers.jwt.encode")
    def test_create_access_token_payload_data(self, mock_jwt_encode):
        """Should call jwt.encode with correct user id."""
        mock_jwt_encode.return_value = "mocked-token"

        JwtOAuth2TokenProvider.create_access_token(self.payload)

        args, kwargs = mock_jwt_encode.call_args
        payload_dict = args[0]
        assert payload_dict["user_id"] == self.payload.user_id

    @patch("app.auth.providers.jwt.encode")
    def test_create_access_token_expiration_ttl(self, mock_jwt_encode):
        """Should call jwt.encode with exp set to now + ttl minutes."""
        mock_jwt_encode.return_value = "mocked-token"

        JwtOAuth2TokenProvider.create_access_token(self.payload)

        args, kwargs = mock_jwt_encode.call_args
        payload_dict = args[0]
        exp_dt = payload_dict["exp"]
        now = datetime.now(timezone.utc)
        expected_exp = now + timedelta(minutes=self.ttl)
        # The expiration should be within a few seconds of now + ttl
        assert abs((exp_dt - expected_exp).total_seconds()) < 5

    @patch("app.auth.providers.jwt.encode")
    def test_create_access_token_hash_key(self, mock_jwt_encode):
        """Should call jwt.encode with correct hash key."""
        mock_jwt_encode.return_value = "mocked-token"

        JwtOAuth2TokenProvider.create_access_token(self.payload)

        args, kwargs = mock_jwt_encode.call_args
        assert args[1] == self.key

    @patch("app.auth.providers.jwt.encode")
    def test_create_access_token_algorithm(self, mock_jwt_encode):
        """Should call jwt.encode with correct algorithm."""
        mock_jwt_encode.return_value = "mocked-token"

        JwtOAuth2TokenProvider.create_access_token(self.payload)

        args, kwargs = mock_jwt_encode.call_args
        assert kwargs["algorithm"] == self.algorithm

    @patch("app.auth.providers.jwt.decode")
    def test_verify_access_token_happy_path(self, mock_jwt_decode):
        """Should return TokenPayload when given a valid JWT access token."""
        mock_jwt_decode.return_value = {
            "user_id": self.payload.user_id,
            "exp": 1234567890,
        }
        token = "dummy-token"

        result = JwtOAuth2TokenProvider.verify_access_token(
            token, DummyCredentialsException
        )

        assert isinstance(result, TokenPayload)
        assert result.user_id == self.payload.user_id

    @patch("app.auth.providers.jwt.decode")
    def test_verify_access_token_invalid_token(self, mock_jwt_decode):
        """Should raise requested exception if token is invalid."""
        from jose import JWTError

        mock_jwt_decode.side_effect = JWTError
        invalid_token = "invalid.token.value"

        with pytest.raises(DummyCredentialsException):
            JwtOAuth2TokenProvider.verify_access_token(
                invalid_token, DummyCredentialsException
            )

    @patch("app.auth.providers.jwt.decode")
    def test_verify_access_token_missing_user_id(self, mock_jwt_decode):
        """
        Should raise requested exception if user_id is missing in token payload.
        """
        mock_jwt_decode.return_value = {"exp": 1234567890}
        token = "dummy-token"
        with pytest.raises(DummyCredentialsException):
            JwtOAuth2TokenProvider.verify_access_token(token, DummyCredentialsException)
