from enum import Enum

import pytest
from httpx import ASGITransport, AsyncClient

from app.main.web_api import create_app


class StatusCode(Enum):
    OK = 200
    NOT_FOUND = 404
    REDIRECT = 307
    UNSUPPORTED_ENTITY = 422
    CONFLICT = 409
    UNAUTHORIZED = 401


@pytest.fixture(scope="session")
def status_code():
    return StatusCode


app = create_app()


@pytest.fixture()
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def auth_client():
    transport = ASGITransport(app=app)
    data = {"username": "testuser29123ss", "password": "test2187672"}

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("/auth/signup", data=data)
        res = await ac.post("/auth/login", data=data)
        token = res.cookies.get("access_token")
        ac.cookies.set("access_token", token)
        yield ac
