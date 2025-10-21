from fastapi import APIRouter

from .repositories import VoteRepository
from .routes import VoteRoutes
from .services import VoteService
from .use_cases import VoteUseCase


def build_votes_router() -> APIRouter:
    vote_repository = VoteRepository()
    vote_service = VoteService(vote_repository)
    votes_use_case = VoteUseCase(vote_service)
    return VoteRoutes(votes_use_case).router
