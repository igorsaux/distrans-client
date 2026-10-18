from __future__ import annotations

import json
import threading
import time

import pytest

from distrans_client.exceptions import (
    GatewayAuthError,
    GatewayClosedError,
    GatewayConnectionError,
)
from distrans_client.gateway import Gateway, GatewayEventType, MessageEvent, UserEvent
from tests.gateway_helpers import SyncGatewayServer, dispatch


def make_gateway(server: SyncGatewayServer, token: str | None = "good", **kwargs: object) -> Gateway:
    return Gateway(server.url, token, proxy=None, **kwargs)


def test_identify_hello_and_path() -> None:
    with SyncGatewayServer(interval_ms=5_000) as server:
        with make_gateway(server) as gateway:
            assert gateway.connected
            assert gateway.heartbeat_interval_ms == 5_000

            assert server.paths == ["/api/gateway"]
            assert server.identifies == [{"op": "identify", "d": {"token": "good"}}]


def test_dispatch_event_is_parsed() -> None:
    event = dispatch("message_created", 1, {"id": "1", "channel_id": "2", "guild_id": "3"})

    with SyncGatewayServer(interval_ms=5_000, events=[event]) as server:
        with make_gateway(server) as gateway:
            received = gateway.recv(timeout=5)

    assert isinstance(received, MessageEvent)
    assert received.type is GatewayEventType.MESSAGE_CREATED
    assert received.seq == 1
    assert (received.message_id, received.channel_id, received.guild_id) == ("1", "2", "3")


def test_heartbeat_is_sent_at_the_announced_interval() -> None:
    with SyncGatewayServer(interval_ms=150) as server:
        with make_gateway(server) as gateway:
            deadline = time.monotonic() + 5
            while len(server.acks) < 2 and time.monotonic() < deadline:
                time.sleep(0.02)

            assert gateway.heartbeat_interval_ms == 150

    assert len(server.acks) >= 2
    assert all(message == {"op": "ack"} for _, message in server.acks)
    assert 0.1 <= server.acks[0][0] - server.hello_at[0] <= 1.5


def test_heartbeat_first_ack_is_not_early() -> None:
    with SyncGatewayServer(interval_ms=250) as server:
        started = time.monotonic()
        with make_gateway(server) as gateway:
            deadline = time.monotonic() + 5
            while not server.acks and time.monotonic() < deadline:
                time.sleep(0.01)
        elapsed = time.monotonic() - started

        assert gateway.heartbeat_interval_ms == 250

    assert server.acks, "the gateway never acknowledged"
    # The ack must not be sent immediately after the handshake.
    assert elapsed >= 0.2


def test_recv_timeout() -> None:
    with SyncGatewayServer(interval_ms=5_000) as server:
        with make_gateway(server) as gateway:
            started = time.monotonic()
            with pytest.raises(TimeoutError):
                gateway.recv(timeout=0.2)

    assert time.monotonic() - started >= 0.15


def test_auth_failure_raises_auth_error() -> None:
    with SyncGatewayServer() as server:
        gateway = make_gateway(server, token="bad")

        with pytest.raises(GatewayAuthError):
            gateway.connect()


def test_missing_token_raises_auth_error() -> None:
    gateway = Gateway("ws://127.0.0.1:1/api/gateway", None, proxy=None)

    with pytest.raises(GatewayAuthError):
        gateway.connect()


def test_unreachable_server_raises_connection_error() -> None:
    gateway = Gateway("ws://127.0.0.1:1/api/gateway", "good", proxy=None, connect_timeout=1)

    with pytest.raises(GatewayConnectionError):
        gateway.connect()


def test_unexpected_close_raises_closed_error() -> None:
    with SyncGatewayServer(close_after_hello=True) as server:
        with make_gateway(server, auth_timeout=5) as gateway:
            with pytest.raises(GatewayClosedError) as raised:
                gateway.recv(timeout=5)

    assert raised.value.code == 1000


def test_close_stops_iteration() -> None:
    with SyncGatewayServer(interval_ms=5_000) as server:
        gateway = make_gateway(server)
        gateway.connect()
        gateway.connect()
        gateway.close()
        gateway.close()

        assert gateway.closed
        assert not gateway.connected
        with pytest.raises(StopIteration):
            next(gateway)


def test_close_from_another_thread_unblocks_recv() -> None:
    with SyncGatewayServer(interval_ms=5_000) as server:
        with make_gateway(server) as gateway:
            errors: list[BaseException] = []

            def consume() -> None:
                try:
                    gateway.recv()
                except BaseException as exc:  # noqa: BLE001 - asserted below
                    errors.append(exc)

            thread = threading.Thread(target=consume)
            thread.start()
            time.sleep(0.1)
            gateway.close()
            thread.join(timeout=5)

    assert not thread.is_alive()
    assert errors and isinstance(errors[0], GatewayClosedError)


def test_reconnect_and_token_provider() -> None:
    from websockets.sync.server import ServerConnection

    tokens: list[str | None] = []

    def handler(connection: ServerConnection, index: int) -> None:
        raw = connection.recv(timeout=5)
        message = json.loads(raw)
        tokens.append((message.get("d") or {}).get("token"))

        connection.send(json.dumps({"op": "hello", "d": {"heartbeat_interval": 5_000}}))

        if index == 0:
            connection.close(1000, "restart")
            return

        connection.send(json.dumps(dispatch("user_created", 1, {"id": "10"})))
        try:
            connection.recv(timeout=5)
        except Exception:
            return

    reconnects: list[Gateway] = []

    with SyncGatewayServer(handler=handler) as server:
        gateway = Gateway(
            server.url,
            token_provider=lambda: "token-1" if not tokens else "token-2",
            auto_reconnect=True,
            on_reconnect=reconnects.append,
            proxy=None,
        )

        event = gateway.recv(timeout=5)
        gateway.close()

    assert event.type is GatewayEventType.USER_CREATED
    assert isinstance(event, UserEvent)
    assert event.id == "10"
    assert tokens == ["token-1", "token-2"]
    assert reconnects == [gateway]
