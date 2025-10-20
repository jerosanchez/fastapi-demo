import uuid
from datetime import datetime, timezone

from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.users.exceptions import EmailAlreadyExistsException
from app.users.models import NewUserData, User
from app.users.routes import UserRoutes
from app.users.schemas import UserOut
from app.users.use_cases import CreateUserUseCaseABC, GetUserByIdUseCaseABC


class MockCreateUserUseCase(CreateUserUseCaseABC):
    def __init__(self):
        self.should_raise: Exception | None = None
        self.user: User | None = None

    def execute(self, new_user_data: NewUserData, db: Session):
        if self.should_raise:
            raise self.should_raise
        return self.user or User(id="user-1", email=new_user_data.email, is_active=True)


class MockGetUserByIdUseCase(GetUserByIdUseCaseABC):
    def __init__(self):
        self.user: User | None = None

    def execute(self, user_id: str, db: Session):
        return self.user


class TestUserRoutes:
    def setup_method(self):
        self.create_user_use_case_mock = MockCreateUserUseCase()
        self.get_user_by_id_use_case_mock = MockGetUserByIdUseCase()
        self.user_routes = UserRoutes(
            self.create_user_use_case_mock, self.get_user_by_id_use_case_mock
        )
        self.app = FastAPI()
        self.app.include_router(self.user_routes.router)
        self.client = TestClient(self.app)

    def test_create_user_happy_path(self):
        """Should return new user when data is valid."""
        user_id = uuid.uuid4()
        new_user = User(
            id=user_id,
            email="new@example.com",
            is_active=True,
            created_at=self._now_with_tz(),
        )
        self.create_user_use_case_mock.user = new_user

        response = self.client.post(
            "/users/", json={"email": "new@example.com", "password": "pass"}
        )

        assert response.status_code == status.HTTP_201_CREATED

        response_data = response.json()["data"]
        returned_user = UserOut(**response_data)

        assert returned_user.id == new_user.id
        assert returned_user.email == new_user.email
        assert returned_user.is_active == new_user.is_active
        assert returned_user.created_at == new_user.created_at

    def test_create_user_email_exists(self):
        """
        Should return 400 BAD REQUEST if email already exists.
        """
        self.create_user_use_case_mock.should_raise = EmailAlreadyExistsException()

        response = self.client.post(
            "/users/", json={"email": "existing@example.com", "password": "pass"}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.json()["detail"]
            == "User with email existing@example.com already exists"
        )

    def test_get_user_by_id_happy_path(self):
        """
        Should return user data when user exists.
        """
        existing_user = User(
            id=uuid.uuid4(),
            email="user@example.com",
            is_active=True,
            created_at=self._now_with_tz(),
        )
        self.get_user_by_id_use_case_mock.user = existing_user

        response = self.client.get(f"/users/{existing_user.id}")

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()["data"]
        returned_user = UserOut(**response_data)

        assert returned_user.id == existing_user.id
        assert returned_user.email == existing_user.email
        assert returned_user.is_active == existing_user.is_active
        assert returned_user.created_at == existing_user.created_at

    def test_get_user_by_id_not_found(self):
        """
        Should return 404 NOT FOUND if user not found.
        """
        non_existing_id = uuid.uuid4()
        self.get_user_by_id_use_case_mock.user = None

        response = self.client.get(f"/users/{non_existing_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == f"User not found, id: {non_existing_id}"

    # === Private Helpers ===

    @staticmethod
    def _now_with_tz():
        """
        Return current time as a timezone-aware datetime object.
        """
        return datetime.now(timezone.utc)
