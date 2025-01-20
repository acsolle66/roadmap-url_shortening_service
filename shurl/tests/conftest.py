import os
from ..main import app as fastapi_app
from httpx import AsyncClient, ASGITransport
import pytest_asyncio
from asgi_lifespan import LifespanManager


@pytest_asyncio.fixture(scope="session", autouse=False)
async def app():
    os.environ["ENV"] = "TEST"
    async with LifespanManager(fastapi_app) as manager:
        yield manager.app


@pytest_asyncio.fixture(scope="session", autouse=False)
async def test_client(app):
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://test"
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="function", autouse=True)
async def drop_db():
    yield
    await fastapi_app.db_client.drop_database(fastapi_app.db_config.MONGO_DB)
