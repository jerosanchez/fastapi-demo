from fastapi import APIRouter

from .routes import PostsRoutes
from .use_cases import (
    CreatePostUseCase,
    DeletePostUseCase,
    GetPostByIdUseCase,
    GetPostsUseCase,
    UpdatePostUseCase,
)


def build_posts_router() -> APIRouter:
    get_posts_use_case = GetPostsUseCase()
    create_post_use_case = CreatePostUseCase()
    get_post_by_id_use_case = GetPostByIdUseCase()
    update_post_use_case = UpdatePostUseCase()
    delete_post_use_case = DeletePostUseCase()
    return PostsRoutes(
        get_posts_use_case,
        create_post_use_case,
        get_post_by_id_use_case,
        update_post_use_case,
        delete_post_use_case,
    ).router
