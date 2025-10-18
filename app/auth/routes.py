from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.oauth2 import create_access_token
from app.core.database import get_db
from app.users.models import User
from app.utils.passwords import verify_password

from .schemas import Token, TokenPayload


class AuthRouter:
    def __init__(self):
        self.router = APIRouter(tags=["Authentication"])
        self.router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)(
            self.login
        )

    def login(
        self,
        credentials: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
    ):
        user = db.query(User).filter(User.email == credentials.username).first()

        if not user:
            self._report_invalid_login()

        if not verify_password(credentials.password, user.password):
            self._report_invalid_login()

        access_token = create_access_token(payload=TokenPayload(user_id=user.id))

        return Token(access_token=access_token, token_type="bearer")

    @staticmethod
    def _report_invalid_login():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid email or password",
        )
