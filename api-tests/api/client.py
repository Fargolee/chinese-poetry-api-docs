from __future__ import annotations

import time
from typing import Any

import requests
import allure

from config.settings import BASE_URL, TIMEOUT


class PoetryApiClient:
    """REST API 请求层，统一处理基础地址、超时和 JSON 响应。"""

    def __init__(self, base_url: str = BASE_URL, timeout: float = TIMEOUT) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.rate_limit_retries = 3

    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        kwargs.setdefault("timeout", self.timeout)
        url = f"{self.base_url}{path}"
        for attempt in range(self.rate_limit_retries + 1):
            response = self.session.request(method, url, **kwargs)
            allure.attach(
                f"{method} {url}\nparams={kwargs.get('params')}\njson={kwargs.get('json')}",
                name="request",
                attachment_type=allure.attachment_type.TEXT,
            )
            body = response.content
            if "json" in response.headers.get("content-type", "").lower():
                allure.attach(
                    body.decode("utf-8", errors="replace"),
                    name=f"response-{response.status_code}",
                    attachment_type=allure.attachment_type.JSON,
                )
            else:
                allure.attach(
                    body,
                    name=f"response-{response.status_code}",
                    attachment_type=allure.attachment_type.TEXT,
                )
            if response.status_code != 429 or attempt == self.rate_limit_retries:
                return response
            retry_after = response.headers.get("Retry-After")
            try:
                delay = max(float(retry_after), 1.0) if retry_after else 1.1
            except ValueError:
                delay = 1.1
            time.sleep(delay)
        raise AssertionError("unreachable")

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", path, **kwargs)
