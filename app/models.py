# Import all model classes here so Alembic can discover them
from .users.models import User
from .posts.models import Post
from .votes.models import Vote

__all__ = ["User", "Post", "Vote"]
