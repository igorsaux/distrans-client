from __future__ import annotations

import json

import httpx
import pytest

from distrans_client import (
    DistransAPIError,
    DistransClient,
    DistransDownloadError,
    DistransError,
    RetryPolicy,
    no_mentions,
)
from distrans_client.api.users import get_me
from distrans_client.models.attachment import Attachment


def make_client(handler: httpx.MockTransport) -> DistransClient:
    return DistransClient(
        "https://example.test/api",
        httpx_args={"transport": handler},
    )


def test_login_sets_token_and_keeps_refresh_cookie() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if request.url.path == "/api/auth/token":
            return httpx.Response(
                200,
                json={"access_token": "jwt-1", "expires_in": 3600},
                headers={
                    "set-cookie": "refresh_token=rt-1; Path=/api; HttpOnly; Secure; SameSite=Strict",
                },
            )
        if request.url.path == "/api/users/@me":
            return httpx.Response(
                200,
                json={
                    "id": "1",
                    "username": "alice",
                    "display_name": None,
                    "avatar_hash": None,
                    "is_bot": False,
                },
            )
        raise AssertionError(f"unexpected request: {request.method} {request.url}")

    with make_client(httpx.MockTransport(handler)) as client:
        token = client.login("alice", "secret")
        me = get_me.sync(client=client.raw)

    assert token.access_token == "jwt-1"
    assert token.expires_in == 3600
    assert me is not None
    assert me.username == "alice"

    login_request = seen[0]
    assert json.loads(login_request.content) == {
        "grant_type": "password",
        "username": "alice",
        "password": "secret",
    }
    assert seen[1].headers["authorization"] == "Bearer jwt-1"
    assert client.http.cookies["refresh_token"] == "rt-1"


def test_refresh_sends_cookie_and_rotates_token() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/auth/token/refresh"
        assert "refresh_token=rt-1" in request.headers["cookie"]
        return httpx.Response(
            200,
            json={"access_token": "jwt-2", "expires_in": 3600},
            headers={
                "set-cookie": "refresh_token=rt-2; Path=/api; HttpOnly; Secure; SameSite=Strict",
            },
        )

    with make_client(httpx.MockTransport(handler)) as client:
        client.http.cookies.set("refresh_token", "rt-1", domain="example.test", path="/api")
        token = client.refresh()

    assert token.access_token == "jwt-2"
    assert client.raw.token == "jwt-2"
    assert client.http.headers["authorization"] == "Bearer jwt-2"
    assert client.http.cookies["refresh_token"] == "rt-2"


def test_upload_file_sends_caller_content_type() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/files"
        assert request.url.params["name"] == "note.txt"
        assert request.headers["content-type"] == "text/plain"
        assert request.read() == b"hello"
        return httpx.Response(
            201,
            json={
                "id": "10",
                "name": "note.txt",
                "size": 5,
                "content_type": "text/plain",
                "hash": "a" * 64,
                "public_url": "https://files.example.test/files/" + "a" * 64,
            },
        )

    with make_client(httpx.MockTransport(handler)) as client:
        uploaded = client.upload_file("note.txt", b"hello", "text/plain")

    assert uploaded.id == "10"
    assert uploaded.hash_ == "a" * 64
    assert uploaded.public_url is not None


def test_upload_requires_content_type() -> None:
    with make_client(httpx.MockTransport(lambda request: httpx.Response(500))) as client:
        with pytest.raises(ValueError):
            client.upload_file("note.txt", b"hello", "")


def test_documented_error_raises_api_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/guilds/1/avatar"
        assert request.headers["content-type"] == "image/png"
        return httpx.Response(403, json={"message": "Missing permissions"})

    with make_client(httpx.MockTransport(handler)) as client:
        with pytest.raises(DistransAPIError) as raised:
            client.set_guild_avatar("1", b"png", "image/png")

    assert raised.value.status_code == 403
    assert raised.value.message == "Missing permissions"


def test_logout_clears_token() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/auth/token/logout"
        return httpx.Response(200)

    with make_client(httpx.MockTransport(handler)) as client:
        client.set_token("jwt-1")
        client.logout()

    assert client.raw.token == ""
    assert "authorization" not in client.http.headers


