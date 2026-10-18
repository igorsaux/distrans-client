"""Local WebSocket servers used by the gateway tests."""

from __future__ import annotations

import json
import threading
import time
from collections.abc import Callable, Sequence
from typing import Any

from websockets.sync.server import Server, ServerConnection, serve

GATEWAY_PATH = "/api/gateway"

SyncHandler = Callable[[ServerConnection, int], None]


class SyncGatewayServer:
    """A scripted gateway served on ``127.0.0.1`` with an ephemeral port."""

    def __init__(
        self,
        *,
        interval_ms: int = 200,
        accept_token: str | None = "good",
        events: Sequence[dict[str, Any]] = (),
        close_after_hello: bool = False,
        handler: SyncHandler | None = None,
    ) -> None:
        self.interval_ms = interval_ms
        self.accept_token = accept_token
        self.events = list(events)
        self.close_after_hello = close_after_hello
        self.paths: list[str] = []
        self.identifies: list[dict[str, Any]] = []
        self.acks: list[tuple[float, dict[str, Any]]] = []
        self.hello_at: list[float] = []
        self.connections = 0
        self._handler = handler

        self._server: Server = serve(
            self._serve,
            "127.0.0.1",
            0,
            ping_interval=None,
            compression=None,
        )
        self._thread: threading.Thread | None = None

    @property
    def port(self) -> int:
        return self._server.socket.getsockname()[1]

    @property
    def url(self) -> str:
        return f"ws://127.0.0.1:{self.port}{GATEWAY_PATH}"

    def _serve(self, connection: ServerConnection) -> None:
        index = self.connections
        self.connections += 1
        self.paths.append(connection.request.path)

        if self._handler is not None:
            self._handler(connection, index)
        else:
            self._default_handler(connection)

    def _default_handler(self, connection: ServerConnection) -> None:
        try:
            raw = connection.recv(timeout=5)
        except TimeoutError:
            return

        message = json.loads(raw)
        self.identifies.append(message)

        token = (message.get("d") or {}).get("token")
        if self.accept_token is not None and token != self.accept_token:
            connection.close(1000, "invalid token")
            return

        connection.send(json.dumps({"op": "hello", "d": {"heartbeat_interval": self.interval_ms}}))
        self.hello_at.append(time.monotonic())

        if self.close_after_hello:
            connection.close(1000, "bye")
            return

        for event in self.events:
            connection.send(json.dumps(event))

        while True:
            try:
                raw = connection.recv(timeout=5)
            except TimeoutError:
                return
            except Exception:
                return

            self.acks.append((time.monotonic(), json.loads(raw)))

    def __enter__(self) -> SyncGatewayServer:
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, *args: object) -> None:
        self._server.shutdown()
        if self._thread is not None:
            self._thread.join(timeout=5)


def dispatch(event_type: str, seq: int, data: dict[str, Any]) -> dict[str, Any]:
    return {"op": "dispatch", "s": seq, "t": event_type, "d": data}
