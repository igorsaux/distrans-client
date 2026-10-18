"""Asynchronous WebSocket gateway client."""

from __future__ import annotations

import asyncio
import inspect
import random
import time
from collections.abc import AsyncIterator, Awaitable, Callable
from typing import Any

from websockets.asyncio.client import connect as ws_connect
from websockets.exceptions import ConnectionClosed, InvalidHandshake, InvalidStatus, InvalidURI

from ..exceptions import (
    GatewayAuthError,
    GatewayClosedError,
    GatewayConnectionError,
    GatewayHandshakeError,
    GatewayProtocolError,
)
from ._util import close_details
from .events import DispatchEvent, UnknownDispatchEvent
from .protocol import HelloFrame, ack_message, identify_message, parse_frame

__all__ = ["AsyncGateway"]

TokenProvider = Callable[[], str | None | Awaitable[str | None]]
ReconnectHandler = Callable[["AsyncGateway"], Any | Awaitable[Any]]

_POLL_SLICE = 0.5


class AsyncGateway:
    """Asynchronous Distrans gateway connection.

    Mirrors :class:`~distrans_client.gateway.sync.Gateway`: lazy connect,
    automatic ``ack`` heartbeat on a background task, typed dispatch events and
    optional reconnection. Use it as an async context manager::

        async with client.gateway() as gw:
            async for event in gw:
                ...

    Args:
        url: Full gateway URL, normally produced by
            :func:`distrans_client.gateway.gateway_url`.
        token: Access token (JWT) or static ``bot_`` token.
        token_provider: Callable (sync or async) returning the token for the
            next connection attempt.
        auto_reconnect: Reconnect after an unexpected close. Events are not
            replayed by the server.
        on_reconnect: Callable (sync or async) invoked after a reconnection.
        connect_timeout: Timeout for the TCP/TLS/HTTP handshake, in seconds.
        auth_timeout: Timeout for ``identify``/``hello``, in seconds.
        close_timeout: Timeout for the closing handshake, in seconds.
        max_message_size: Maximum accepted frame size in bytes.
        proxy: Proxy setting forwarded to ``websockets``; ``None`` disables it.
        ssl: TLS context for ``wss://`` URLs.
    """

    def __init__(
        self,
        url: str,
        token: str | None = None,
        *,
        token_provider: TokenProvider | None = None,
        auto_reconnect: bool = False,
        on_reconnect: ReconnectHandler | None = None,
        connect_timeout: float | None = 10.0,
        auth_timeout: float | None = 10.0,
        close_timeout: float | None = 10.0,
        max_message_size: int | None = None,
        proxy: str | bool | None = True,
        ssl: Any = None,
    ) -> None:
        self.url = url
        self._token = token
        self._token_provider = token_provider
        self.auto_reconnect = auto_reconnect
        self._on_reconnect = on_reconnect
        self.connect_timeout = connect_timeout
        self.auth_timeout = auth_timeout
        self.close_timeout = close_timeout
        self.max_message_size = max_message_size
        self.proxy = proxy
        self._ssl = ssl

        self._lock = asyncio.Lock()
        self._closed = asyncio.Event()
        self._ws: Any = None
        self._heartbeat: asyncio.Task[None] | None = None
        self._heartbeat_interval_ms: int | None = None

    # ---------------------------------------------------------------- state

    @property
    def connected(self) -> bool:
        return self._ws is not None

    @property
    def closed(self) -> bool:
        return self._closed.is_set()

    @property
    def heartbeat_interval_ms(self) -> int | None:
        """The interval announced by the last ``hello`` frame."""
        return self._heartbeat_interval_ms

    # -------------------------------------------------------------- connect

    async def connect(self) -> AsyncGateway:
        """Open the connection and complete ``identify``/``hello``.

        Raises the same exceptions as the synchronous gateway.
        """
        async with self._lock:
            if self._closed.is_set():
                raise GatewayClosedError(None, "gateway is closed")
            if self._ws is not None:
                return self

            await self._connect_locked()

        return self

    async def _connect_locked(self) -> None:
        token = await self._resolve_token()
        if not token:
            raise GatewayAuthError("gateway identify requires an access token")

        kwargs: dict[str, Any] = {
            "open_timeout": self.connect_timeout,
            "close_timeout": self.close_timeout,
            "ping_interval": None,
            "proxy": self.proxy,
        }
        if self.max_message_size is not None:
            kwargs["max_size"] = self.max_message_size
        if self.url.startswith("wss://") and self._ssl is not None:
            kwargs["ssl"] = self._ssl

        try:
            ws = await ws_connect(self.url, **kwargs)
        except InvalidStatus as exc:
            raise GatewayHandshakeError(exc.response.status_code) from exc
        except (InvalidURI, InvalidHandshake, OSError, TimeoutError) as exc:
            raise GatewayConnectionError(f"gateway connection failed: {exc}") from exc

        connected_at = time.monotonic()
        try:
            await ws.send(identify_message(token))
            hello = await self._await_hello(ws, connected_at)
        except GatewayProtocolError:
            await self._discard(ws)
            raise
        except TimeoutError as exc:
            await self._discard(ws)
            raise GatewayConnectionError("timed out waiting for the gateway 'hello' frame") from exc
        except ConnectionClosed as exc:
            await self._discard(ws)
            code, reason = close_details(exc)
            if code in (None, 1000, 1005):
                raise GatewayAuthError("the server closed the gateway before 'hello'") from exc
            raise GatewayConnectionError(
                f"the server closed the gateway before 'hello' (code {code}, reason {reason!r})"
            ) from exc

        self._ws = ws
        self._heartbeat_interval_ms = hello.heartbeat_interval_ms
        self._heartbeat = asyncio.create_task(
            self._heartbeat_loop(ws, connected_at, hello.heartbeat_interval_ms / 1000.0),
            name="distrans-gateway-heartbeat",
        )

    async def _await_hello(self, ws: Any, connected_at: float) -> HelloFrame:
        deadline = None if self.auth_timeout is None else connected_at + self.auth_timeout

        while True:
            if deadline is None:
                raw = await ws.recv()
            else:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError
                raw = await asyncio.wait_for(ws.recv(), timeout=remaining)

            if isinstance(raw, bytes):
                raise GatewayProtocolError("the gateway sent a binary frame")
            frame = parse_frame(raw)
            if isinstance(frame, HelloFrame):
                return frame
            if frame is None:
                continue
            raise GatewayProtocolError("the gateway sent a dispatch before 'hello'")

    async def _resolve_token(self) -> str | None:
        if self._token_provider is None:
            return self._token

        value = self._token_provider()
        if inspect.isawaitable(value):
            value = await value
        return value

    # ------------------------------------------------------------- heartbeat

    async def _heartbeat_loop(self, ws: Any, connected_at: float, interval: float) -> None:
        next_ack = connected_at + interval

        try:
            while True:
                wait = next_ack - time.monotonic()
                if wait > 0:
                    await asyncio.sleep(wait)

                await ws.send(ack_message())

                next_ack += interval
                now = time.monotonic()
                if next_ack <= now:
                    next_ack = now + interval
        except asyncio.CancelledError:
            raise
        except Exception:
            return

    async def _stop_heartbeat_task(self) -> None:
        task = self._heartbeat
        self._heartbeat = None
        if task is None or task is asyncio.current_task():
            return

        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        except Exception:
            pass

    # ----------------------------------------------------------------- recv

    async def recv(self, timeout: float | None = None) -> DispatchEvent | UnknownDispatchEvent:
        """Return the next dispatch event.

        Raises the built-in ``TimeoutError`` after ``timeout`` seconds without
        an event and :class:`GatewayClosedError` when the connection ends and
        reconnection is disabled.
        """
        deadline = None if timeout is None else time.monotonic() + timeout

        while True:
            if self._closed.is_set() and self._ws is None:
                raise GatewayClosedError(None, "gateway is closed")

            await self.connect()
            ws = self._ws
            assert ws is not None

            try:
                frame = await self._read_frame(ws, deadline)
            except TimeoutError:
                raise
            except ConnectionClosed as exc:
                await self._lose_transport(ws)
                if not self.auto_reconnect or self._closed.is_set():
                    raise GatewayClosedError(*close_details(exc)) from exc
                await self._reconnect(deadline)
                continue
            except (GatewayProtocolError, GatewayAuthError):
                await self._lose_transport(ws)
                raise
            except (OSError, ConnectionError) as exc:
                await self._lose_transport(ws)
                if not self.auto_reconnect or self._closed.is_set():
                    raise GatewayConnectionError(f"gateway connection lost: {exc}") from exc
                await self._reconnect(deadline)
                continue

            if isinstance(frame, HelloFrame):
                continue

            return frame

    async def _read_frame(self, ws: Any, deadline: float | None) -> Any:
        while True:
            if self._closed.is_set():
                raise GatewayClosedError(None, "gateway is closed")

            if deadline is None:
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=_POLL_SLICE)
                except TimeoutError:
                    continue
            else:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=min(remaining, _POLL_SLICE))
                except TimeoutError:
                    continue

            if isinstance(raw, bytes):
                raise GatewayProtocolError("the gateway sent a binary frame")

            frame = parse_frame(raw)
            if frame is None:
                continue

            return frame

    async def _reconnect(self, deadline: float | None) -> None:
        delay = 0.0
        immediate = True

        while not self._closed.is_set():
            if not immediate:
                delay = min(max(delay * 2, 1.0), 30.0)
                jittered = random.uniform(delay / 2, delay)
                if not await self._wait_or_closed(jittered, deadline):
                    raise TimeoutError
            immediate = False

            try:
                await self.connect()
            except GatewayAuthError:
                raise
            except GatewayHandshakeError as exc:
                if 400 <= exc.status_code < 500:
                    raise
            except GatewayConnectionError:
                continue
            else:
                if self._on_reconnect is not None:
                    result = self._on_reconnect(self)
                    if inspect.isawaitable(result):
                        await result
                return

        raise GatewayClosedError(None, "gateway is closed")

    async def _wait_or_closed(self, delay: float, deadline: float | None) -> bool:
        if deadline is not None:
            delay = min(delay, max(0.0, deadline - time.monotonic()))

        try:
            await asyncio.wait_for(self._closed.wait(), timeout=delay)
        except TimeoutError:
            return True

        return False

    # ---------------------------------------------------------------- close

    async def close(self, code: int = 1000, reason: str = "") -> None:
        """Close the connection. Idempotent."""
        self._closed.set()

        async with self._lock:
            ws = self._ws
            self._ws = None

        await self._stop_heartbeat_task()

        if ws is not None:
            try:
                await ws.close(code, reason)
            except Exception:
                pass

    async def _lose_transport(self, ws: Any) -> None:
        if self._ws is ws:
            self._ws = None

        await self._stop_heartbeat_task()
        await self._discard(ws)

    @staticmethod
    async def _discard(ws: Any) -> None:
        try:
            await ws.close()
        except Exception:
            pass

    async def __aenter__(self) -> AsyncGateway:
        return await self.connect()

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    def __aiter__(self) -> AsyncIterator[DispatchEvent | UnknownDispatchEvent]:
        return self

    async def __anext__(self) -> DispatchEvent | UnknownDispatchEvent:
        if self._closed.is_set() and self._ws is None:
            raise StopAsyncIteration

        return await self.recv()
