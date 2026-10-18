"""Asynchronous convenience wrapper around the generated client.

Mirrors :class:`distrans_client.facade.DistransClient` for asyncio. One
``httpx.AsyncClient`` and one generated ``AuthenticatedClient`` are kept for the
lifetime of the object, preserving the connection pool and the
``refresh_token`` cookie issued by ``POST /auth/token``.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any, TypeVar

import httpx

from .api.auth import post_auth_token, post_auth_token_logout, post_auth_token_refresh
from .api.emojis import get_guild_emojis, post_guild_emoji, update_emoji_icon
from .api.files import post_file
from .api.guilds import put_guild_avatar
from .api.messages import get_messages, post_message
from .api.users import put_me_avatar
from .api.webhooks import put_webhook_avatar
from .client import AuthenticatedClient
from .exceptions import DistransAPIError, DistransDownloadError, DistransError
from .facade import (
    _DEFAULT_DOWNLOAD_RETRY,
    _build_upload_request,
    _download_client_args,
    _expect_no_content,
    _list_page,
    _prepare_async_transport,
    _unwrap,
    _validate_page_size,
)
from .gateway import AsyncGateway, build_ssl_context, gateway_url
from .models.allowed_mentions import AllowedMentions
from .models.attachment import Attachment
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
from .retry import RetryPolicy
from .types import UNSET, Unset

T = TypeVar("T")


class AsyncDistransClient:
    """Asyncio Distrans client.

    Args:
        base_url: API root including the ``/api`` prefix, for example
            ``https://chat.example.com/api``. Required: the backend is
            self-hosted, so there is no default host.
        token: Access token (JWT or ``bot_`` token). Optional: public endpoints
            and ``POST /auth/token`` work without a token.
        timeout: Passed to ``httpx.AsyncClient``.
        verify: TLS verification flag, passed to ``httpx.AsyncClient`` and to
            the gateway.
        follow_redirects: Passed to ``httpx.AsyncClient``.
        headers: Default headers for every request.
        httpx_args: Extra ``httpx.AsyncClient`` keyword arguments (for example
            ``{"transport": httpx.MockTransport(handler)}`` in tests).
        raise_on_unexpected_status: Raise the generated ``UnexpectedStatus`` for
            status codes that are not part of the contract.
        retry: Optional retry policy for the API client. Disabled by default.
        download_timeout: Timeout for public file downloads, in seconds.
        download_httpx_args: Extra ``httpx.AsyncClient`` arguments for the
            download client. ``headers``, ``cookies`` and ``auth`` are ignored
            so the API token can never be attached to a public file URL.
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
        _prepare_async_transport(api_args, retry, verify)
        self._http = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            verify=verify,
            follow_redirects=follow_redirects,
            headers=dict(headers or {}),
            **api_args,
        )
        download_args = _download_client_args(download_httpx_args, timeout=download_timeout, verify=verify)
        _prepare_async_transport(download_args, download_retry, verify)
        self._download_http = httpx.AsyncClient(**download_args)
        self._verify = verify
        self._client = AuthenticatedClient(
            base_url=base_url,
            token=token or "",
            raise_on_unexpected_status=raise_on_unexpected_status,
        )
        self._client.set_async_httpx_client(self._http)
        if token:
            self.set_token(token)

    @property
    def raw(self) -> AuthenticatedClient:
        """The underlying generated client, for calling ``generated.api`` functions."""
        return self._client

    @property
    def http(self) -> httpx.AsyncClient:
        """The underlying ``httpx.AsyncClient`` (shared cookie jar)."""
        return self._http

    @property
    def download_http(self) -> httpx.AsyncClient:
        """The separate ``httpx.AsyncClient`` used by :meth:`download` (no API token)."""
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

    async def close(self) -> None:
        try:
            await self._http.aclose()
        finally:
            await self._download_http.aclose()

    async def aclose(self) -> None:
        """Alias of :meth:`close` matching the ``httpx`` spelling."""
        await self.close()

    async def __aenter__(self) -> AsyncDistransClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    async def login(self, username: str, password: str) -> TokenResponse:
        """Password grant. Stores the returned access token and the refresh cookie."""
        body = PostAuthTokenBody(
            grant_type=PostAuthTokenBodyGrantType.PASSWORD,
            username=username,
            password=password,
        )
        response = await post_auth_token.asyncio_detailed(client=self._client, body=body)
        result = _unwrap(response, TokenResponse)
        self.set_token(result.access_token)
        return result

    async def refresh(self) -> TokenResponse:
        """Rotate the refresh cookie and install the new access token."""
        result = _unwrap(
            await post_auth_token_refresh.asyncio_detailed(client=self._client),
            TokenResponse,
        )
        self.set_token(result.access_token)
        return result

    async def logout(self) -> None:
        """Revoke the refresh token and clear the local access token."""
        response = await post_auth_token_logout.asyncio_detailed(client=self._client)
        _expect_no_content(response)
        self.set_token(None)

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
    ) -> AsyncGateway:
        """Create an :class:`~distrans_client.gateway.AsyncGateway` for this deployment.

        By default the gateway authenticates with the client's current access
        token, re-read on every (re)connect, so :meth:`refresh` is honored.

        This method is intentionally synchronous: the connection is opened by
        ``async with`` or by the first ``await recv()``.
        """
        if token_provider is None and token is None:
            token_provider = lambda: self._client.token or None  # noqa: E731

        return AsyncGateway(
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

    async def upload_file(self, name: str, data: bytes, content_type: str) -> FileUpload:
        """Upload raw bytes to ``POST /files``.

        ``content_type`` is mandatory: the server validates the request
        ``Content-Type`` against ``files.whitelist`` and rejects
        ``application/octet-stream`` unless it is explicitly whitelisted.
        """
        return await self._upload(post_file, FileUpload, data, content_type, name=name)

    async def set_my_avatar(self, data: bytes, content_type: str) -> str:
        result = await self._upload(put_me_avatar, PutMeAvatarResponse200, data, content_type)
        return result.avatar_hash

    async def set_guild_avatar(self, guild_id: str, data: bytes, content_type: str) -> str:
        result = await self._upload(
            put_guild_avatar,
            PutGuildAvatarResponse200,
            data,
            content_type,
            guild_id=guild_id,
        )
        return result.avatar_hash

    async def create_emoji(self, guild_id: str, name: str, data: bytes, content_type: str) -> Emoji:
        return await self._upload(
            post_guild_emoji,
            Emoji,
            data,
            content_type,
            guild_id=guild_id,
            name=name,
        )

    async def set_emoji_icon(self, emoji_id: str, data: bytes, content_type: str) -> str:
        result = await self._upload(
            update_emoji_icon,
            UpdateEmojiIconResponse200,
            data,
            content_type,
            emoji_id=emoji_id,
        )
        return result.icon_hash

    async def set_webhook_avatar(self, webhook_id: str, data: bytes, content_type: str) -> str | None:
        result = await self._upload(
            put_webhook_avatar,
            PutWebhookAvatarResponse200,
            data,
            content_type,
            webhook_id=webhook_id,
        )
        value = result.avatar_hash
        return None if isinstance(value, Unset) else value

    async def download(self, url: str) -> bytes:
        """GET a public URL (for example an S3 ``public_url``) without the API token."""
        response = await self._download_http.get(url)
        if not 200 <= response.status_code < 300:
            raise DistransDownloadError(url, response.status_code, response.text)
        return response.content

    async def download_attachment(self, attachment: Attachment) -> bytes:
        """Download an attachment through its :attr:`Attachment.public_url`."""
        if attachment.public_url is None:
            raise DistransError(f"attachment {attachment.id} has no public URL")
        return await self.download(attachment.public_url)

    async def send_message(
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

        response = await post_message.asyncio_detailed(client=self._client, channel_id=channel_id, body=body)
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
            response = await post_message.asyncio_detailed(client=self._client, channel_id=channel_id, body=fallback)
            if int(response.status_code) == 201 and isinstance(response.parsed, Message):
                return response.parsed
            parsed = response.parsed

        if isinstance(parsed, Error):
            raise DistransAPIError(response.status_code, parsed.message)
        raise DistransError(f"unexpected response (status {int(response.status_code)})")

    async def reply(self, channel_id: str, message_id: str, content: str, **kwargs: Any) -> Message:
        """Send ``content`` as a reply to ``message_id``."""
        return await self.send_message(channel_id, content, reply_to_id=message_id, **kwargs)

    def iter_guild_emojis(self, guild_id: str, *, page_size: int = 100) -> AsyncIterator[Emoji]:
        """Iterate over a guild's custom emojis in ascending id order."""
        return self._iter_guild_emojis(guild_id, _validate_page_size(page_size))

    def iter_messages_after(
        self,
        channel_id: str,
        after: str,
        *,
        page_size: int = 100,
    ) -> AsyncIterator[Message]:
        """Iterate over messages after ``after``, oldest to newest."""
        return self._iter_messages_after(channel_id, after, _validate_page_size(page_size))

    def iter_messages_before(
        self,
        channel_id: str,
        before: str | None = None,
        *,
        page_size: int = 100,
    ) -> AsyncIterator[Message]:
        """Iterate over messages before ``before``, newest to oldest.

        ``None`` starts from the latest message.
        """
        return self._iter_messages_before(channel_id, before, _validate_page_size(page_size))

    async def _iter_guild_emojis(self, guild_id: str, page_size: int) -> AsyncIterator[Emoji]:
        cursor: str | None = None
        while True:
            response = await get_guild_emojis.asyncio_detailed(
                client=self._client,
                guild_id=guild_id,
                limit=page_size,
                after=cursor if cursor is not None else UNSET,
            )
            page = _list_page(response)
            if not page:
                break
            for emoji in page:
                yield emoji

            last_id = page[-1].id
            if len(page) < page_size or (cursor is not None and int(last_id) <= int(cursor)):
                break
            cursor = last_id

    async def _iter_messages_after(self, channel_id: str, after: str, page_size: int) -> AsyncIterator[Message]:
        cursor = after
        while True:
            response = await get_messages.asyncio_detailed(
                client=self._client,
                channel_id=channel_id,
                limit=page_size,
                after=cursor,
            )
            page = _list_page(response)
            if not page:
                break
            for message in page:
                yield message

            last_id = page[-1].id
            if int(last_id) <= int(cursor):
                break
            cursor = last_id

    async def _iter_messages_before(
        self,
        channel_id: str,
        before: str | None,
        page_size: int,
    ) -> AsyncIterator[Message]:
        cursor = before
        while True:
            response = await get_messages.asyncio_detailed(
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
            for message in reversed(page):
                yield message
            oldest_id = page[0].id
            if cursor is not None and int(oldest_id) >= int(cursor):
                break
            cursor = oldest_id

    async def _upload(
        self,
        endpoint: Any,
        expected: type[T],
        data: bytes,
        content_type: str,
        **kwargs: Any,
    ) -> T:
        request = _build_upload_request(endpoint, data, content_type, **kwargs)
        # httpx.AsyncClient rejects a synchronous file object; send the bytes.
        request["content"] = data
        raw = await self._http.request(**request)
        return _unwrap(endpoint._build_response(client=self._client, response=raw), expected)