def test_gateway_uses_current_token() -> None:
    from distrans_client import Gateway

    with make_client(httpx.MockTransport(lambda request: httpx.Response(500))) as client:
        client.set_token("jwt-9")
        gateway = client.gateway(proxy=None)

        assert isinstance(gateway, Gateway)
        assert gateway.url == "wss://example.test/api/gateway"
        assert gateway._resolve_token() == "jwt-9"
        gateway.close()


def _message_payload(message_id: str, *, content: str = "hello", reply_to_id: str | None = None) -> dict:
    return {
        "id": message_id,
        "channel_id": "10",
        "author_id": "1",
        "webhook_id": None,
        "content": content,
        "created_at": 1,
        "reply_to_id": reply_to_id,
        "edited_at": None,
        "embeds": None,
        "attachments": [],
        "mention_everyone": False,
        "mentions": [],
        "mention_roles": [],
        "pinned": False,
        "reactions": None,
    }


def _emoji_payload(emoji_id: str) -> dict:
    return {"id": emoji_id, "name": f"emoji{emoji_id}", "icon_hash": "0" * 16}


def test_download_uses_separate_client_without_token_or_cookies() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if request.url.host == "files.example.test":
            return httpx.Response(302, headers={"location": "https://cdn.example.test/files/obj"})
        assert request.url.host == "cdn.example.test"
        return httpx.Response(200, content=b"webp-bytes", headers={"content-type": "image/webp"})

    client = DistransClient(
        "https://example.test/api",
        token="bot_secret",
        httpx_args={"transport": httpx.MockTransport(lambda request: httpx.Response(500))},
        download_httpx_args={
            "transport": httpx.MockTransport(handler),
            "headers": {"Authorization": "Bearer leaked"},
            "cookies": {"session": "leaked"},
            "auth": ("user", "pass"),
        },
    )
    try:
        data = client.download("https://files.example.test/files/obj")
    finally:
        client.close()

    assert data == b"webp-bytes"
    assert len(seen) == 2
    for request in seen:
        assert "authorization" not in request.headers
        assert "cookie" not in request.headers
        assert "content-type" not in request.headers


def test_download_non_2xx_raises_download_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, text="missing object")

    client = DistransClient(
        "https://example.test/api",
        download_httpx_args={"transport": httpx.MockTransport(handler)},
    )
    try:
        with pytest.raises(DistransDownloadError) as raised:
            client.download("https://files.example.test/files/missing")
    finally:
        client.close()

    assert raised.value.url == "https://files.example.test/files/missing"
    assert raised.value.status_code == 404
    assert raised.value.message == "missing object"


def test_download_attachment_requires_public_url() -> None:
    attachment = Attachment(
        id="1",
        name="photo.png",
        size=3,
        content_type="image/png",
        hash_="a" * 64,
        public_url=None,
    )
    with make_client(httpx.MockTransport(lambda request: httpx.Response(500))) as client:
        with pytest.raises(DistransError):
            client.download_attachment(attachment)


def test_send_message_returns_message() -> None:
    seen: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(json.loads(request.content))
        return httpx.Response(201, json=_message_payload("100"))

    with make_client(httpx.MockTransport(handler)) as client:
        message = client.send_message("10", "hello")

    assert message.id == "100"
    assert seen == [{"content": "hello"}]


def test_send_message_retries_reply_once_without_reply_to_id() -> None:
    seen: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        seen.append(body)
        if "reply_to_id" in body:
            return httpx.Response(400, json={"message": "'reply_to_id' is invalid"})
        return httpx.Response(201, json=_message_payload("101", reply_to_id=None))

    with make_client(httpx.MockTransport(handler)) as client:
        message = client.send_message("10", "hello", reply_to_id="99")

    assert message.id == "101"
    assert len(seen) == 2
    assert seen[0]["reply_to_id"] == "99"
    assert "reply_to_id" not in seen[1]


@pytest.mark.parametrize(
    ("status", "payload"),
    [
        (400, {"message": "content is empty"}),
        (403, {"message": "Missing permissions"}),
    ],
)
def test_send_message_does_not_retry_other_errors(status: int, payload: dict) -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(status, json=payload)

    with make_client(httpx.MockTransport(handler)) as client:
        with pytest.raises(DistransAPIError) as raised:
            client.send_message("10", "hello", reply_to_id="99")

    assert calls == 1
    assert raised.value.status_code == status
    assert raised.value.message == payload["message"]


