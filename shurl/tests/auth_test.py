import faker
import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient

base_url = "/api/auth"

faker = Faker()


@pytest.mark.asyncio
async def test_create_user(test_client: AsyncClient):
    r = await test_client.post(
        base_url + "/users",
        json={"username": faker.user_name(), "password": faker.password(8)},
    )
    data = r.json()
    assert r.status_code == status.HTTP_201_CREATED
    assert r.status_code == status.HTTP_201_CREATED
    assert data.get("id")
    assert data.get("username")
    assert data.get("hashed_password") is None


@pytest.mark.asyncio
async def test_get_access_token(test_client: AsyncClient):
    user = {"username": faker.user_name(), "password": faker.password(8)}
    await test_client.post(base_url + "/users", json=user)
    r = await test_client.post(base_url + "/token", data=user)
    data = r.json()
    assert r.status_code == status.HTTP_200_OK
    assert data.get("access_token")
    assert data.get("token_type")


@pytest.mark.asyncio
async def test_get_me(test_client: AsyncClient):
    # Create user
    user = {"username": faker.user_name(), "password": faker.password(8)}
    await test_client.post(base_url + "/users", json=user)

    # Get access token
    r = await test_client.post(base_url + "/token", data=user)
    access_token = r.json().get("access_token")
    headers = {"Authorization": "Bearer " + access_token}

    # Get me
    r = await test_client.get(base_url + "/users/me", headers=headers)
    assert r.status_code == status.HTTP_200_OK
    assert r.json().get("username") == user["username"]
    assert r.json().get("id")
