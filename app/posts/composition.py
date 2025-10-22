from fastapi import APIRouter

from .policies import PostPolicy
from .repositories import PostRepository
from .routes import PostsRoutes
from .services import PostService
from .use_cases import (
    CreatePostUseCase,
    DeletePostUseCase,
    GetPostByIdUseCase,
    GetPostsUseCase,
    UpdatePostUseCase,
)


def build_posts_router() -> APIRouter:
    post_repository = PostRepository()
    post_policy = PostPolicy()
    post_service = PostService(post_repository, post_policy)
    get_posts_use_case = GetPostsUseCase(post_service)
    create_post_use_case = CreatePostUseCase(post_service)
    get_post_by_id_use_case = GetPostByIdUseCase(post_service)
    update_post_use_case = UpdatePostUseCase(post_service)
    delete_post_use_case = DeletePostUseCase(post_service)

    return PostsRoutes(
        get_posts_use_case,
        create_post_use_case,
        get_post_by_id_use_case,
        update_post_use_case,
        delete_post_use_case,
    ).router
