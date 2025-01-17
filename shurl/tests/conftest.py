import os

import pytest
from fastapi.testclient import TestClient

from ..main import app


@pytest.fixture(scope="session", autouse=False)
def test_client():
    os.environ["ENV"] = "TEST"
    with TestClient(app) as client:
        yield client
        app.client.drop_database(app.db_config.MONGO_DB)
