from unittest.mock import Mock

from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from app.users.exceptions import EmailAlreadyExistsException
from app.users.models import User
from app.users.routes import UserRoutes
from app.users.schemas import UserOut
from app.users.use_cases import CreateUserUseCaseABC, GetUserByIdUseCaseABC

from ..shared.test_helpers import make_stored_user, random_user_id


class TestUserRoutes:
    def setup_method(self):
        self.create_user_use_case_mock = Mock(spec=CreateUserUseCaseABC)
        self.get_user_by_id_use_case_mock = Mock(spec=GetUserByIdUseCaseABC)
        self.sut = UserRoutes(
            self.create_user_use_case_mock, self.get_user_by_id_use_case_mock
        )
        self.app = FastAPI()
        self.app.include_router(self.sut.router)
        self.client = TestClient(self.app)

    def test_create_user_happy_path(self):
        """Should return new user when data is valid."""
        new_user = make_stored_user()

        self.create_user_use_case_mock.execute.return_value = new_user

        response = self.client.post(
            "/users/", json={"email": new_user.email, "password": new_user.password}
        )
        returned_user = _extract_user_out_from_response(response)

        assert response.status_code == status.HTTP_201_CREATED

        _assert_user_equals(returned_user, new_user)

    def test_create_user_email_exists(self):
        """
        Should return 400 BAD REQUEST if email already exists.
        """
        new_user = make_stored_user()
        self.create_user_use_case_mock.execute.side_effect = (
            EmailAlreadyExistsException()
        )

        response = self.client.post(
            "/users/", json={"email": new_user.email, "password": new_user.password}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert response.json() == {
            "detail": f"User with email {new_user.email} already exists"
        }

    def test_get_user_by_id_happy_path(self):
        """
        Should return user data when user exists.
        """
        stored_user = make_stored_user()

        self.get_user_by_id_use_case_mock.execute.return_value = stored_user

        response = self.client.get(f"/users/{stored_user.id}")
        returned_user = _extract_user_out_from_response(response)

        assert response.status_code == status.HTTP_200_OK

        _assert_user_equals(returned_user, stored_user)

    def test_get_user_by_id_not_found(self):
        """
        Should return 404 NOT FOUND if user not found.
        """
        user_id = random_user_id()

        self.get_user_by_id_use_case_mock.execute.return_value = None

        response = self.client.get(f"/users/{user_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND

        assert response.json() == {"detail": f"User not found, id: {user_id}"}


# === Helper functions ===


def _extract_user_out_from_response(response) -> UserOut:
    response_data = response.json()["data"]
    return UserOut(**response_data)


def _assert_user_equals(user_out: UserOut, user: User):
    assert str(user_out.id) == str(user.id)
    assert user_out.email == user.email
    assert user_out.is_active == user.is_active
    assert str(user_out.created_at) == user.created_at
