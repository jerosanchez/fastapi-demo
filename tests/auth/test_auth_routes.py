from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from app.auth.exceptions import PasswordVerificationException, UserNotFoundException
from app.auth.models import Token
from app.auth.routes import AuthRouter
from app.auth.use_cases import AuthenticateUserUseCaseABC


class MockAuthenticateUserUseCase(AuthenticateUserUseCaseABC):
    def __init__(self):
        self.should_raise: Exception | None = None
        self.token: Token | None = None

    def execute(self, db, username, password) -> Token:
        if self.should_raise:
            raise self.should_raise
        if self.token is not None:
            return self.token
        return Token(access_token="dummy", token_type="bearer")


class TestAuthRouter:
    def setup_method(self):
        """
        Setup AuthRouter and FastAPI app for each test.
        """
        self.authenticate_user_use_case = MockAuthenticateUserUseCase()
        self.auth_router = AuthRouter(self.authenticate_user_use_case)
        self.app = FastAPI()
        self.app.include_router(self.auth_router.router)
        self.client = TestClient(self.app)

    def test_login_happy_path(self):
        """
        Should return valid token when credentials are correct.
        """
        token = Token(access_token="abc123", token_type="bearer")
        self.authenticate_user_use_case.token = token

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
        Should raise 403 error when user is not found.
        """
        self.authenticate_user_use_case.should_raise = UserNotFoundException()

        response = self.client.post(
            "/login",
            data={"username": "nouser", "password": "pass"},
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json()["detail"] == "Invalid email or password"

    def test_login_password_verification_error(self):
        """
        Should raise 403 error when password verification fails.
        """
        self.authenticate_user_use_case.should_raise = PasswordVerificationException()

        response = self.client.post(
            "/login",
            data={"username": "user", "password": "wrongpass"},
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json()["detail"] == "Invalid email or password"
