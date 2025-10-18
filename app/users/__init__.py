from .routes import router


def init_service(app):
    app.include_router(router)
