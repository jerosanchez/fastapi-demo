from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db

from .models import Token
from .schemas import TokenOut
from .service import AuthService


class AuthRouter:
    def __init__(self, service: AuthService):
        self.service = service
        self.router = APIRouter(tags=["Authentication"])
        self.router.post(
            "/login", status_code=status.HTTP_200_OK, response_model=TokenOut
        )(self.login)

    def login(
        self,
        credentials: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
    ):
        token: Token = self.service.authenticate_user(
            db, credentials.username, credentials.password
        )
        if not token:
            self._report_invalid_login()
        return TokenOut(access_token=token.access_token, token_type=token.token_type)

    @staticmethod
    def _report_invalid_login():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid email or password",
        )
