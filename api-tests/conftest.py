from __future__ import annotations

import pytest

from api.client import PoetryApiClient


@pytest.fixture(scope="session")
def client() -> PoetryApiClient:
    return PoetryApiClient()


def assert_error(response, status_code: int) -> dict:
    assert response.status_code == status_code, response.text[:500]
    payload = response.json()
    assert set(("error", "message")).issubset(payload), payload
    return payload


def assert_data(response, status_code: int = 200):
    assert response.status_code == status_code, response.text[:500]
    payload = response.json()
    assert "data" in payload, payload
    return payload["data"]
