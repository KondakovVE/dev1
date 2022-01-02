from logging import log
import pytest
from fastapi import FastAPI
from sqlalchemy.orm.session import Session
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from loguru import logger

import os


@pytest.fixture(scope="session")
def apply_migration():
    os.environ["TESTING"] = "1"


@pytest.fixture(scope="session")
def app(apply_migration: None) -> FastAPI:
    from app.main import app

    return app


@pytest.fixture()
async def client(app: FastAPI) -> AsyncClient:
    logger.debug('client fixture')
    async with LifespanManager(app):
        logger.debug('with lifespan manager')
        async with AsyncClient(
            app=app,
            base_url='http://testserver',
            headers={"Content-Type": "application/json"}
        ) as client:
            logger.debug('with async client')

            yield client


@pytest.fixture()
async def auth_client(app: FastAPI, client: AsyncClient) -> AsyncClient:

    new_user = {
        "email": "lebron@james.io",
        "name": "Testuser",
        "password": "heatcavslakers",
    }

    res = await client.post('users/register', json={"user": new_user})
    assert res.status_code == 201

    res = await client.post('users/login', json={"login": new_user})
    assert res.status_code == 200
    assert "access_token" in res.json()
    assert res.json()["access_token"] is not None

    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {res.json()['access_token']['token']}",
    }
    return client
