from __future__ import annotations

import asyncio
import json
import time
from collections.abc import Awaitable, Callable
from typing import Any

import pytest
from websockets.asyncio.server import Server, ServerConnection, serve

from distrans_client.exceptions import GatewayAuthError, GatewayClosedError
from distrans_client.gateway import AsyncGateway, GatewayEventType, UserEvent
from tests.gateway_helpers import dispatch

GATEWAY_PATH = "/api/gateway"

AsyncHandler = Callable[[ServerConnection, int], Awaitable[None]]


class AsyncGatewayServer:
    def __init__(self, *, interval_ms: int = 200, handler: AsyncHandler | None = None) -> None:
        self.interval_ms = interval_ms
        self.paths: list[str] = []
        self.identifies: list[dict[str, Any]] = []
        self.acks: list[tuple[float, dict[str, Any]]] = []
        self.hello_at: list[float] = []
        self.connections = 0
        self._handler = handler
        self._server: Server | None = None

    @property
    def url(self) -> str:
        assert self._server is not None
        port = self._server.sockets[0].getsockname()[1]
        return f"ws://127.0.0.1:{port}{GATEWAY_PATH}"

    async def start(self) -> AsyncGatewayServer:
        self._server = await serve(self._serve, "127.0.0.1", 0, ping_interval=None, compression=None)
        return self

    async def stop(self) -> None:
        assert self._server is not None
        self._server.close()
        await self._server.wait_closed()

    async def _serve(self, connection: ServerConnection) -> None:
        index = self.connections
        self.connections += 1
        self.paths.append(connection.request.path)

        if self._handler is not None:
            await self._handler(connection, index)
        else:
            await self._default_handler(connection)

    async def _default_handler(self, connection: ServerConnection) -> None:
        message = json.loads(await asyncio.wait_for(connection.recv(), timeout=5))
        self.identifies.append(message)

        token = (message.get("d") or {}).get("token")
        if token != "good":
            await connection.close(1000, "invalid token")
            return

        await connection.send(json.dumps({"op": "hello", "d": {"heartbeat_interval": self.interval_ms}}))
        self.hello_at.append(time.monotonic())

        while True:
            try:
                raw = await asyncio.wait_for(connection.recv(), timeout=5)
            except Exception:
                return

            self.acks.append((time.monotonic(), json.loads(raw)))


def make_gateway(server: AsyncGatewayServer, token: str | None = "good", **kwargs: object) -> AsyncGateway:
    return AsyncGateway(server.url, token, proxy=None, **kwargs)


async def test_async_identify_hello_and_path() -> None:
    server = await AsyncGatewayServer(interval_ms=5_000).start()
    try:
        async with make_gateway(server) as gateway:
            assert gateway.connected
            assert gateway.heartbeat_interval_ms == 5_000
            assert server.paths == [GATEWAY_PATH]
            assert server.identifies == [{"op": "identify", "d": {"token": "good"}}]
    finally:
        await server.stop()


async def test_async_dispatch_event() -> None:
    async def handler(connection: ServerConnection, index: int) -> None:
        json.loads(await connection.recv())
        await connection.send(json.dumps({"op": "hello", "d": {"heartbeat_interval": 5_000}}))
        await connection.send(json.dumps(dispatch("user_created", 3, {"id": "10"})))
        try:
            await asyncio.wait_for(connection.recv(), timeout=5)
        except Exception:
            return

    server = await AsyncGatewayServer(handler=handler).start()
    try:
        async with make_gateway(server) as gateway:
            event = await gateway.recv(timeout=5)
    finally:
        await server.stop()

    assert isinstance(event, UserEvent)
    assert event.type is GatewayEventType.USER_CREATED
    assert event.seq == 3
    assert event.id == "10"


