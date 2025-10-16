from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.utils.passwords import hash_password

from . import models
from .schemas import UserCreate, UserOut

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=dict[str, UserOut],
)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    if (
        db.query(models.User)
        .filter(models.User.email == user_data.email)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user_data.email} already exists",
        )

    user_data.password = hash_password(user_data.password)

    new_user = models.User(**user_data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"data": new_user}


@router.get("/{user_id}", response_model=dict[str, UserOut])
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post not found, id: {id}",
        )
    return {"data": user}
