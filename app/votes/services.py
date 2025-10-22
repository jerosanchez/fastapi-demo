from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.posts.exceptions import ForbiddenException

from .exceptions import (
    AlreadyVotedException,
    PostNotFoundException,
    VoteNotFoundException,
)
from .policies import VotePolicy
from .repositories import PostRepositoryABC, VoteRepositoryABC


class VoteServiceABC(ABC):
    @abstractmethod
    def add_vote(self, post_id: str, db: Session, current_user):
        pass

    @abstractmethod
    def remove_vote(self, post_id: str, db: Session, current_user):
        pass


class VoteService(VoteServiceABC):
    def __init__(
        self,
        vote_repository: VoteRepositoryABC,
        vote_policy: VotePolicy,
        post_repository: PostRepositoryABC,
    ):
        self._vote_repository = vote_repository
        self._vote_policy = vote_policy
        self._post_repository = post_repository

    def add_vote(self, post_id: str, db: Session, current_user):
        self._enforce_policies(post_id, db, current_user)
        found_vote = self._vote_repository.get_vote(post_id, current_user.id, db)
        if found_vote:
            raise AlreadyVotedException()
        self._vote_repository.add_vote(post_id, current_user.id, db)

    def remove_vote(self, post_id: str, db: Session, current_user):
        self._enforce_policies(post_id, db, current_user)
        found_vote = self._vote_repository.get_vote(post_id, current_user.id, db)
        if not found_vote:
            raise VoteNotFoundException()
        self._vote_repository.remove_vote(post_id, current_user.id, db)

    def _enforce_policies(self, post_id: str, db: Session, current_user):
        post = self._post_repository.get_post(post_id, db)
        if not post:
            raise PostNotFoundException()
        if not self._vote_policy.can_vote(post, current_user):
            raise ForbiddenException()
