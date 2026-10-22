"""High-level convenience wrapper around the generated client.

The wrapper keeps one ``httpx.Client`` and one generated ``AuthenticatedClient``
for the whole lifetime of the object. Reusing the connection pool also preserves
the ``refresh_token`` cookie set by ``POST /auth/token``, which is required by
the refresh/logout endpoints.
"""

from __future__ import annotations

from collections.abc import Iterator
from io import BytesIO
from typing import Any, TypeVar

import httpx

from .api.auth import post_auth_token, post_auth_token_logout, post_auth_token_refresh
from .api.emojis import get_guild_emojis, post_guild_emoji, update_emoji_icon
from .api.files import post_file
from .api.guilds import put_guild_avatar
from .api.messages import get_channel_pinned_messages, get_messages, post_message
from .api.users import put_me_avatar
from .api.webhooks import (
    delete_webhook_message,
    edit_webhook_message,
    get_webhook_message,
    put_webhook_avatar,
)
from .client import AuthenticatedClient
from .exceptions import DistransAPIError, DistransDownloadError, DistransError
from .gateway import Gateway, build_ssl_context, gateway_url
from .models.allowed_mentions import AllowedMentions
from .models.attachment import Attachment
from .models.edit_webhook_message_body import EditWebhookMessageBody
from .models.embed import Embed
from .models.emoji import Emoji
from .models.error import Error
from .models.file_upload import FileUpload
from .models.message import Message
from .models.post_auth_token_body import PostAuthTokenBody
from .models.post_auth_token_body_grant_type import PostAuthTokenBodyGrantType
from .models.post_message_body import PostMessageBody
from .models.put_guild_avatar_response_200 import PutGuildAvatarResponse200
from .models.put_me_avatar_response_200 import PutMeAvatarResponse200
from .models.put_webhook_avatar_response_200 import PutWebhookAvatarResponse200
from .models.token_response import TokenResponse
from .models.update_emoji_icon_response_200 import UpdateEmojiIconResponse200
from .retry import AsyncRetryTransport, RetryPolicy, RetryTransport
from .types import UNSET, File, Response, Unset

T = TypeVar("T")

_DEFAULT_DOWNLOAD_RETRY = RetryPolicy(attempts=2, methods=frozenset({"GET"}))


def _unwrap(response: Response[Any], expected: type[T]) -> T:
    parsed = response.parsed
    if isinstance(parsed, Error):
        raise DistransAPIError(response.status_code, parsed.message)
    if isinstance(parsed, expected):
        return parsed
    raise DistransError(f"unexpected response (status {int(response.status_code)})")


def _list_page(response: Response[Any]) -> list[Any]:
    parsed = response.parsed
    if isinstance(parsed, Error):
        raise DistransAPIError(response.status_code, parsed.message)
    if isinstance(parsed, list):
        return parsed
    raise DistransError(f"unexpected response (status {int(response.status_code)})")


def _validate_page_size(page_size: int) -> int:
    if not 1 <= page_size <= 100:
        raise ValueError("page_size must be between 1 and 100")
    return page_size


def _prepare_sync_transport(args: dict[str, Any], retry: RetryPolicy | None, verify: bool | str) -> None:
    if retry is None:
        return
    transport = args.pop("transport", None)
    if transport is None:
        transport = httpx.HTTPTransport(verify=verify, retries=0)
    args["transport"] = RetryTransport(transport, retry)


def _prepare_async_transport(args: dict[str, Any], retry: RetryPolicy | None, verify: bool | str) -> None:
    if retry is None:
        return
    transport = args.pop("transport", None)
    if transport is None:
        transport = httpx.AsyncHTTPTransport(verify=verify, retries=0)
    args["transport"] = AsyncRetryTransport(transport, retry)


def _download_client_args(
    download_httpx_args: dict[str, Any] | None,
    *,
    timeout: float,
    verify: bool | str,
) -> dict[str, Any]:
    args = dict(download_httpx_args or {})
    for key in ("headers", "cookies", "auth"):
        args.pop(key, None)
    args.setdefault("timeout", timeout)
    args.setdefault("verify", verify)
    args["follow_redirects"] = True
    return args


