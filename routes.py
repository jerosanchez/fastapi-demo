from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import utils
from database import get_db
from schemas import PostCreate, PostOut, PostUpdate, UserCreate, UserOut

router = APIRouter()


### Posts routes


@router.get("/posts", response_model=dict[str, list[PostOut]])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@router.post(
    "/posts",
    status_code=status.HTTP_201_CREATED,
    response_model=dict[str, PostOut],
)
async def create_post(post_data: PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post_data.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@router.get("/posts/{post_id}", response_model=dict[str, PostOut])
async def get_post_by_id(post_id: str, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        _report_not_found(post_id)
    return {"data": post}


@router.patch(
    "/posts/{post_id}",
    response_model=dict[str, PostOut],
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_post(
    post_id: str, post_data: PostUpdate, db: Session = Depends(get_db)
):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if not post:
        _report_not_found(post_id)
    post_query.update(post_data.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(post)
    return {"data": post}


@router.delete(
    "/posts/{post_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_post(post_id: str, db: Session = Depends(get_db)) -> None:
    db.query(models.Post).filter(models.Post.id == post_id).delete()
    db.commit()
    return


### Users routes


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


### Helper functions


def _report_not_found(id: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found, id: {id}"
    )
