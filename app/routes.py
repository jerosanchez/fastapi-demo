from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.models as models
import app.utils as utils
from app.database import get_db
from app.schemas import UserCreate, UserOut

router = APIRouter()


@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=dict[str, UserOut],
)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user_data.email} already exists",
        )

    # Replace plain password with hashed password
    user_data.password = utils.hash_password(user_data.password)

    new_user = models.User(**user_data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"data": new_user}


@router.get("/users/{user_id}", response_model=dict[str, UserOut])
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        _report_not_found(user_id)
    return {"data": user}


### Helper functions


def _report_not_found(id: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found, id: {id}"
    )
