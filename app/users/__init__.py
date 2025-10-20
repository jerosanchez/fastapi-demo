from .composition import build_user_router


def init_service(app):
    app.include_router(build_user_router())
