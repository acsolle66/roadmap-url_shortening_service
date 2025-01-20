from fastapi.testclient import TestClient
import pytest


# https://github.com/florimondmanca/asgi-lifespan
@pytest.mark.asyncio
async def test_post_url_map_with_valid_payload(test_client: TestClient):
    response = await test_client.post(
        "/api/shorten/", json={"url": "http://somelongtest.url"}
    )
    data: dict = response.json()
    assert response.status_code == 201
    assert data.get("id")
    assert data.get("url")
    assert data.get("shortCode")
    assert data.get("createdAt")
    assert data.get("updatedAt")


@pytest.mark.asyncio
async def test_shorten_get_all_url_maps(test_client: TestClient):
    response = await test_client.get("/api/shorten/")
    assert response
