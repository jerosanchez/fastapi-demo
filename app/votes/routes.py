from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import oauth2
from app.core.database import get_db
from app.users.models import User
from app.votes.models import Vote
from app.votes.schemas import VotePost

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
async def vote(
    vote_data: VotePost,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
):
    vote_query = db.query(Vote).filter(
        Vote.post_id == str(vote_data.post_id), Vote.user_id == current_user.id
    )

    found_vote = vote_query.first()

    if vote_data.vote_direction:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} has already voted on this post",
            )

        vote = Vote(post_id=str(vote_data.post_id), user_id=current_user.id)

        db.add(vote)

    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist"
            )

        vote_query.delete(synchronize_session=False)

    db.commit()

    return
