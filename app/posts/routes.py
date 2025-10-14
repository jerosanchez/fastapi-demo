from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import oauth2
from app.core.database import get_db
from app.users.models import User

from .models import Post
from .schemas import PostCreate, PostOut, PostUpdate

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=dict[str, list[PostOut]])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return {"data": posts}


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=dict[str, PostOut],
)
async def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
):
    new_post = Post(**post_data.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@router.get("/{post_id}", response_model=dict[str, PostOut])
async def get_post_by_id(post_id: str, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        _report_not_found(post_id)
    return {"data": post}


@router.patch(
    "/{post_id}",
    response_model=dict[str, PostOut],
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_post(
    post_id: str,
    post_data: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
):
    post_query = db.query(Post).filter(Post.id == post_id)
    post = post_query.first()
    if not post:
        _report_not_found(post_id)
    post_query.update(post_data.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(post)
    return {"data": post}


@router.delete(
    "/{post_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_post(
    post_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
) -> None:
    db.query(Post).filter(Post.id == post_id).delete()
    db.commit()
    return


### Helper functions


def _report_not_found(id: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found, id: {id}"
    )