def _expect_no_content(response: Response[Any]) -> None:
    parsed = response.parsed
    if isinstance(parsed, Error):
        raise DistransAPIError(response.status_code, parsed.message)
    if not 200 <= int(response.status_code) < 300:
        raise DistransError(f"unexpected response (status {int(response.status_code)})")


def _build_upload_request(endpoint: Any, data: bytes, content_type: str, **kwargs: Any) -> dict[str, Any]:
    if not content_type:
        raise ValueError("content_type is required")
    body = File(payload=BytesIO(data), mime_type=content_type)
    request = endpoint._get_kwargs(body=body, **kwargs)
    request.setdefault("headers", {})["Content-Type"] = content_type
    return request


class DistransClient:
    """Synchronous Distrans client.

    Args:
        base_url: API root including the ``/api`` prefix, for example
            ``https://chat.example.com/api``. Required: the backend is
            self-hosted, so there is no default host.
        token: Access token (JWT or ``bot_`` token). Optional: public endpoints
            and ``POST /auth/token`` work without a token.
        timeout: Passed to ``httpx.Client``.
        verify: TLS verification flag, passed to ``httpx.Client``.
        follow_redirects: Passed to ``httpx.Client``.
        headers: Default headers for every request.
        httpx_args: Extra ``httpx.Client`` keyword arguments (for example
            ``{"transport": httpx.MockTransport(handler)}`` in tests).
        raise_on_unexpected_status: Raise the generated ``UnexpectedStatus`` for
            status codes that are not part of the contract.
        retry: Optional retry policy for the API client. Disabled by default.
        download_timeout: Timeout for public file downloads, in seconds.
        download_httpx_args: Extra ``httpx.Client`` arguments for the download
            client. ``headers``, ``cookies`` and ``auth`` are ignored so the API
            token can never be attached to a public file URL.
        download_retry: Retry policy for downloads. Defaults to retrying ``GET``
            twice; pass ``None`` to disable.
    """

    def __init__(
        self,
        base_url: str,
        token: str | None = None,
        *,
        timeout: float | httpx.Timeout | None = 30.0,
        verify: bool | str = True,
        follow_redirects: bool = False,
        headers: dict[str, str] | None = None,
        httpx_args: dict[str, Any] | None = None,
        raise_on_unexpected_status: bool = True,
        retry: RetryPolicy | None = None,
        download_timeout: float = 30.0,
        download_httpx_args: dict[str, Any] | None = None,
        download_retry: RetryPolicy | None = _DEFAULT_DOWNLOAD_RETRY,
    ) -> None:
        api_args = dict(httpx_args or {})
        _prepare_sync_transport(api_args, retry, verify)
        self._http = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            verify=verify,
            follow_redirects=follow_redirects,
            headers=dict(headers or {}),
            **api_args,
        )
        download_args = _download_client_args(download_httpx_args, timeout=download_timeout, verify=verify)
        _prepare_sync_transport(download_args, download_retry, verify)
        self._download_http = httpx.Client(**download_args)
        self._verify = verify
        self._client = AuthenticatedClient(
            base_url=base_url,
            token=token or "",
            raise_on_unexpected_status=raise_on_unexpected_status,
        )
        self._client.set_httpx_client(self._http)
        if token:
            self.set_token(token)

    @property
    def raw(self) -> AuthenticatedClient:
        """The underlying generated client, for calling ``generated.api`` functions."""
        return self._client

    @property
    def http(self) -> httpx.Client:
        """The underlying ``httpx.Client`` (shared cookie jar)."""
        return self._http

    @property
    def download_http(self) -> httpx.Client:
        """The separate ``httpx.Client`` used by :meth:`download` (no API token)."""
        return self._download_http

    @property
    def base_url(self) -> str:
        return str(self._http.base_url)

    def set_token(self, token: str | None) -> None:
        self._client.token = token or ""
        if token:
            self._http.headers["Authorization"] = f"{self._client.prefix} {token}"
        else:
            self._http.headers.pop("Authorization", None)

    def close(self) -> None:
        try:
            self._http.close()
        finally:
            self._download_http.close()

    def gateway(
        self,
        *,
        token: str | None = None,
        token_provider: Any = None,
        auto_reconnect: bool = False,
        on_reconnect: Any = None,
        connect_timeout: float | None = 10.0,
        auth_timeout: float | None = 10.0,
        close_timeout: float | None = 10.0,
        max_message_size: int | None = None,
        proxy: str | bool | None = True,
    ) -> Gateway:
        """Create a :class:`~distrans_client.gateway.Gateway` for this deployment.

        By default the gateway authenticates with the client's current access
        token, re-read on every (re)connect, so :meth:`refresh` is honored.

        Args:
            token: Explicit token, overriding the client's current token.
            token_provider: Callable returning the token for the next connect.
            auto_reconnect: Reconnect after unexpected closes.
            on_reconnect: Called with the gateway after reconnecting.
            connect_timeout: Timeout for the WebSocket/HTTP handshake.
            auth_timeout: Timeout for ``identify``/``hello``.
            close_timeout: Timeout for the closing handshake.
            max_message_size: Maximum accepted frame size in bytes.
            proxy: Proxy setting forwarded to ``websockets``.
        """
        if token_provider is None and token is None:
            token_provider = lambda: self._client.token or None  # noqa: E731

        return Gateway(
            gateway_url(self.base_url),
            token=token,
            token_provider=token_provider,
            auto_reconnect=auto_reconnect,
            on_reconnect=on_reconnect,
            connect_timeout=connect_timeout,
            auth_timeout=auth_timeout,
            close_timeout=close_timeout,
            max_message_size=max_message_size,
            proxy=proxy,
            ssl=build_ssl_context(self._verify),
        )

    def __enter__(self) -> DistransClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def login(self, username: str, password: str) -> TokenResponse:
        """Password grant. Stores the returned access token and the refresh cookie."""
        body = PostAuthTokenBody(
            grant_type=PostAuthTokenBodyGrantType.PASSWORD,
            username=username,
            password=password,
        )
        response = post_auth_token.sync_detailed(client=self._client, body=body)
        result = _unwrap(response, TokenResponse)
        self.set_token(result.access_token)
        return result

    def refresh(self) -> TokenResponse:
        """Rotate the refresh cookie and install the new access token."""
        result = _unwrap(
            post_auth_token_refresh.sync_detailed(client=self._client),
            TokenResponse,
        )
        self.set_token(result.access_token)
        return result

    def logout(self) -> None:
        """Revoke the refresh token and clear the local access token."""
        response = post_auth_token_logout.sync_detailed(client=self._client)
        _expect_no_content(response)
        self.set_token(None)

    def upload_file(self, name: str, data: bytes, content_type: str) -> FileUpload:
        """Upload raw bytes to ``POST /files``.

        ``content_type`` is mandatory: the server validates the request
        ``Content-Type`` against ``files.whitelist`` and rejects
        ``application/octet-stream`` unless it is explicitly whitelisted.
        """
        return self._upload(post_file, FileUpload, data, content_type, name=name)

    def set_my_avatar(self, data: bytes, content_type: str) -> str:
        result = self._upload(put_me_avatar, PutMeAvatarResponse200, data, content_type)
        return result.avatar_hash

    def set_guild_avatar(self, guild_id: str, data: bytes, content_type: str) -> str:
        result = self._upload(put_guild_avatar, PutGuildAvatarResponse200, data, content_type, guild_id=guild_id)
        return result.avatar_hash

    def create_emoji(self, guild_id: str, name: str, data: bytes, content_type: str) -> Emoji:
        return self._upload(post_guild_emoji, Emoji, data, content_type, guild_id=guild_id, name=name)

    def set_emoji_icon(self, emoji_id: str, data: bytes, content_type: str) -> str:
        result = self._upload(update_emoji_icon, UpdateEmojiIconResponse200, data, content_type, emoji_id=emoji_id)
        return result.icon_hash

    def set_webhook_avatar(self, webhook_id: str, data: bytes, content_type: str) -> str | None:
        result = self._upload(
            put_webhook_avatar,
            PutWebhookAvatarResponse200,
            data,
            content_type,
            webhook_id=webhook_id,
        )
        value = result.avatar_hash
        return None if isinstance(value, Unset) else value

    def get_webhook_message(self, webhook_id: str, token: str, message_id: str) -> Message:
        """Get a message sent by a webhook using its execute token."""
        response = get_webhook_message.sync_detailed(
            client=self._client,
            webhook_id=webhook_id,
            token=token,
            message_id=message_id,
        )
        return _unwrap(response, Message)

    def edit_webhook_message(
        self,
        webhook_id: str,
        token: str,
        message_id: str,
        *,
        content: str | Unset = UNSET,
        embeds: list[Embed] | None | Unset = UNSET,
    ) -> Message:
        """Edit a message sent by a webhook using its execute token.

        Omitted fields keep their stored values; ``embeds=None`` or ``[]``
        clears the embeds.
        """
        body = EditWebhookMessageBody(content=content, embeds=embeds)
        response = edit_webhook_message.sync_detailed(
            client=self._client,
            webhook_id=webhook_id,
            token=token,
            message_id=message_id,
            body=body,
        )
        return _unwrap(response, Message)

    def delete_webhook_message(self, webhook_id: str, token: str, message_id: str) -> None:
        """Delete a message sent by a webhook using its execute token."""
        response = delete_webhook_message.sync_detailed(
            client=self._client,
            webhook_id=webhook_id,
            token=token,
            message_id=message_id,
        )
        _expect_no_content(response)

    def download(self, url: str) -> bytes:
        """GET a public URL (for example an S3 ``public_url``) without the API token."""
        response = self._download_http.get(url)
        if not 200 <= response.status_code < 300:
            raise DistransDownloadError(url, response.status_code, response.text)
        return response.content

    def download_attachment(self, attachment: Attachment) -> bytes:
        """Download an attachment through its :attr:`Attachment.public_url`."""
        if attachment.public_url is None:
            raise DistransError(f"attachment {attachment.id} has no public URL")
        return self.download(attachment.public_url)

    def send_message(
        self,
        channel_id: str,
        content: str,
        *,
        reply_to_id: str | None = None,
        embeds: list[Embed] | None | Unset = UNSET,
        allowed_mentions: AllowedMentions | None | Unset = UNSET,
    ) -> Message:
        """Send a message, optionally as a reply.

        If the server rejects a reply target with ``400`` and mentions
        ``reply_to_id`` in the error message, the message is sent once more
        without the reply target.
        """
        body = PostMessageBody(
            content=content,
            embeds=embeds,
            allowed_mentions=allowed_mentions,
        )
        if reply_to_id is not None:
            body.reply_to_id = reply_to_id

        response = post_message.sync_detailed(client=self._client, channel_id=channel_id, body=body)
        if int(response.status_code) == 201 and isinstance(response.parsed, Message):
            return response.parsed

        parsed = response.parsed
        if (
            int(response.status_code) == 400
            and isinstance(parsed, Error)
            and reply_to_id is not None
            and "reply_to_id" in parsed.message
        ):
            fallback = PostMessageBody(
                content=content,
                embeds=embeds,
                allowed_mentions=allowed_mentions,
            )
            response = post_message.sync_detailed(client=self._client, channel_id=channel_id, body=fallback)
            if int(response.status_code) == 201 and isinstance(response.parsed, Message):
                return response.parsed
            parsed = response.parsed

        if isinstance(parsed, Error):
            raise DistransAPIError(response.status_code, parsed.message)
        raise DistransError(f"unexpected response (status {int(response.status_code)})")

    def reply(self, channel_id: str, message_id: str, content: str, **kwargs: Any) -> Message:
        """Send ``content`` as a reply to ``message_id``."""
        return self.send_message(channel_id, content, reply_to_id=message_id, **kwargs)

    def iter_guild_emojis(self, guild_id: str, *, page_size: int = 100) -> Iterator[Emoji]:
        """Iterate over a guild's custom emojis in ascending id order."""
        return self._iter_guild_emojis(guild_id, _validate_page_size(page_size))

    def iter_messages_after(
        self,
        channel_id: str,
        after: str,
        *,
        page_size: int = 100,
    ) -> Iterator[Message]:
        """Iterate over messages after ``after``, oldest to newest."""
        return self._iter_messages_after(channel_id, after, _validate_page_size(page_size))

    def iter_messages_before(
        self,
        channel_id: str,
        before: str | None = None,
        *,
        page_size: int = 100,
    ) -> Iterator[Message]:
        """Iterate over messages before ``before``, newest to oldest.

        ``None`` starts from the latest message.
        """
        return self._iter_messages_before(channel_id, before, _validate_page_size(page_size))

    def iter_pinned_messages_after(
        self,
        channel_id: str,
        after: str,
        *,
        page_size: int = 100,
    ) -> Iterator[Message]:
        """Iterate over pinned messages after ``after``, oldest to newest."""
        return self._iter_pinned_messages_after(channel_id, after, _validate_page_size(page_size))

    def iter_pinned_messages_before(
        self,
        channel_id: str,
        before: str | None = None,
        *,
        page_size: int = 100,
    ) -> Iterator[Message]:
        """Iterate over pinned messages before ``before``, newest to oldest.

        ``None`` starts from the latest pinned message.
        """
        return self._iter_pinned_messages_before(channel_id, before, _validate_page_size(page_size))

    def _iter_guild_emojis(self, guild_id: str, page_size: int) -> Iterator[Emoji]:
        cursor: str | None = None
        while True:
            response = get_guild_emojis.sync_detailed(
                client=self._client,
                guild_id=guild_id,
                limit=page_size,
                after=cursor if cursor is not None else UNSET,
            )
            page = _list_page(response)
            if not page:
                break
            yield from page

            last_id = page[-1].id
            if len(page) < page_size or (cursor is not None and int(last_id) <= int(cursor)):
                break
            cursor = last_id

    def _iter_messages_after(self, channel_id: str, after: str, page_size: int) -> Iterator[Message]:
        cursor = after
        while True:
            response = get_messages.sync_detailed(
                client=self._client,
                channel_id=channel_id,
                limit=page_size,
                after=cursor,
            )
            page = _list_page(response)
            if not page:
                break
            yield from page

            last_id = page[-1].id
            if int(last_id) <= int(cursor):
                break
            cursor = last_id

    def _iter_messages_before(self, channel_id: str, before: str | None, page_size: int) -> Iterator[Message]:
        cursor = before
        while True:
            response = get_messages.sync_detailed(
                client=self._client,
                channel_id=channel_id,
                limit=page_size,
                before=cursor if cursor is not None else UNSET,
            )
            page = _list_page(response)
            if not page:
                break

            # The API returns ascending pages; reverse each page so the iterator
            # is newest-to-oldest overall.
            yield from reversed(page)
            oldest_id = page[0].id
            if cursor is not None and int(oldest_id) >= int(cursor):
                break
            cursor = oldest_id

    def _iter_pinned_messages_after(
        self,
        channel_id: str,
        after: str,
        page_size: int,
    ) -> Iterator[Message]:
        cursor = after
        while True:
            response = get_channel_pinned_messages.sync_detailed(
                client=self._client,
                channel_id=channel_id,
                limit=page_size,
                after=cursor,
            )
            page = _list_page(response)
            if not page:
                break
            yield from page

            last_id = page[-1].id
            if int(last_id) <= int(cursor):
                break
            cursor = last_id

    def _iter_pinned_messages_before(
        self,
        channel_id: str,
        before: str | None,
        page_size: int,
    ) -> Iterator[Message]:
        cursor = before
        while True:
            response = get_channel_pinned_messages.sync_detailed(
                client=self._client,
                channel_id=channel_id,
                limit=page_size,
                before=cursor if cursor is not None else UNSET,
            )
            page = _list_page(response)
            if not page:
                break

            # The API returns ascending pages; reverse each page so the iterator
            # is newest-to-oldest overall.
            yield from reversed(page)
            oldest_id = page[0].id
            if cursor is not None and int(oldest_id) >= int(cursor):
                break
            cursor = oldest_id

    def _upload(self, endpoint: Any, expected: type[T], data: bytes, content_type: str, **kwargs: Any) -> T:
        request = _build_upload_request(endpoint, data, content_type, **kwargs)
        raw = self._http.request(**request)
        return _unwrap(endpoint._build_response(client=self._client, response=raw), expected)
