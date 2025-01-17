import os

import pytest
from fastapi.testclient import TestClient

from ..main import app


@pytest.fixture(scope="session", autouse=False)
def test_client():
    os.environ["ENV"] = "TEST"
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function", autouse=True)
def drop_db(test_client: TestClient):
    yield
    test_client.app.db_client.drop_database(app.db_config.MONGO_DB)
