from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, status

import models
from database import engine
from schemas import PostCreate, PostUpdate, create_random_posts

app = FastAPI()

post_repository = create_random_posts(5)

models.Base.metadata.create_all(bind=engine)


@app.get("/posts")
async def get_posts():
    return {"data": post_repository}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostCreate):
    new_post = {
        "id": uuid4(),
        "title": post_data.title,
        "content": post_data.content,
        "published": post_data.published,
        "rating": post_data.rating,
    }
    post_repository.append(new_post)
    return {"data": new_post}


@app.get("/posts/{post_id}")
async def get_post_by_id(post_id: str):
    uuid = _make_uuid(post_id)

    post = next((post for post in post_repository if post.id == uuid), None)

    if post:
        return {"data": post}
    _report_not_found(post_id)


@app.patch("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_post(post_id: str, post_data: PostUpdate):
    uuid = _make_uuid(post_id)

    for index, post in enumerate(post_repository):
        if post.id == uuid:
            updated_post = post.model_copy()
            updated_post.title = post_data.title
            updated_post.content = post_data.content
            updated_post.published = post_data.published
            updated_post.rating = post_data.rating
            post_repository[index] = updated_post
            return {"data": updated_post}

    _report_not_found(post_id)


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: str):
    uuid = _make_uuid(post_id)

    for index, post in enumerate(post_repository):
        if post.id == uuid:
            post_repository.pop(index)
    return


### Helper functions


def _make_uuid(id: str) -> UUID:
    try:
        return UUID(id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid UUID: {id}"
        )


def _report_not_found(id: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found, id: {id}"
    )
