from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.votes.models import Vote

from .exceptions import AlreadyVotedException, VoteNotFoundException


class VotesUseCaseABC(ABC):
    @abstractmethod
    def vote(
        self, post_id: str, vote_direction: int, db: Session, current_user
    ) -> None:
        pass


class VoteUseCase(VotesUseCaseABC):
    def vote(
        self, post_id: str, vote_direction: int, db: Session, current_user
    ) -> None:
        vote_query = db.query(Vote).filter(
            Vote.post_id == post_id, Vote.user_id == current_user.id
        )
        found_vote = vote_query.first()

        if vote_direction:  # 1 (upvote)
            if found_vote:
                raise AlreadyVotedException()
            vote = Vote(post_id=post_id, user_id=current_user.id)
            db.add(vote)

        else:  # 0 (remove vote)
            if not found_vote:
                raise VoteNotFoundException()
            vote_query.delete(synchronize_session=False)

        db.commit()

        return None
