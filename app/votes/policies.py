from app.posts.models import Post
from app.users.models import User


class VotePolicy:
    @staticmethod
    def can_vote(post: Post, user: User) -> bool:
        return bool(user.is_active) and str(post.owner_id) != user.id