def test_send_message_forwards_allowed_mentions() -> None:
    seen: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(json.loads(request.content))
        return httpx.Response(201, json=_message_payload("103"))

    with make_client(httpx.MockTransport(handler)) as client:
        client.send_message("10", "hi", allowed_mentions=no_mentions())

    assert seen == [{"content": "hi", "allowed_mentions": {"parse": []}}]


def test_reply_forwards_reply_to_id() -> None:
    seen: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(json.loads(request.content))
        return httpx.Response(201, json=_message_payload("102", reply_to_id="99"))

    with make_client(httpx.MockTransport(handler)) as client:
        message = client.reply("10", "99", "hi")

    assert message.reply_to_id == "99"
    assert seen == [{"content": "hi", "reply_to_id": "99"}]


def test_iter_guild_emojis_pages_until_short_page() -> None:
    seen: list[str | None] = []

    def handler(request: httpx.Request) -> httpx.Response:
        after = request.url.params.get("after")
        seen.append(after)
        assert request.url.params["limit"] == "100"
        if after is None:
            return httpx.Response(200, json=[_emoji_payload(str(i)) for i in range(1, 101)])
        assert after == "100"
        return httpx.Response(200, json=[_emoji_payload(str(i)) for i in range(101, 162)])

    with make_client(httpx.MockTransport(handler)) as client:
        emojis = list(client.iter_guild_emojis("1"))

    assert len(emojis) == 161
    assert [emoji.id for emoji in emojis] == [str(i) for i in range(1, 162)]
    assert seen == [None, "100"]


@pytest.mark.parametrize("page_size", [0, -1, 101])
def test_pagination_page_size_validation(page_size: int) -> None:
    with make_client(httpx.MockTransport(lambda request: httpx.Response(500))) as client:
        with pytest.raises(ValueError):
            client.iter_guild_emojis("1", page_size=page_size)
        with pytest.raises(ValueError):
            client.iter_messages_after("1", "0", page_size=page_size)
        with pytest.raises(ValueError):
            client.iter_messages_before("1", page_size=page_size)


def test_iter_messages_after_pages_ascending() -> None:
    seen: list[str | None] = []

    def handler(request: httpx.Request) -> httpx.Response:
        after = request.url.params.get("after")
        seen.append(after)
        if after == "2":
            return httpx.Response(200, json=[_message_payload("3"), _message_payload("4")])
        if after == "4":
            return httpx.Response(200, json=[])
        return httpx.Response(200, json=[_message_payload("1"), _message_payload("2")])

    with make_client(httpx.MockTransport(handler)) as client:
        messages = list(client.iter_messages_after("10", "0", page_size=2))

    assert [message.id for message in messages] == ["1", "2", "3", "4"]
    assert seen == ["0", "2", "4"]


def test_iter_messages_before_pages_descending() -> None:
    seen: list[str | None] = []

    def handler(request: httpx.Request) -> httpx.Response:
        before = request.url.params.get("before")
        seen.append(before)
        if before is None:
            return httpx.Response(200, json=[_message_payload("3"), _message_payload("4")])
        if before == "3":
            return httpx.Response(200, json=[_message_payload("1"), _message_payload("2")])
        return httpx.Response(200, json=[])

    with make_client(httpx.MockTransport(handler)) as client:
        messages = list(client.iter_messages_before("10", page_size=2))

    assert [message.id for message in messages] == ["4", "3", "2", "1"]
    assert seen == [None, "3", "1"]


def test_pagination_error_page_raises_api_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, json={"message": "Missing permissions"})

    with make_client(httpx.MockTransport(handler)) as client:
        with pytest.raises(DistransAPIError) as raised:
            list(client.iter_messages_after("10", "0"))

    assert raised.value.status_code == 403
    assert raised.value.message == "Missing permissions"


def test_client_retry_policy_wraps_api_transport() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(503, text="try later")
        return httpx.Response(
            200,
            json={
                "id": "1",
                "username": "alice",
                "display_name": None,
                "avatar_hash": None,
                "is_bot": False,
            },
        )

    client = DistransClient(
        "https://example.test/api",
        httpx_args={"transport": httpx.MockTransport(handler)},
        retry=RetryPolicy(attempts=1, backoff=0),
    )
    try:
        me = get_me.sync(client=client.raw)
    finally:
        client.close()

    assert me is not None
    assert calls == 2
