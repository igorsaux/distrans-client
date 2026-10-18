from __future__ import annotations

from collections.abc import Callable

import httpx
import pytest

from distrans_client import RetryPolicy
from distrans_client.retry import AsyncRetryTransport, RetryTransport


def _client(
    handler: Callable[[httpx.Request], httpx.Response],
    policy: RetryPolicy,
) -> httpx.Client:
    return httpx.Client(transport=RetryTransport(httpx.MockTransport(handler), policy))


def _async_client(
    handler: Callable[[httpx.Request], httpx.Response],
    policy: RetryPolicy,
) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=AsyncRetryTransport(httpx.MockTransport(handler), policy))


def test_retry_policy_normalizes_methods_and_validates() -> None:
    policy = RetryPolicy(methods=frozenset({"get", "Post"}))
    assert policy.methods == frozenset({"GET", "POST"})

    with pytest.raises(ValueError):
        RetryPolicy(attempts=-1)
    with pytest.raises(ValueError):
        RetryPolicy(backoff=-1)
    with pytest.raises(ValueError):
        RetryPolicy(max_backoff=-1)
    with pytest.raises(ValueError):
        RetryPolicy(statuses=(99,))
    with pytest.raises(ValueError):
        RetryPolicy(statuses=(600,))


def test_retry_after_zero_retries_get() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(429, headers={"Retry-After": "0"})
        return httpx.Response(200)

    with _client(handler, RetryPolicy(attempts=1, backoff=0)) as client:
        response = client.get("https://example.test/")

    assert response.status_code == 200
    assert calls == 2


def test_retry_exhausts_attempts_and_returns_last_response() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(503, text="still down")

    with _client(handler, RetryPolicy(attempts=1, backoff=0)) as client:
        response = client.get("https://example.test/")

    assert response.status_code == 503
    assert calls == 2


def test_post_is_not_retried_by_default() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(503)

    with _client(handler, RetryPolicy(attempts=2, backoff=0)) as client:
        response = client.post("https://example.test/", content=b"x")

    assert response.status_code == 503
    assert calls == 1


def test_post_is_retried_when_enabled() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(503)

    policy = RetryPolicy(attempts=2, backoff=0, methods=frozenset({"POST"}))
    with _client(handler, policy) as client:
        response = client.post("https://example.test/", content=b"x")

    assert response.status_code == 503
    assert calls == 3


def test_transport_error_is_retried_and_then_raised() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        raise httpx.ConnectError("boom", request=request)

    with _client(handler, RetryPolicy(attempts=1, backoff=0)) as client:
        with pytest.raises(httpx.ConnectError):
            client.get("https://example.test/")

    assert calls == 2


async def test_async_retry_after_zero_retries_get() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(429, headers={"Retry-After": "0"})
        return httpx.Response(200)

    async with _async_client(handler, RetryPolicy(attempts=1, backoff=0)) as client:
        response = await client.get("https://example.test/")

    assert response.status_code == 200
    assert calls == 2


async def test_async_retry_exhausts_attempts_and_returns_last_response() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(503, text="still down")

    async with _async_client(handler, RetryPolicy(attempts=1, backoff=0)) as client:
        response = await client.get("https://example.test/")

    assert response.status_code == 503
    assert calls == 2


async def test_async_post_is_not_retried_by_default() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(503)

    async with _async_client(handler, RetryPolicy(attempts=2, backoff=0)) as client:
        response = await client.post("https://example.test/", content=b"x")

    assert response.status_code == 503
    assert calls == 1


async def test_async_post_is_retried_when_enabled() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(503)

    policy = RetryPolicy(attempts=2, backoff=0, methods=frozenset({"POST"}))
    async with _async_client(handler, policy) as client:
        response = await client.post("https://example.test/", content=b"x")

    assert response.status_code == 503
    assert calls == 3


async def test_async_transport_error_is_retried_and_then_raised() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        raise httpx.ConnectError("boom", request=request)

    async with _async_client(handler, RetryPolicy(attempts=1, backoff=0)) as client:
        with pytest.raises(httpx.ConnectError):
            await client.get("https://example.test/")

    assert calls == 2
