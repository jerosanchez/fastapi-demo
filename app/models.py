# Import all model classes here so Alembic can discover them
from .posts.models import Post
from .users.models import User
from .votes.models import Vote

__all__ = ["User", "Post", "Vote"]
