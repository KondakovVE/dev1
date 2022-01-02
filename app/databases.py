from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.dependencies import get_db_settings
from loguru import logger
import os


settings = get_db_settings()
logger.debug('Загружены настройки бд')

if os.environ.get("TESTING"):
    logger.debug('Запуск в режиме тестов. Чистим БД')
    SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.username}:{settings.password}@{settings.host}:{settings.port}/postgres"

    engine = create_engine(SQLALCHEMY_DATABASE_URL,
                           isolation_level="AUTOCOMMIT")
    logger.debug('Создан движой SQLAlchemy для сброса базы')
    with engine.connect() as connect:
        connect.execute(f"DROP DATABASE IF EXISTS {settings.database}_test")
        logger.debug('Тестовая база сброшена')
        connect.execute(f"CREATE DATABASE {settings.database}_test")
        logger.debug('Тестовая база создана снова')

    logger.debug('Подготовка тестового контура завершена')
    SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.username}:{settings.password}@{settings.host}:{settings.port}/{settings.database}_test"
else:
    logger.debug('Запуск в рабочем режиме')
    SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.username}:{settings.password}@{settings.host}:{settings.port}/{settings.database}"


logger.debug(f'SQLALCHEMY_DATABASE_URL: {SQLALCHEMY_DATABASE_URL}')

engine = create_engine(SQLALCHEMY_DATABASE_URL)
logger.debug(f'engine created')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger.debug(f'session created')

Model = declarative_base()
logger.debug(f'model created')
