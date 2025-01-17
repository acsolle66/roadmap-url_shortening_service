import pytest
from fastapi.testclient import TestClient

from ..main import app

test_client = TestClient(app)


@pytest.mark.skip()
def test_health_endpoint_response():
    response = test_client.get("/api/health/ping")
    assert response.status_code == 200
    assert response.json().get("response") == "pong"
