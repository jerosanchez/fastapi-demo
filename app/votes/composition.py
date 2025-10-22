from fastapi import APIRouter

from .policies import VotePolicy
from .repositories import PostRepository, VoteRepository
from .routes import VoteRoutes
from .services import VoteService
from .use_cases import VoteUseCase


def build_votes_router() -> APIRouter:
    vote_repository = VoteRepository()
    post_repository = PostRepository()
    vote_policy = VotePolicy()
    vote_service = VoteService(vote_repository, vote_policy, post_repository)
    votes_use_case = VoteUseCase(vote_service)
    return VoteRoutes(votes_use_case).router
