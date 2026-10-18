from __future__ import annotations

import os

import pytest

from distrans_client import AsyncDistransClient, DistransClient

BASE_URL = os.environ.get("DISTRANS_BASE_URL")
USERNAME = os.environ.get("DISTRANS_USERNAME")
PASSWORD = os.environ.get("DISTRANS_PASSWORD")

pytestmark = pytest.mark.integration

skip_without_credentials = pytest.mark.skipif(
    not (BASE_URL and USERNAME and PASSWORD),
    reason="credentials are not set",
)


@skip_without_credentials
def test_gateway_receives_hello() -> None:
    with DistransClient(BASE_URL) as client:
        client.login(USERNAME, PASSWORD)
        with client.gateway(proxy=None) as gateway:
            assert gateway.heartbeat_interval_ms is not None
            assert gateway.heartbeat_interval_ms > 0


@skip_without_credentials
async def test_async_gateway_receives_hello() -> None:
    async with AsyncDistransClient(BASE_URL) as client:
        await client.login(USERNAME, PASSWORD)
        async with client.gateway(proxy=None) as gateway:
            assert gateway.heartbeat_interval_ms is not None
            assert gateway.heartbeat_interval_ms > 0
