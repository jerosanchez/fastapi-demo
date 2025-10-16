from . import models
from .routes import router


def init_service(app, engine):
    models.Base.metadata.create_all(bind=engine)
    app.include_router(router)
