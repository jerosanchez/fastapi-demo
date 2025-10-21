from fastapi import APIRouter

from .routes import VoteRoutes
from .use_cases import VotesUseCaseABC, VoteUseCase


def build_votes_router() -> APIRouter:
    votes_use_case = VoteUseCase()
    return VoteRoutes(votes_use_case).router
