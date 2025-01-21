import random

import pytest
from fastapi.testclient import TestClient
from pydantic import HttpUrl

base_route = "/api/shorten/"
valid_payload = {"url": "http://somelongtest.url"}


# CREATE
@pytest.mark.asyncio
async def test_create_short_url_with_missing_payload(test_client: TestClient):
    r = await test_client.post(base_route, json={})
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_create_short_url_with_invalid_json_key(test_client: TestClient):
    r = await test_client.post(base_route, json={"invalid": "http://somelongtest.url"})
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_create_short_url_with_invalid_json_data(test_client: TestClient):
    r = await test_client.post(base_route, json={"url": "somelongtest.url"})
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_create_short_url_with_valid_payload(test_client: TestClient):
    r = await test_client.post(base_route, json=valid_payload)
    data = r.json()
    assert r.status_code == 201
    assert data.get("id")
    assert data.get("url")
    assert data.get("shortCode")
    assert data.get("createdAt")
    assert data.get("updatedAt")
    assert data.get("accesCount") is None


# READ
@pytest.mark.asyncio
async def test_get_all_short_urls(test_client: TestClient):
    # Check document count before insertion
    r = await test_client.get(base_route)
    assert r.status_code == 200
    assert len(r.json()) == 0

    # Populate database with random number of documents (from 1-10)
    count = random.randint(1, 10)
    for i in range(count):
        await test_client.post(base_route, json=valid_payload)

    # Check count of generated entries
    r = await test_client.get(base_route)
    assert r.status_code == 200
    assert len(r.json()) == count


@pytest.mark.asyncio
async def test_get_short_url_by_short_code(test_client: TestClient):
    # Populate database with one document
    r = await test_client.post(base_route, json=valid_payload)
    post_json = r.json()
    short_code = post_json.get("shortCode")
    document_route = base_route + short_code

    # Get document by short code
    r = await test_client.get(document_route)
    get_json = r.json()
    assert r.status_code == 200
    assert post_json == get_json


@pytest.mark.asyncio
async def test_get_none_existent_short_url(test_client: TestClient):
    r = await test_client.get(base_route + "01234567")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_get_short_url_by_short_code_with_stats(test_client: TestClient):
    # Populate database with one document
    r = await test_client.post(base_route, json=valid_payload)
    post_json = r.json()
    short_code = post_json.get("shortCode")
    document_route = base_route + short_code

    # Get document by short code and check access count
    r = await test_client.get(document_route + "/stats")
    get_json = r.json()
    assert r.status_code == 200
    assert get_json.pop("accessCount") == 0
    assert post_json == get_json


# UPDATE
async def test_update_short_url_by_short_code(test_client: TestClient):
    # Populate database with one document
    r = await test_client.post(base_route, json=valid_payload)
    post_json = r.json()
    short_code = post_json.get("shortCode")
    document_route = base_route + short_code
    assert post_json.get("url") == HttpUrl(valid_payload["url"]).unicode_string()

    # Update document and check content
    r = await test_client.put(
        document_route,
        json={"url": "http://somelongupdatedtest.url"},
    )
    put_json = r.json()
    assert r.status_code == 200
    assert put_json.get("url") != HttpUrl(valid_payload["url"]).unicode_string()
    assert (
        put_json.get("url")
        == HttpUrl("http://somelongupdatedtest.url").unicode_string()
    )
    assert put_json.get("createdAt") == post_json.get("createdAt")
    assert put_json.get("updatedAt") != post_json.get("updatedAt")


# DELETE
async def test_delete_short_url_by_short_code(test_client: TestClient):
    # Populate database with one document
    r = await test_client.post(base_route, json=valid_payload)
    short_code = r.json().get("shortCode")
    document_route = base_route + short_code

    # Check documents count before deletion
    r = await test_client.get(base_route)
    assert len(r.json()) == 1

    # Delete document by short code
    r = await test_client.delete(document_route)
    assert r.status_code == 204

    # Check documents count
    r = await test_client.get(base_route)
    assert len(r.json()) == 0


# ACCESS COUNT INCREASE ENDPOINT
async def test_url_access_count_increase_endpoint(test_client: TestClient):
    # Populate database
    r = await test_client.post(base_route, json=valid_payload)
    short_code = r.json().get("shortCode")
    document_route = base_route + short_code

    # Check access count before increase
    r = await test_client.get(document_route + "/stats")
    assert r.json().get("accessCount") == 0

    # Increase access count
    r = await test_client.put(document_route + "/increase")
    assert r.status_code == 204

    # Check access count after increase
    r = await test_client.get(document_route + "/stats")
    assert r.json().get("accessCount") == 1
