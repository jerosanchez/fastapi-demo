from . import models
from .routes import router


def init_service(app, engine):
    app.include_router(router)
