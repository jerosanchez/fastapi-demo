from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies.database import get_db

from .exceptions import EmailAlreadyExistsException
from .schemas import UserCreate, UserOut
from .use_cases import CreateUserUseCaseABC, GetUserByIdUseCaseABC


class UserRoutes:
    def __init__(
        self,
        create_user_use_case: CreateUserUseCaseABC,
        get_user_by_id_use_case: GetUserByIdUseCaseABC,
    ):
        self.create_user_use_case = create_user_use_case
        self.get_user_by_id_use_case = get_user_by_id_use_case

        self.router = APIRouter(prefix="/users", tags=["Users"])
        self._build_routes()

    # === Public Route Handlers ===

    def create_user(self, user_data: UserCreate, db: Session = Depends(get_db)):
        """
        Handle user creation.
        """
        try:
            user = self.create_user_use_case.execute(user_data.model_dump(), db)
            return {"data": user}
        except EmailAlreadyExistsException:
            self._report_user_exists(str(user_data.email))

    def get_user_by_id(self, user_id: str, db: Session = Depends(get_db)):
        """
        Handle fetching a user by ID.
        """
        user = self.get_user_by_id_use_case.execute(user_id, db)
        if user is None:
            self._report_user_not_found(user_id)
        return {"data": user}

    # === Private Helpers ===

    def _build_routes(self):
        """
        Register route handlers on the router.
        """
        self.router.post(
            "/",
            status_code=201,
            response_model=dict[str, UserOut],
        )(self.create_user)
        self.router.get("/{user_id}", response_model=dict[str, UserOut])(
            self.get_user_by_id
        )

    @staticmethod
    def _report_user_exists(email: str):
        """
        Raise HTTP 400 if user already exists.
        """
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {email} already exists",
        )

    @staticmethod
    def _report_user_not_found(user_id: str):
        """
        Raise HTTP 404 if user is not found.
        """
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found, id: {user_id}",
        )
