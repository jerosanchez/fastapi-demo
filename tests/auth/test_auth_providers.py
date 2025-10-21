from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest

from app.auth.models import TokenPayload
from app.auth.providers import JwtOAuth2TokenProvider
from tests.shared.test_helpers import random_string, random_user_id


class DummyCredentialsException(Exception):
    pass


class TestJwtOAuth2TokenProvider:
    def setup_method(self):
        self.jwt_encode_patch = patch("app.auth.providers.jwt.encode")
        self.mock_jwt_encode = self.jwt_encode_patch.start()

        self.jwt_decode_patch = patch("app.auth.providers.jwt.decode")
        self.mock_jwt_decode = self.jwt_decode_patch.start()

        self.settings_patch = patch("app.auth.providers.settings")
        self.mock_settings = self.settings_patch.start()
        self.mock_settings.oauth_hash_key = "some-hash-key"
        self.mock_settings.oauth_algorithm = "HS256"
        self.mock_settings.oauth_token_ttl = 15

    def teardown_method(self):
        self.settings_patch.stop()

    def test_create_access_token_payload_data(self):
        """Should call jwt.encode with correct user id."""
        payload = TokenPayload(user_id=random_user_id())

        JwtOAuth2TokenProvider.create_access_token(payload)

        args, kwargs = self.mock_jwt_encode.call_args
        payload_dict = args[0]

        assert payload_dict["user_id"] == payload.user_id

    def test_create_access_token_expiration_ttl(self):
        """Should call jwt.encode with exp set to now + ttl minutes."""
        payload = TokenPayload(user_id=random_user_id())

        JwtOAuth2TokenProvider.create_access_token(payload)

        args, kwargs = self.mock_jwt_encode.call_args
        payload_dict = args[0]

        returned_exp = payload_dict["exp"]
        now = datetime.now(timezone.utc)
        ttl_in_minutes = self.mock_settings.oauth_token_ttl
        expected_exp = now + timedelta(minutes=ttl_in_minutes)

        # The expiration should be within a one second of now + ttl
        assert abs((returned_exp - expected_exp).total_seconds()) < 1

    def test_create_access_token_hash_key(self):
        """Should call jwt.encode with correct hash key."""
        payload = TokenPayload(user_id=random_user_id())

        JwtOAuth2TokenProvider.create_access_token(payload)

        args, kwargs = self.mock_jwt_encode.call_args
        assert args[1] == self.mock_settings.oauth_hash_key

    def test_create_access_token_algorithm(self):
        """Should call jwt.encode with correct algorithm."""
        payload = TokenPayload(user_id=random_user_id())

        JwtOAuth2TokenProvider.create_access_token(payload)

        args, kwargs = self.mock_jwt_encode.call_args
        assert kwargs["algorithm"] == self.mock_settings.oauth_algorithm

    def test_verify_access_token_happy_path(self):
        """Should return TokenPayload when given a valid JWT access token."""
        user_id = random_user_id()
        valid_token = random_string()

        self.mock_jwt_decode.return_value = {
            "user_id": user_id,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=1),
        }

        returned_payload = JwtOAuth2TokenProvider.verify_access_token(
            valid_token, DummyCredentialsException
        )

        assert returned_payload.user_id == user_id

    def test_verify_access_token_invalid_token(self):
        """Should raise requested exception if token is invalid."""
        some_token = random_string()

        from jose import JWTError

        self.mock_jwt_decode.side_effect = JWTError

        with pytest.raises(DummyCredentialsException):
            JwtOAuth2TokenProvider.verify_access_token(
                some_token, DummyCredentialsException
            )

    def test_verify_access_token_missing_user_id(self):
        """
        Should raise requested exception if user_id is missing in token payload.
        """
        some_token = random_string()

        self.mock_jwt_decode.return_value = {
            "exp": datetime.now(timezone.utc) + timedelta(minutes=1),
            "user_id": None,
        }

        with pytest.raises(DummyCredentialsException):
            JwtOAuth2TokenProvider.verify_access_token(
                some_token, DummyCredentialsException
            )
