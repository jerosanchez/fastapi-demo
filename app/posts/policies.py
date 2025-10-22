from app.users.models import User

from .models import Post


class PostPolicy:
    @staticmethod
    def can_view(post: Post, user: User) -> bool:
        return True

    @staticmethod
    def can_create(user: User) -> bool:
        return bool(user.is_active)

    @staticmethod
    def can_update(post: Post, user: User) -> bool:
        return str(post.owner_id) == str(user.id)

    @staticmethod
    def can_delete(post: Post, user: User) -> bool:
        return str(post.owner_id) == str(user.id)
