import pytest
from fastapi.testclient import TestClient

from ..main import app

from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint_response(test_client: AsyncClient):
    response = await test_client.get("/api/health/ping")
    assert response.status_code == 200
    assert response.json().get("response") == "pong"
