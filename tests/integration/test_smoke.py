from __future__ import annotations

import os

import pytest

from distrans_client import DistransClient
from distrans_client.api.meta import get_limits

BASE_URL = os.environ.get("DISTRANS_BASE_URL")
USERNAME = os.environ.get("DISTRANS_USERNAME")
PASSWORD = os.environ.get("DISTRANS_PASSWORD")

pytestmark = pytest.mark.integration


@pytest.mark.skipif(not BASE_URL, reason="DISTRANS_BASE_URL is not set")
def test_limits() -> None:
    with DistransClient(BASE_URL) as client:
        limits = get_limits.sync(client=client.raw)

    assert limits is not None
    assert limits.messages.max_codepoints_per_message > 0
    assert limits.files.max_size > 0


@pytest.mark.skipif(not (BASE_URL and USERNAME and PASSWORD), reason="credentials are not set")
def test_login_and_me() -> None:
    from distrans_client.api.users import get_me

    with DistransClient(BASE_URL) as client:
        client.login(USERNAME, PASSWORD)
        me = get_me.sync(client=client.raw)

    assert me is not None
    assert me.username == USERNAME
