from fastapi import FastAPI

from app import auth, posts, users
from app.core.database import engine

app = FastAPI()

posts.init_app(app, engine)
users.init_app(app, engine)
auth.init_app(app, engine)
