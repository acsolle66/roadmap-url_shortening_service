import os

import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

from ..main import app


# https://github.com/florimondmanca/asgi-lifespan
@pytest_asyncio.fixture(scope="session", autouse=False)
async def test_app():
    os.environ["ENV"] = "TEST"
    async with LifespanManager(app) as manager:
        yield manager.app


@pytest_asyncio.fixture(scope="session", autouse=False)
async def test_client(test_app):
    async with AsyncClient(
        transport=ASGITransport(test_app),
        base_url="http://test",
        follow_redirects=True,
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="function", autouse=False)
async def auth_test_client(test_client: AsyncClient):
    test_user = {"username": "test_user", "password": "password123"}
    await test_client.post("api/auth/users", json=test_user)
    r = await test_client.post("api/auth/token", data=test_user)
    token = r.json().get("access_token")
    headers = {"Authorization": "Bearer " + token}
    test_client.headers = headers
    yield test_client


@pytest_asyncio.fixture(scope="function", autouse=True)
async def drop_test_db(test_client: AsyncClient):
    yield
    await app.db_client.drop_database(app.db_config.MONGO_DB)
