import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint_response(test_client: AsyncClient):
    r = await test_client.get("/api/health/ping")
    assert r.status_code == 200
    assert r.json().get("response") == "pong"
