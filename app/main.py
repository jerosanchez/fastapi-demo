from fastapi import FastAPI

import app.posts.models as posts_models
import app.users.models as users_models
from app.core.database import engine
from app.posts.routes import router as posts_router
from app.users.routes import router as users_router

app = FastAPI()

posts_models.Base.metadata.create_all(bind=engine)
app.include_router(posts_router)

users_models.Base.metadata.create_all(bind=engine)
app.include_router(users_router)
