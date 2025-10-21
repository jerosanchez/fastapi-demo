from fastapi import APIRouter

from .routes import VoteRoutes
from .services import VoteService
from .use_cases import VoteUseCase


def build_votes_router() -> APIRouter:
    vote_service = VoteService()
    votes_use_case = VoteUseCase(vote_service)
    return VoteRoutes(votes_use_case).router
