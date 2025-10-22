from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.dependencies.current_user import get_current_user
from app.core.dependencies.database import get_db
from app.users.models import User

from .exceptions import ForbiddenException
from .models import CreatePostData, UpdatePostData
from .schemas import PostCreate, PostOut, PostUpdate, PostWithVotes
from .use_cases import (
    CreatePostUseCase,
    DeletePostUseCase,
    GetPostByIdUseCase,
    GetPostsUseCase,
    UpdatePostUseCase,
)


class PostsRoutes:
    def __init__(
        self,
        get_posts_use_case: GetPostsUseCase,
        create_post_use_case: CreatePostUseCase,
        get_post_by_id_use_case: GetPostByIdUseCase,
        update_post_use_case: UpdatePostUseCase,
        delete_post_use_case: DeletePostUseCase,
    ):
        self._get_posts_use_case = get_posts_use_case
        self._create_post_use_case = create_post_use_case
        self._get_post_by_id_use_case = get_post_by_id_use_case
        self._update_post_use_case = update_post_use_case
        self._delete_post_use_case = delete_post_use_case

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
        posts = self._get_posts_use_case.execute(page, size, search, db)
        response_data = [
            PostWithVotes(Post=PostOut.model_validate(post), votes=votes)
            for post, votes in posts
        ]
        return {"data": response_data}

    def create_post(
        self,
        post_data: PostCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        new_post = self._create_post_use_case.execute(
            _build_create_post_data(post_data), db, current_user
        )
        return {"data": new_post}

    def get_post_by_id(
        self,
        post_id: str,
        db: Session = Depends(get_db),
    ):
        post = self._get_post_by_id_use_case.execute(post_id, db)
        if not post:
            _report_not_found(post_id)
        post_out = PostOut.model_validate(post)
        return {"data": post_out}

    def update_post(
        self,
        post_id: str,
        post_data: PostUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        try:
            post = self._update_post_use_case.execute(
                post_id, _build_update_post_data(post_data), db, current_user
            )
            if post is None:
                _report_not_found(post_id)

            return {"data": post}

        except ForbiddenException:
            _report_forbidden()

    def delete_post(
        self,
        post_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ) -> None:
        try:
            result = self._delete_post_use_case.execute(post_id, db, current_user)
            if result is None:
                _report_not_found(post_id)

            return

        except ForbiddenException:
            _report_forbidden()

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
            response_model=dict[str, PostOut],
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


def _build_create_post_data(post_data: PostCreate) -> CreatePostData:
    return CreatePostData(
        title=getattr(post_data, "title"),
        content=getattr(post_data, "content"),
        published=getattr(post_data, "published"),
        rating=getattr(post_data, "rating"),
    )


def _build_update_post_data(post_data: PostUpdate) -> UpdatePostData:
    return UpdatePostData(
        title=getattr(post_data, "title"),
        content=getattr(post_data, "content"),
        published=getattr(post_data, "published"),
        rating=getattr(post_data, "rating"),
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
