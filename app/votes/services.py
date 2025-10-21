from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from .exceptions import AlreadyVotedException, VoteNotFoundException
from .models import Vote


class VoteServiceABC(ABC):
    @abstractmethod
    def add_vote(self, post_id: str, db: Session, current_user):
        pass

    @abstractmethod
    def remove_vote(self, post_id: str, db: Session, current_user):
        pass


class VoteService(VoteServiceABC):
    def add_vote(self, post_id: str, db: Session, current_user):
        vote_query = db.query(Vote).filter(
            Vote.post_id == post_id, Vote.user_id == current_user.id
        )
        found_vote = vote_query.first()
        if found_vote:
            raise AlreadyVotedException()
        vote = Vote(post_id=post_id, user_id=current_user.id)
        db.add(vote)
        db.commit()

    def remove_vote(self, post_id: str, db: Session, current_user):
        vote_query = db.query(Vote).filter(
            Vote.post_id == post_id, Vote.user_id == current_user.id
        )
        found_vote = vote_query.first()
        if not found_vote:
            raise VoteNotFoundException()
        vote_query.delete(synchronize_session=False)
        db.commit()
