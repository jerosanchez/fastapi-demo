from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from app.auth.exceptions import PasswordVerificationException, UserNotFoundException
from app.auth.models import Token
from app.auth.routes import AuthRouter
from app.auth.use_cases import AuthenticateUserUseCaseABC

from ..shared.test_helpers import random_password, random_string, random_user_id


class MockAuthenticateUserUseCase(AuthenticateUserUseCaseABC):
    def __init__(self):
        self.should_raise: Exception | None = None
        self.return_value: Token | None = None

    def execute(self, db, username, password) -> Token:
        if self.should_raise:
            raise self.should_raise
        return self.return_value or Token(access_token="dummy", token_type="bearer")


class TestAuthRouter:
    def setup_method(self):
        """
        Setup AuthRouter and FastAPI app for each test.
        """
        self.authenticate_user_use_case_mock = MockAuthenticateUserUseCase()
        self.sut = AuthRouter(self.authenticate_user_use_case_mock)
        self.app = FastAPI()
        self.app.include_router(self.sut.router)
        self.client = TestClient(self.app)

    def test_login_happy_path(self):
        """
        Should return valid token when credentials are correct.
        """
        token = Token(access_token=random_string(), token_type="bearer")

        self.authenticate_user_use_case_mock.return_value = token

        response = self.client.post(
            "/login",
            data={"username": "user", "password": "pass"},
        )

        assert response.status_code == status.HTTP_200_OK

        assert response.json() == {
            "access_token": token.access_token,
            "token_type": token.token_type,
        }

    def test_login_user_not_found(self):
        """
        Should return 403 error when user is not found.
        """
        non_existent_user_id = random_string()

        self.authenticate_user_use_case_mock.should_raise = UserNotFoundException()

        response = self.client.post(
            "/login",
            data={"username": non_existent_user_id, "password": random_password()},
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

        assert response.json() == {"detail": "Invalid email or password"}

    def test_login_password_verification_error(self):
        """
        Should return 403 error when password verification fails.
        """
        wrong_password = random_password()

        self.authenticate_user_use_case_mock.should_raise = (
            PasswordVerificationException()
        )

        response = self.client.post(
            "/login",
            data={"username": random_user_id(), "password": wrong_password},
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

        assert response.json() == {"detail": "Invalid email or password"}