async def test_async_heartbeat() -> None:
    server = await AsyncGatewayServer(interval_ms=150).start()
    try:
        async with make_gateway(server) as gateway:
            deadline = time.monotonic() + 5
            while len(server.acks) < 2 and time.monotonic() < deadline:
                await asyncio.sleep(0.02)

            assert gateway.heartbeat_interval_ms == 150
    finally:
        await server.stop()

    assert len(server.acks) >= 2
    assert all(message == {"op": "ack"} for _, message in server.acks)
    assert 0.1 <= server.acks[0][0] - server.hello_at[0] <= 1.5


async def test_async_recv_timeout() -> None:
    server = await AsyncGatewayServer(interval_ms=5_000).start()
    try:
        async with make_gateway(server) as gateway:
            started = time.monotonic()
            with pytest.raises(TimeoutError):
                await gateway.recv(timeout=0.2)
            assert time.monotonic() - started >= 0.15
    finally:
        await server.stop()


async def test_async_auth_failure() -> None:
    server = await AsyncGatewayServer().start()
    try:
        gateway = make_gateway(server, token="bad")
        with pytest.raises(GatewayAuthError):
            await gateway.connect()
    finally:
        await server.stop()


async def test_async_closed_error() -> None:
    async def handler(connection: ServerConnection, index: int) -> None:
        json.loads(await connection.recv())
        await connection.send(json.dumps({"op": "hello", "d": {"heartbeat_interval": 5_000}}))
        await connection.close(1000, "bye")

    server = await AsyncGatewayServer(handler=handler).start()
    try:
        async with make_gateway(server) as gateway:
            with pytest.raises(GatewayClosedError) as raised:
                await gateway.recv(timeout=5)
    finally:
        await server.stop()

    assert raised.value.code == 1000
    assert raised.value.reason == "bye"


async def test_async_close_stops_iteration() -> None:
    server = await AsyncGatewayServer(interval_ms=5_000).start()
    try:
        gateway = make_gateway(server)
        await gateway.connect()
        await gateway.connect()
        await gateway.close()
        await gateway.close()

        assert gateway.closed
        assert not gateway.connected
        with pytest.raises(StopAsyncIteration):
            await gateway.__anext__()
    finally:
        await server.stop()


async def test_async_close_unblocks_recv() -> None:
    server = await AsyncGatewayServer(interval_ms=5_000).start()
    try:
        gateway = make_gateway(server)
        await gateway.connect()

        async def consume() -> None:
            with pytest.raises(GatewayClosedError):
                await gateway.recv()

        task = asyncio.create_task(consume())
        await asyncio.sleep(0.1)
        await gateway.close()
        await asyncio.wait_for(task, timeout=5)
    finally:
        await server.stop()


async def test_async_reconnect_with_callbacks() -> None:
    tokens: list[str | None] = []

    async def handler(connection: ServerConnection, index: int) -> None:
        message = json.loads(await connection.recv())
        tokens.append((message.get("d") or {}).get("token"))
        await connection.send(json.dumps({"op": "hello", "d": {"heartbeat_interval": 5_000}}))

        if index == 0:
            await connection.close(1000, "restart")
            return

        await connection.send(json.dumps(dispatch("user_created", 1, {"id": "10"})))
        try:
            await asyncio.wait_for(connection.recv(), timeout=5)
        except Exception:
            return

    async def token_provider() -> str:
        return "token-1" if not tokens else "token-2"

    reconnects: list[AsyncGateway] = []

    async def on_reconnect(gateway: AsyncGateway) -> None:
        reconnects.append(gateway)

    server = await AsyncGatewayServer(handler=handler).start()
    try:
        gateway = AsyncGateway(
            server.url,
            token_provider=token_provider,
            auto_reconnect=True,
            on_reconnect=on_reconnect,
            proxy=None,
        )
        event = await gateway.recv(timeout=5)
        await gateway.close()
    finally:
        await server.stop()

    assert isinstance(event, UserEvent)
    assert event.id == "10"
    assert tokens == ["token-1", "token-2"]
    assert reconnects == [gateway]
