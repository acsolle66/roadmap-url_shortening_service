import random
from typing import Literal

import faker
import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from pydantic import HttpUrl

base_url = "/api/shorten/"

faker = Faker()
valid_payload = {"url": faker.uri()}


# CREATE
@pytest.mark.parametrize(
    "invalid_payload, expected_status_code",
    [
        ({}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        ({"invalid": faker.uri()}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        ({"url": faker.uri_path()}, status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
@pytest.mark.asyncio
async def test_create_short_url_with_invalid_inputs(
    auth_test_client: AsyncClient,
    invalid_payload: dict[str, str],
    expected_status_code: Literal[422],
):
    r = await auth_test_client.post(base_url, json=invalid_payload)
    assert r.status_code == expected_status_code


@pytest.mark.asyncio
async def test_create_short_url_with_valid_payload(auth_test_client: AsyncClient):
    r = await auth_test_client.post(base_url, json=valid_payload)
    data = r.json()
    assert r.status_code == status.HTTP_201_CREATED
    assert data.get("id")
    assert data.get("url")
    assert data.get("shortCode")
    assert data.get("createdAt")
    assert data.get("updatedAt")
    assert data.get("accesCount") is None


# READ
@pytest.mark.asyncio
async def test_get_all_short_urls(auth_test_client: AsyncClient):
    # Check document count before insertion
    r = await auth_test_client.get(base_url)
    assert r.status_code == 200
    assert len(r.json()) == 0

    # Populate database with random number of documents (from 1-10)
    count = random.randint(1, 10)
    for _ in range(count):
        await auth_test_client.post(base_url, json=valid_payload)

    # Check count of generated entries
    r = await auth_test_client.get(base_url)
    assert r.status_code == status.HTTP_200_OK
    assert len(r.json()) == count


@pytest.mark.asyncio
async def test_get_short_url_by_short_code(
    test_client: AsyncClient,
    auth_test_client: AsyncClient,
):
    # Populate database with one document
    r = await auth_test_client.post(base_url, json=valid_payload)
    post_json = r.json()
    short_code = post_json.get("shortCode")
    document_route = base_url + short_code

    # Get document by short code
    r = await test_client.get(document_route)
    get_json = r.json()
    assert r.status_code == status.HTTP_200_OK
    assert post_json == get_json


@pytest.mark.asyncio
async def test_get_none_existent_short_url_by_short_code(test_client: AsyncClient):
    r = await test_client.get(base_url + "01234567")
    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert r.json().get("detail") == "URL not found"


@pytest.mark.asyncio
async def test_get_short_url_with_stats_by_short_code(auth_test_client: AsyncClient):
    # Populate database with one document
    r = await auth_test_client.post(base_url, json=valid_payload)
    post_json = r.json()
    short_code = post_json.get("shortCode")
    document_route = base_url + short_code

    # Get document by short code and check access count
    r = await auth_test_client.get(document_route + "/stats")
    get_json = r.json()
    assert r.status_code == status.HTTP_200_OK
    assert get_json.pop("accessCount") == 0
    assert post_json == get_json


# UPDATE
@pytest.mark.asyncio
async def test_update_short_url_by_short_code(auth_test_client: AsyncClient):
    # Populate database with one document
    r = await auth_test_client.post(base_url, json=valid_payload)
    post_json = r.json()
    short_code = post_json.get("shortCode")
    document_route = base_url + short_code
    assert post_json.get("url") == HttpUrl(valid_payload["url"]).unicode_string()

    # Update document and check content
    r = await auth_test_client.put(
        document_route,
        json={"url": valid_payload["url"] + "/test"},
    )
    put_json = r.json()
    assert r.status_code == status.HTTP_200_OK
    assert put_json.get("url") != HttpUrl(valid_payload["url"]).unicode_string()
    assert (
        put_json.get("url") == HttpUrl(valid_payload["url"] + "/test").unicode_string()
    )
    assert put_json.get("createdAt") == post_json.get("createdAt")
    assert put_json.get("updatedAt") != post_json.get("updatedAt")


# DELETE
@pytest.mark.asyncio
async def test_delete_short_url_by_short_code(auth_test_client: AsyncClient):
    # Populate database with one document
    r = await auth_test_client.post(base_url, json=valid_payload)
    short_code = r.json().get("shortCode")
    document_route = base_url + short_code

    # Check documents count before deletion
    r = await auth_test_client.get(base_url)
    assert len(r.json()) == 1

    # Delete document by short code
    r = await auth_test_client.delete(document_route)
    assert r.status_code == status.HTTP_200_OK
    assert r.json().get("detail") == "Deleted"

    # Check documents count
    r = await auth_test_client.get(base_url)
    assert len(r.json()) == 0


# ACCESS COUNT INCREASE ENDPOINT
@pytest.mark.asyncio
async def test_increment_access_count_by_short_code(auth_test_client: AsyncClient):
    # Populate database
    r = await auth_test_client.post(base_url, json=valid_payload)
    short_code = r.json().get("shortCode")
    document_route = base_url + short_code

    # Check access count before increase
    r = await auth_test_client.get(document_route + "/stats")
    assert r.json().get("accessCount") == 0

    # Call the endpoint with random number of hits (from 1-10)
    count = random.randint(1, 10)
    for i in range(count):
        r = await auth_test_client.put(document_route + "/increase")
        assert r.status_code == status.HTTP_200_OK
        assert r.json().get("detail") == i + 1

    # Check access count after increase
    r = await auth_test_client.get(document_route + "/stats")
    assert r.json().get("accessCount") == count
