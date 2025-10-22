from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.posts.models import Post

from .models import Vote


class VoteRepositoryABC(ABC):
    @abstractmethod
    def get_vote(self, post_id: str, user_id: str, db: Session) -> Vote:
        """Return a vote for a post/user, or None if not found."""
        pass

    @abstractmethod
    def add_vote(self, post_id: str, user_id: str, db: Session) -> None:
        """Add a vote for a post/user."""
        pass

    @abstractmethod
    def remove_vote(self, post_id: str, user_id: str, db: Session) -> None:
        """Remove a vote for a post/user."""
        pass


class VoteRepository(VoteRepositoryABC):
    def get_vote(self, post_id: str, user_id: str, db: Session) -> Vote:
        return (
            db.query(Vote)
            .filter(Vote.post_id == post_id, Vote.user_id == user_id)
            .first()
        )

    def add_vote(self, post_id: str, user_id: str, db: Session) -> None:
        vote = Vote(post_id=post_id, user_id=user_id)
        db.add(vote)
        db.commit()

    def remove_vote(self, post_id: str, user_id: str, db: Session) -> None:
        db.query(Vote).filter(Vote.post_id == post_id, Vote.user_id == user_id).delete(
            synchronize_session=False
        )
        db.commit()


class PostRepositoryABC(ABC):
    @abstractmethod
    def get_post(self, post_id: str, db: Session) -> Post | None:
        pass


class PostRepository(PostRepositoryABC):
    def get_post(self, post_id: str, db: Session) -> Post | None:
        return db.query(Post).filter(Post.id == post_id).first()
