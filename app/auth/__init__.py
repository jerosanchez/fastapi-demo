# from . import models
from .routes import router


def init_app(app, engine):
    # models.Base.metadata.create_all(bind=engine)
    app.include_router(router)
