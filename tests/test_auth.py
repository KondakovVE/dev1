from fastapi.applications import FastAPI
from fastapi import status
from httpx import AsyncClient

import pytest

pytestmark = pytest.mark.asyncio


class TestUserWorkFlow:
    async def test_register_new_user(self, app: FastAPI, client: AsyncClient):
        user = {
            "email": "test1@mail.io",
            "name": "Test User 1",
            "password": "test1@mail.io"
        }
        res = await client.post('users/register', json={"user": user})
        assert res.status_code == 201

    async def test_registration_failed_with_exist_email(self, app: FastAPI, client: AsyncClient):
        new_user = {
            "email": "test2@mail.io",
            "name": "Test User 2",
            "password": "test1@mail.io"
        }
        res = await client.post('users/register', json={"user": new_user})

        assert res.status_code == 201

        res = await client.post('users/register', json={"user": new_user})
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    async def test_user_cant_login_with_wrong_password(self, app: FastAPI, client: AsyncClient):
        new_user = {
            "email": "test5@mail.io",
            "name": "Test User 5",
            "password": "test5@mail.io"
        }
        res = await client.post('users/register', json={"user": new_user})
        assert res.status_code == 201

        login = {
            "email": "test5@mail.io",
            "password": "wrong_password"
        }
        res = await client.post('users/login', json={"login": login})
        assert res.status_code == 401

    async def test_user_can_login(self, app: FastAPI, client: AsyncClient):
        new_user = {
            "email": "test4@mail.io",
            "name": "Test User 4",
            "password": "test4@mail.io"
        }
        res = await client.post('users/register', json={"user": new_user})
        assert res.status_code == 201

        login = {
            "email": "test4@mail.io",
            "password": "test4@mail.io"
        }
        res = await client.post('users/login', json={"login": login})
        assert res.status_code == 200
        assert "access_token" in res.json()
        assert res.json()["access_token"] is not None

    async def test_authorizated_user_have_access_to_profile(self, app: FastAPI, auth_client: AsyncClient):
        res = await auth_client.get('users/me')

        assert res.status_code == 200
        res_user = res.json()
