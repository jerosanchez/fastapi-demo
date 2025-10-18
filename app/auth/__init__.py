from .composition import build_auth_router


def init_service(app):
    app.include_router(build_auth_router())
