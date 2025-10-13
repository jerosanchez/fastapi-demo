from fastapi import FastAPI

import models
from database import engine
from routes import router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(router)
