from fastapi import APIRouter

from .routes import PostsRoutes


def build_posts_router() -> APIRouter:
    return PostsRoutes().router
