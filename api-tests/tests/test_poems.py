from __future__ import annotations

import pytest

from conftest import assert_data, assert_error


def assert_poem(poem):
    assert {"title", "content", "author", "dynasty", "type"} <= set(poem)
    assert isinstance(poem["content"], list)


@pytest.mark.smoke
@pytest.mark.contract
def test_list_poems_default(client):
    data = assert_data(client.get("/api/v1/poems?page=1&page_size=2"))
    assert len(data) == 2
    for poem in data:
        assert_poem(poem)


@pytest.mark.contract
def test_list_poems_traditional_chinese(client):
    data = assert_data(client.get("/api/v1/poems?lang=zh-Hant&page_size=1"))
    assert len(data) == 1
    assert_poem(data[0])


@pytest.mark.contract
@pytest.mark.parametrize(
    "query",
    [
        "dynasty=唐&page_size=1",
        "author=李白&page_size=1",
        "dynasty_id=6&type_id=11&type_id=12&page_size=1",
    ],
)
def test_list_poems_filters(client, query):
    data = assert_data(client.get(f"/api/v1/poems?{query}"))
    assert data


@pytest.mark.contract
def test_list_poems_cursor_pagination(client):
    first = client.get("/api/v1/poems?page_size=1")
    data = assert_data(first)
    assert data
    cursor = first.json()["pagination"].get("next_cursor")
    assert cursor
    second = client.get(f"/api/v1/poems?page_size=1&after={cursor}")
    assert_data(second)


@pytest.mark.contract
def test_list_poems_page_size_upper_boundary(client):
    response = client.get("/api/v1/poems?page_size=100")
    assert response.status_code == 200
    assert len(response.json()["data"]) <= 100


@pytest.mark.negative
def test_list_poems_rejects_unknown_parameter(client):
    payload = assert_error(client.get("/api/v1/poems?dynastyName=唐"), 400)
    assert "dynastyName" in payload["message"]


@pytest.mark.negative
def test_list_poems_rejects_invalid_page_size(client):
    assert_error(client.get("/api/v1/poems?page_size=0"), 400)


@pytest.mark.smoke
@pytest.mark.contract
def test_search_poems_by_keyword(client):
    data = assert_data(client.get("/api/v1/poems/search?q=静夜思"))
    assert any(item["title"] == "静夜思" for item in data)


@pytest.mark.contract
def test_search_poems_by_dynasty_and_title(client):
    data = assert_data(client.get("/api/v1/poems/search?q=月&dynasty=唐&type=title&page_size=5"))
    assert data
    assert all("月" in item["title"] for item in data)


@pytest.mark.negative
def test_search_poems_requires_query(client):
    assert_error(client.get("/api/v1/poems/search"), 400)


@pytest.mark.negative
def test_search_poems_rejects_unsupported_type(client):
    assert_error(client.get("/api/v1/poems/search?q=月&type=unknown"), 400)


@pytest.mark.semantic
def test_semantic_search(client):
    response = client.get("/api/v1/poems/semantic?q=下雪天一个老人独自在小船上钓鱼&limit=1")
    if response.status_code == 503:
        pytest.skip("服务端未启用语义检索")
    data = assert_data(response)
    assert len(data) <= 1


@pytest.mark.smoke
@pytest.mark.contract
@pytest.mark.parametrize(
    "query",
    [
        "",
        "author=李白",
        "type=五言绝句",
        "type=唐诗&dynasty=唐",
        "char=春",
        "author=李白&type=五言绝句",
        "author=李白&type=五言绝句&dynasty=唐",
        "author=李白&dynasty=唐&type=五言绝句&type=七言绝句&type=五言律诗",
    ],
)
def test_random_poem_variants(client, query):
    data = assert_data(client.get(f"/api/v1/poems/random?{query}"))
    assert_poem(data)


@pytest.mark.negative
def test_random_poem_char_cannot_combine_filters(client):
    assert_error(client.get("/api/v1/poems/random?char=春&author=李白"), 400)


@pytest.mark.negative
def test_random_poem_char_requires_single_character(client):
    assert_error(client.get("/api/v1/poems/random?char=春天"), 400)
