from models import Post
from schemas import PostResponse


def to_post_response(post: Post) -> PostResponse:
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        published=post.published,
        rating=post.rating,
        created_at=post.created_at,
    )
