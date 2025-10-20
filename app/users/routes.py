from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies.database import get_db

from .models import User
from .schemas import UserCreate, UserOut
from .utils import hash_password


class UserRoutes:
    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["Users"])
        self.router.post(
            "/",
            status_code=status.HTTP_201_CREATED,
            response_model=dict[str, UserOut],
        )(self.create_user)
        self.router.get("/{user_id}", response_model=dict[str, UserOut])(
            self.get_user_by_id
        )

    def create_user(self, user_data: UserCreate, db: Session = Depends(get_db)):
        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email {user_data.email} already exists",
            )

        user_data.password = hash_password(user_data.password)

        new_user = User(**user_data.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"data": new_user}

    def get_user_by_id(self, user_id: str, db: Session = Depends(get_db)):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User not found, id: {user_id}",
            )
        return {"data": user}
