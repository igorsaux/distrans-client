"""Optional retries for ``httpx`` transports.

The generated operations call ``httpx.Client.request`` directly, so retries are
implemented as a transport wrapper instead of changing every operation.
"""

from __future__ import annotations

import asyncio
import random
import time
from dataclasses import dataclass

import httpx

DEFAULT_RETRY_STATUSES = (429, 502, 503, 504)
DEFAULT_RETRY_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    """Retry rules for :class:`RetryTransport` and :class:`AsyncRetryTransport`.

    ``attempts`` is the number of extra attempts after the first request.
    Only methods in ``methods`` are retried; by default these are idempotent
    methods, so enabling retries cannot duplicate a ``POST``.
    """

    attempts: int = 2
    backoff: float = 0.5
    max_backoff: float = 10.0
    statuses: tuple[int, ...] = DEFAULT_RETRY_STATUSES
    methods: frozenset[str] = DEFAULT_RETRY_METHODS

    def __post_init__(self) -> None:
        if self.attempts < 0:
            raise ValueError("attempts must be >= 0")
        if self.backoff < 0:
            raise ValueError("backoff must be >= 0")
        if self.max_backoff < 0:
            raise ValueError("max_backoff must be >= 0")

        statuses = tuple(self.statuses)
        for status in statuses:
            if not 100 <= status <= 599:
                raise ValueError("statuses must contain HTTP status codes in 100..599")

        methods = frozenset(str(method).upper() for method in self.methods)
        object.__setattr__(self, "statuses", statuses)
        object.__setattr__(self, "methods", methods)


def _retry_after(response: httpx.Response, policy: RetryPolicy) -> float | None:
    value = response.headers.get("Retry-After")
    if value is None:
        return None
    value = value.strip()
    if not value.isdigit():
        return None
    return min(float(int(value)), policy.max_backoff)


def _retry_delay(policy: RetryPolicy, attempt: int, response: httpx.Response | None) -> float:
    if response is not None:
        retry_after = _retry_after(response, policy)
        if retry_after is not None:
            return retry_after

    if policy.backoff <= 0:
        return 0.0

    delay = min(policy.backoff * (2 ** min(attempt, 60)), policy.max_backoff)
    return random.uniform(delay * 0.5, delay)


class RetryTransport(httpx.BaseTransport):
    """A synchronous transport that retries selected methods and statuses."""

    def __init__(self, transport: httpx.BaseTransport, policy: RetryPolicy) -> None:
        self._transport = transport
        self._policy = policy

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        if request.method.upper() not in self._policy.methods:
            return self._transport.handle_request(request)

        # Read the body once so it can be replayed if a retry is needed.
        request.read()

        for attempt in range(self._policy.attempts + 1):
            try:
                response = self._transport.handle_request(request)
            except httpx.TransportError:
                if attempt >= self._policy.attempts:
                    raise
                self._sleep(_retry_delay(self._policy, attempt, None))
                continue

            if response.status_code not in self._policy.statuses or attempt >= self._policy.attempts:
                return response

            delay = _retry_delay(self._policy, attempt, response)
            response.close()
            self._sleep(delay)

        raise AssertionError("unreachable")

    @staticmethod
    def _sleep(delay: float) -> None:
        if delay > 0:
            time.sleep(delay)

    def close(self) -> None:
        self._transport.close()


class AsyncRetryTransport(httpx.AsyncBaseTransport):
    """An asynchronous transport that retries selected methods and statuses."""

    def __init__(self, transport: httpx.AsyncBaseTransport, policy: RetryPolicy) -> None:
        self._transport = transport
        self._policy = policy

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        if request.method.upper() not in self._policy.methods:
            return await self._transport.handle_async_request(request)

        # Read the body once so it can be replayed if a retry is needed.
        await request.aread()

        for attempt in range(self._policy.attempts + 1):
            try:
                response = await self._transport.handle_async_request(request)
            except httpx.TransportError:
                if attempt >= self._policy.attempts:
                    raise
                await self._sleep(_retry_delay(self._policy, attempt, None))
                continue

            if response.status_code not in self._policy.statuses or attempt >= self._policy.attempts:
                return response

            delay = _retry_delay(self._policy, attempt, response)
            await response.aclose()
            await self._sleep(delay)

        raise AssertionError("unreachable")

    @staticmethod
    async def _sleep(delay: float) -> None:
        if delay > 0:
            await asyncio.sleep(delay)

    async def aclose(self) -> None:
        await self._transport.aclose()
