from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from .exceptions import AlreadyVotedException, VoteNotFoundException
from .repositories import VoteRepositoryABC


class VoteServiceABC(ABC):
    @abstractmethod
    def add_vote(self, post_id: str, db: Session, current_user):
        pass

    @abstractmethod
    def remove_vote(self, post_id: str, db: Session, current_user):
        pass


class VoteService(VoteServiceABC):
    def __init__(self, vote_repository: VoteRepositoryABC):
        self._vote_repository = vote_repository

    def add_vote(self, post_id: str, db: Session, current_user):
        found_vote = self._vote_repository.get_vote(post_id, current_user.id, db)
        if found_vote:
            raise AlreadyVotedException()
        self._vote_repository.add_vote(post_id, current_user.id, db)

    def remove_vote(self, post_id: str, db: Session, current_user):
        found_vote = self._vote_repository.get_vote(post_id, current_user.id, db)
        if not found_vote:
            raise VoteNotFoundException()
        self._vote_repository.remove_vote(post_id, current_user.id, db)
