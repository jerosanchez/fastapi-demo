from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.dependencies.current_user import get_current_user
from app.core.dependencies.database import get_db
from app.users.models import User
from app.votes.models import Vote

from .models import Post
from .schemas import PostCreate, PostOut, PostUpdate, PostWithVotes


class PostsRoutes:
    def __init__(self):
        self.router = APIRouter(prefix="/posts", tags=["Posts"])
        self._build_routes()

    def get_posts(
        self,
        page: int = 1,
        size: int = settings.default_page_size,
        search: str | None = None,
        db: Session = Depends(get_db),
    ):
        if page < 1 or size < 1:
            _report_bad_request("Page and size must be positive integers")
        if size > settings.max_page_size:
            _report_bad_request(f"Size must not exceed {settings.max_page_size}")
        query = self._fetch_posts_with_votes_query(db)
        if search:
            query = query.filter(Post.title.ilike(f"%{search}%"))
        return {"data": query.offset((page - 1) * size).limit(size).all()}

    def create_post(
        self,
        post_data: PostCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        new_post = Post(owner_id=current_user.id, **post_data.model_dump())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return {"data": new_post}

    def get_post_by_id(
        self,
        post_id: str,
        db: Session = Depends(get_db),
    ):
        post = self._fetch_posts_with_votes_query(db).filter(Post.id == post_id).first()
        if not post:
            _report_not_found(post_id)
        return {"data": post}

    def update_post(
        self,
        post_id: str,
        post_data: PostUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        post_query = db.query(Post).filter(Post.id == post_id)
        post = post_query.first()
        if not post:
            _report_not_found(post_id)
        if getattr(post, "owner_id", None) != current_user.id:
            _report_forbidden()
        update_data = {
            getattr(Post, k): v
            for k, v in post_data.model_dump(exclude_unset=True).items()
        }
        post_query.update(update_data)
        db.commit()
        db.refresh(post)
        return {"data": post}

    def delete_post(
        self,
        post_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ) -> None:
        post_query = db.query(Post).filter(Post.id == post_id)
        post = post_query.first()
        if not post:
            _report_not_found(post_id)
        if getattr(post, "owner_id", None) != current_user.id:
            _report_forbidden()
        post_query.delete()
        db.commit()
        return

    def _fetch_posts_with_votes_query(self, db: Session):
        return (
            db.query(Post, func.count(Vote.post_id).label("votes"))
            .join(Vote, Vote.post_id == Post.id, isouter=True)
            .group_by(Post.id)
        )

    def _build_routes(self):
        self.router.add_api_route(
            "/",
            self.get_posts,
            response_model=dict[str, list[PostWithVotes]],
            methods=["GET"],
        )
        self.router.add_api_route(
            "/",
            self.create_post,
            response_model=dict[str, PostOut],
            status_code=status.HTTP_201_CREATED,
            methods=["POST"],
        )
        self.router.add_api_route(
            "/{post_id}",
            self.get_post_by_id,
            response_model=dict[str, PostWithVotes],
            methods=["GET"],
        )
        self.router.add_api_route(
            "/{post_id}",
            self.update_post,
            response_model=dict[str, PostOut],
            status_code=status.HTTP_202_ACCEPTED,
            methods=["PATCH"],
        )
        self.router.add_api_route(
            "/{post_id}",
            self.delete_post,
            response_model=None,
            status_code=status.HTTP_204_NO_CONTENT,
            methods=["DELETE"],
        )


def _report_bad_request(detail: str):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def _report_not_found(id: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post not found, id: {id}",
    )


def _report_forbidden():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized to perform requested action",
    )
