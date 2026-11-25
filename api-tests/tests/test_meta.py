from __future__ import annotations

import pytest

from conftest import assert_data, assert_error


@pytest.mark.smoke
def test_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.smoke
@pytest.mark.contract
def test_stats_contract(client):
    data = assert_data(client.get("/api/v1/stats"))
    assert {"total_poems", "total_authors", "total_dynasties", "poems_by_dynasty", "poems_by_type"} <= set(data)
    assert data["total_poems"] > 0


@pytest.mark.contract
def test_openapi_document(client):
    response = client.get("/api/v1/openapi.yaml")
    assert response.status_code == 200
    text = response.content.decode("utf-8")
    assert "openapi: 3.2.0" in text
    assert "/poems/search:" in text
    assert "/authors/{id}:" in text


@pytest.mark.negative
def test_stats_rejects_unknown_query_parameter(client):
    payload = assert_error(client.get("/api/v1/stats?lang=zh-Hans"), 400)
    assert "lang" in payload["message"]
