from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.oauth2 import create_access_token
from app.core.database import get_db
from app.users import models
from app.utils.passwords import verify_password

from .schemas import UserLogin

router = APIRouter(tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_200_OK)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()

    if not user:
        _report_invalid_login()

    if not verify_password(credentials.password, user.password):
        _report_invalid_login()

    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


# Helper functions


def _report_invalid_login():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
    )
