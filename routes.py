from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
from database import get_db
from mappers import to_post_out
from schemas import PostCreate, PostOut, PostUpdate

router = APIRouter()


@router.get("/posts")
async def get_posts(db: Session = Depends(get_db)) -> dict[str, list[PostOut]]:
    posts = db.query(models.Post).all()
    return {"data": [to_post_out(post) for post in posts]}


@router.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate, db: Session = Depends(get_db)
) -> dict[str, PostOut]:
    new_post = models.Post(**post_data.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": to_post_out(new_post)}


@router.get("/posts/{post_id}")
async def get_post_by_id(
    post_id: str, db: Session = Depends(get_db)
) -> dict[str, PostOut]:
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        _report_not_found(post_id)
    return {"data": post}


@router.patch("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_post(
    post_id: str, post_data: PostUpdate, db: Session = Depends(get_db)
) -> dict[str, PostOut]:
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if not post:
        _report_not_found(post_id)
    post_query.update(post_data.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(post)
    return {"data": to_post_out(post)}


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: str, db: Session = Depends(get_db)) -> None:
    db.query(models.Post).filter(models.Post.id == post_id).delete()
    db.commit()
    return


def _report_not_found(id: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found, id: {id}"
    )
