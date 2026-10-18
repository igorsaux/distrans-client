"""Synchronous WebSocket gateway client."""

from __future__ import annotations

import random
import threading
import time
from collections.abc import Callable, Iterator
from typing import Any

from websockets.exceptions import ConnectionClosed, InvalidHandshake, InvalidStatus, InvalidURI
from websockets.sync.client import connect as ws_connect

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

__all__ = ["Gateway"]

TokenProvider = Callable[[], str | None]
ReconnectHandler = Callable[["Gateway"], None]

_POLL_SLICE = 0.5


class Gateway:
    """Synchronous Distrans gateway connection.

    The object is lazy: the WebSocket connection is opened by :meth:`connect`,
    on ``with`` entry, or by the first :meth:`recv`. A background thread sends
    the application-level ``ack`` heartbeat, so events can be processed at any
    pace without the server dropping the connection.

    Args:
        url: Full gateway URL, normally produced by
            :func:`distrans_client.gateway.gateway_url`.
        token: Access token (JWT) or static ``bot_`` token. Ignored when
            ``token_provider`` is given.
        token_provider: Callable returning the token to use for the next
            connection attempt. It is called before every (re)connect, so a
            refreshed access token is picked up automatically.
        auto_reconnect: Reconnect after an unexpected close. The server does
            not replay events, so callers must resynchronise state themselves
            (for example from ``on_reconnect``). Disabled by default.
        on_reconnect: Called with the gateway after a successful reconnection.
        connect_timeout: Timeout for the TCP/TLS/HTTP handshake, in seconds.
        auth_timeout: Timeout for ``identify``/``hello``, in seconds.
        close_timeout: Timeout for the closing handshake, in seconds.
        max_message_size: Maximum accepted frame size in bytes; ``None`` keeps
            the ``websockets`` default.
        proxy: Proxy setting forwarded to ``websockets``. ``None`` disables the
            system proxy, which is also useful in local tests.
        ssl: TLS context. ``None`` uses the ``websockets`` default for
            ``wss://`` URLs.
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

        self._lock = threading.Lock()
        self._closed = threading.Event()
        self._ws: Any = None
        self._heartbeat: threading.Thread | None = None
        self._heartbeat_stop: threading.Event | None = None
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

    def connect(self) -> Gateway:
        """Open the connection and complete ``identify``/``hello``.

        Raises:
            GatewayAuthError: no token is available or the server refused it.
            GatewayHandshakeError: the HTTP upgrade was rejected.
            GatewayConnectionError: the connection could not be established.
            GatewayProtocolError: the server sent a malformed ``hello`` frame.
        """
        with self._lock:
            if self._closed.is_set():
                raise GatewayClosedError(None, "gateway is closed")
            if self._ws is not None:
                return self

            self._connect_locked()

        return self

    def _connect_locked(self) -> None:
        token = self._resolve_token()
        if not token:
            raise GatewayAuthError("gateway identify requires an access token")

        kwargs: dict[str, Any] = {
            "open_timeout": self.connect_timeout,
            "close_timeout": self.close_timeout,
            "ping_interval": None,
            "proxy": self.proxy,
            "legacy": True,
        }
        if self.max_message_size is not None:
            kwargs["max_size"] = self.max_message_size
        if self.url.startswith("wss://") and self._ssl is not None:
            kwargs["ssl"] = self._ssl

        try:
            ws = ws_connect(self.url, **kwargs)
        except InvalidStatus as exc:
            raise GatewayHandshakeError(exc.response.status_code) from exc
        except (InvalidURI, InvalidHandshake, OSError, TimeoutError) as exc:
            raise GatewayConnectionError(f"gateway connection failed: {exc}") from exc

        connected_at = time.monotonic()
        try:
            ws.send(identify_message(token))
            hello = self._await_hello(ws, connected_at)
        except GatewayProtocolError:
            self._discard(ws)
            raise
        except TimeoutError as exc:
            self._discard(ws)
            raise GatewayConnectionError("timed out waiting for the gateway 'hello' frame") from exc
        except ConnectionClosed as exc:
            self._discard(ws)
            code, reason = close_details(exc)
            if code in (None, 1000, 1005):
                raise GatewayAuthError("the server closed the gateway before 'hello'") from exc
            raise GatewayConnectionError(
                f"the server closed the gateway before 'hello' (code {code}, reason {reason!r})"
            ) from exc

        self._ws = ws
        self._heartbeat_interval_ms = hello.heartbeat_interval_ms
        self._start_heartbeat(ws, connected_at, hello.heartbeat_interval_ms)

    def _await_hello(self, ws: Any, connected_at: float) -> HelloFrame:
        deadline = None if self.auth_timeout is None else connected_at + self.auth_timeout

        while True:
            if deadline is None:
                raw = ws.recv()
            else:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError
                raw = ws.recv(timeout=remaining)

            if isinstance(raw, bytes):
                raise GatewayProtocolError("the gateway sent a binary frame")
            frame = parse_frame(raw)
            if isinstance(frame, HelloFrame):
                return frame
            if frame is None:
                continue
            raise GatewayProtocolError("the gateway sent a dispatch before 'hello'")

    def _resolve_token(self) -> str | None:
        if self._token_provider is not None:
            return self._token_provider()
        return self._token

    # ------------------------------------------------------------- heartbeat

    def _start_heartbeat(self, ws: Any, connected_at: float, interval_ms: int) -> None:
        stop = threading.Event()
        thread = threading.Thread(
            target=self._heartbeat_loop,
            args=(ws, connected_at, interval_ms / 1000.0, stop),
            name="distrans-gateway-heartbeat",
            daemon=True,
        )
        self._heartbeat_stop = stop
        self._heartbeat = thread
        thread.start()

    def _heartbeat_loop(self, ws: Any, connected_at: float, interval: float, stop: threading.Event) -> None:
        next_ack = connected_at + interval

        while not stop.is_set():
            now = time.monotonic()
            wait = next_ack - now
            if wait > 0:
                if stop.wait(wait):
                    return
                continue

            try:
                ws.send(ack_message())
            except Exception:
                return

            next_ack += interval
            now = time.monotonic()
            if next_ack <= now:
                next_ack = now + interval

    def _stop_heartbeat_thread(self) -> None:
        stop = self._heartbeat_stop
        self._heartbeat_stop = None
        if stop is not None:
            stop.set()

        thread = self._heartbeat
        self._heartbeat = None
        if thread is not None and thread is not threading.current_thread():
            thread.join(timeout=5.0)

    # ----------------------------------------------------------------- recv

    def recv(self, timeout: float | None = None) -> DispatchEvent | UnknownDispatchEvent:
        """Return the next dispatch event.

        ``hello`` and unknown frames are skipped. Raises the built-in
        ``TimeoutError`` when no event arrives within ``timeout`` seconds and
        :class:`GatewayClosedError` when the connection ends and reconnection is
        disabled. Calling :meth:`close` from another thread ends the wait.
        """
        deadline = None if timeout is None else time.monotonic() + timeout

        while True:
            if self._closed.is_set() and self._ws is None:
                raise GatewayClosedError(None, "gateway is closed")

            self.connect()
            ws = self._ws
            assert ws is not None

            try:
                frame = self._read_frame(ws, deadline)
            except TimeoutError:
                raise
            except ConnectionClosed as exc:
                self._lose_transport(ws)
                if not self.auto_reconnect or self._closed.is_set():
                    raise GatewayClosedError(*close_details(exc)) from exc
                self._reconnect(deadline)
                continue
            except (GatewayProtocolError, GatewayAuthError):
                self._lose_transport(ws)
                raise
            except (OSError, ConnectionError) as exc:
                self._lose_transport(ws)
                if not self.auto_reconnect or self._closed.is_set():
                    raise GatewayConnectionError(f"gateway connection lost: {exc}") from exc
                self._reconnect(deadline)
                continue

            if isinstance(frame, HelloFrame):
                continue

            return frame

    def _read_frame(self, ws: Any, deadline: float | None) -> Any:
        while True:
            if self._closed.is_set():
                raise GatewayClosedError(None, "gateway is closed")

            if deadline is None:
                try:
                    raw = ws.recv(timeout=_POLL_SLICE)
                except TimeoutError:
                    continue
            else:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError
                try:
                    raw = ws.recv(timeout=min(remaining, _POLL_SLICE))
                except TimeoutError:
                    continue

            if isinstance(raw, bytes):
                raise GatewayProtocolError("the gateway sent a binary frame")

            frame = parse_frame(raw)
            if frame is None:
                continue

            return frame

    def _reconnect(self, deadline: float | None) -> None:
        delay = 0.0
        immediate = True

        while not self._closed.is_set():
            if not immediate:
                delay = min(max(delay * 2, 1.0), 30.0)
                jittered = random.uniform(delay / 2, delay)
                if not self._wait_or_closed(jittered, deadline):
                    raise TimeoutError
            immediate = False

            try:
                self.connect()
            except GatewayAuthError:
                raise
            except GatewayHandshakeError as exc:
                if 400 <= exc.status_code < 500:
                    raise
            except GatewayConnectionError:
                continue
            else:
                if self._on_reconnect is not None:
                    self._on_reconnect(self)
                return

        raise GatewayClosedError(None, "gateway is closed")

    def _wait_or_closed(self, delay: float, deadline: float | None) -> bool:
        if deadline is not None:
            delay = min(delay, max(0.0, deadline - time.monotonic()))

        return not self._closed.wait(delay)

    # ---------------------------------------------------------------- close

    def close(self, code: int = 1000, reason: str = "") -> None:
        """Close the connection. Idempotent."""
        self._closed.set()

        with self._lock:
            ws = self._ws
            self._ws = None

        self._stop_heartbeat_thread()

        if ws is not None:
            try:
                ws.close(code, reason)
            except Exception:
                pass

    def _lose_transport(self, ws: Any) -> None:
        with self._lock:
            if self._ws is ws:
                self._ws = None

        self._stop_heartbeat_thread()
        self._discard(ws)

    @staticmethod
    def _discard(ws: Any) -> None:
        try:
            ws.close()
        except Exception:
            pass

    def __enter__(self) -> Gateway:
        return self.connect()

    def __exit__(self, *args: object) -> None:
        self.close()

    def __iter__(self) -> Iterator[DispatchEvent | UnknownDispatchEvent]:
        return self

    def __next__(self) -> DispatchEvent | UnknownDispatchEvent:
        if self._closed.is_set() and self._ws is None:
            raise StopIteration

        return self.recv()
