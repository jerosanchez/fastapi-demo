from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from . import auth, posts, users, votes

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


# As per ADR-0004: centralized exception handling for infrastructure errors
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "Database error. Please try again later."},
    )


# Mount feature routers
posts.init_service(app)
users.init_service(app)
auth.init_service(app)
votes.init_service(app)
