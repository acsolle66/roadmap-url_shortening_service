from fastapi.testclient import TestClient


def test_shorten_get_all_url_maps(test_client: TestClient):
    response = test_client.post("/api/shorten/", json={"url": "test_url"})
    assert response
