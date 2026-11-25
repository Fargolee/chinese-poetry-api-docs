from __future__ import annotations

import pytest

from conftest import assert_data, assert_error


@pytest.mark.contract
def test_authors_list(client):
    data = assert_data(client.get("/api/v1/authors?page=1&page_size=20"))
    assert data
    assert {"id", "name", "poem_count"} <= set(data[0])


@pytest.mark.contract
def test_author_detail(client):
    data = assert_data(client.get("/api/v1/authors/1"))
    assert {"id", "name"} <= set(data)


@pytest.mark.negative
def test_author_not_found(client):
    assert_error(client.get("/api/v1/authors/999999999"), 404)


@pytest.mark.contract
def test_dynasties_list(client):
    data = assert_data(client.get("/api/v1/dynasties"))
    assert data
    assert {"id", "name", "poem_count", "author_count"} <= set(data[0])


@pytest.mark.contract
def test_dynasty_detail(client):
    data = assert_data(client.get("/api/v1/dynasties/1"))
    assert {"id", "name"} <= set(data)


@pytest.mark.contract
def test_types_list(client):
    data = assert_data(client.get("/api/v1/types"))
    assert data
    assert {"id", "name", "category", "poem_count"} <= set(data[0])


@pytest.mark.contract
def test_type_detail(client):
    data = assert_data(client.get("/api/v1/types/10"))
    assert {"id", "name", "category"} <= set(data)


@pytest.mark.negative
@pytest.mark.parametrize("path", ["/api/v1/dynasties/999999999", "/api/v1/types/999999999"])
def test_resource_not_found(path, client):
    assert_error(client.get(path), 404)
