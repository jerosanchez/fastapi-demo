from fastapi import FastAPI

from app import auth, posts, users, votes
from app.core.database import engine

app = FastAPI()

posts.init_service(app, engine)
users.init_service(app, engine)
auth.init_service(app, engine)
votes.init_service(app, engine)
