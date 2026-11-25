from __future__ import annotations

import pytest
import allure

from api.client import PoetryApiClient


@pytest.fixture(scope="session")
def client() -> PoetryApiClient:
    return PoetryApiClient()


def pytest_runtest_setup(item):
    """将 pytest 标记映射为 Allure 标签，避免在每条用例中重复装饰器。"""
    for marker in item.iter_markers():
        if marker.name in {"smoke", "contract", "negative", "semantic"}:
            allure.dynamic.tag(marker.name)


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
