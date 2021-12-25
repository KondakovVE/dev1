from functools import lru_cache
from typing import cast
from . import config
from . import databases
from sqlalchemy.orm import Session


def get_db() -> Session:
    db = databases.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lru_cache
def get_db_settings() -> config.DBSettings:
    return config.DBSettings()
