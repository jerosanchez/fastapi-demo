# Expose the router for FastAPI app inclusion
from .composition import build_votes_router


def init_service(app):
    app.include_router(build_votes_router())
