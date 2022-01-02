from fastapi import FastAPI

from app.databases import Model, engine
from routers import speedster, users

from loguru import logger

logger.debug('init')
Model.metadata.create_all(bind=engine)
logger.debug('model metadata was created')

app = FastAPI()
logger.debug('app init')
app.include_router(speedster.router)
logger.debug('speedster router added')
app.include_router(users.router)
logger.debug('users router added')
