from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import auth, posts, users, votes

app = FastAPI()

# Allowed origins for CORS
allowed_origins = [
    "*",  # Allows all origins, maybe too permissive for production
    # "https://www.google.com",  # Example, adjust as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

posts.init_service(app)
users.init_service(app)
auth.init_service(app)
votes.init_service(app)
