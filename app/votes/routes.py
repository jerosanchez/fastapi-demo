from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies.current_user import get_current_user
from app.core.dependencies.database import get_db
from app.posts.exceptions import ForbiddenException
from app.users.models import User

from .exceptions import (
    AlreadyVotedException,
    PostNotFoundException,
    VoteNotFoundException,
)
from .schemas import VotePost
from .use_cases import VotesUseCaseABC


class VoteRoutes:
    def __init__(self, vote_use_case: VotesUseCaseABC):
        self._vote_use_case = vote_use_case
        self.router = APIRouter(prefix="/votes", tags=["Votes"])
        self._build_routes()

    def vote(
        self,
        vote_data: VotePost,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):

        try:
            post_id = str(vote_data.post_id)
            vote_direction = vote_data.vote_direction
            self._vote_use_case.execute(post_id, vote_direction, db, current_user)
            return

        except PostNotFoundException:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post does not exist",
            )

        except ForbiddenException:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to vote on this post",
            )

        except AlreadyVotedException:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User has already voted on this post",
            )

        except VoteNotFoundException:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist",
            )

    def _build_routes(self):
        self.router.post("/", status_code=status.HTTP_204_NO_CONTENT)(self.vote)
