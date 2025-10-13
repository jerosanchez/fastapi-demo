from fastapi import FastAPI

import app.models as models
from app.database import engine
from app.posts.routes import router as posts_router
from app.routes import router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(router)
app.include_router(posts_router)
