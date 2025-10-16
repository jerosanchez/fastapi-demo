from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import auth, posts, users, votes
from app.core.database import engine

app = FastAPI()

# Allowed origins for CORS
allowed_origins = [
    "*",  # Allows all origins, maybe too permissive for production
    # "https://www.google.com",  # Example of an allowed origin, adjust as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

posts.init_service(app, engine)
users.init_service(app, engine)
auth.init_service(app, engine)
votes.init_service(app, engine)
