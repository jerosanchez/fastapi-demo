from abc import ABC, abstractmethod

from .services import VoteServiceABC


class VotesUseCaseABC(ABC):
    @abstractmethod
    def execute(self, post_id: str, vote_direction: int, db, current_user) -> None:
        pass


class VoteUseCase(VotesUseCaseABC):
    def __init__(self, vote_service: VoteServiceABC):
        self.service = vote_service

    def execute(self, post_id: str, vote_direction: int, db, current_user) -> None:
        if vote_direction:  # 1 = upvote
            self.service.add_vote(post_id, db, current_user)
        else:  # 0 = downvote
            self.service.remove_vote(post_id, db, current_user)
