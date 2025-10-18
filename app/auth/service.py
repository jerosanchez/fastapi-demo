from sqlalchemy.orm import Session

from app.auth.oauth2 import create_access_token
from app.users.models import User
from app.utils.passwords import verify_password

from .exceptions import PasswordVerificationException, UserNotFoundException
from .models import Token, TokenPayload


class AuthService:
    def authenticate_user(self, db: Session, username: str, password: str) -> Token:
        user = db.query(User).filter(User.email == username).first()

        if not user:
            raise UserNotFoundException()

        if not verify_password(password, user.password):
            raise PasswordVerificationException()

        access_token = create_access_token(payload=TokenPayload(user_id=user.id))

        return Token(access_token=access_token, token_type="bearer")
