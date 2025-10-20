from .composition import user_routes


def init_service(app):
    app.include_router(user_routes.router)
