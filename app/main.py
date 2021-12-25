from fastapi import FastAPI

from app.databases import Model, engine
from routers import speedster


Model.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(speedster.router)
