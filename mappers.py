from models import Post
from schemas import PostOut


def to_post_out(post: Post) -> PostOut:
    return PostOut(
        id=post.id,
        title=post.title,
        content=post.content,
        published=post.published,
        rating=post.rating,
    )
