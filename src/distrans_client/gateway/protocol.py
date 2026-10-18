"""Gateway URL handling, frame encoding and frame parsing.

The server protocol is intentionally small:

* the client sends ``{"op": "identify", "d": {"token": "..."}}`` once;
* the server replies ``{"op": "hello", "d": {"heartbeat_interval": <ms>}}``;
* the client sends ``{"op": "ack"}`` roughly every ``heartbeat_interval`` ms;
* the server pushes ``{"op": "dispatch", "s": <seq>, "t": "...", "d": {...}}``.

Only text frames are used. Binary frames and fragmented messages are not part
of the protocol and are rejected by the parser.
"""

from __future__ import annotations

import json
import ssl
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlsplit

from ..exceptions import GatewayProtocolError
from .events import (
    ChannelEvent,
    ChannelsReorderedEvent,
    DispatchEvent,
    EmojiEvent,
    GatewayEventType,
    GuildEvent,
    MessageEvent,
    MessageReactionEvent,
    OverwriteEvent,
    RoleAssignmentEvent,
    RoleEvent,
    RolesReorderedEvent,
    UnknownDispatchEvent,
    UserEvent,
    WebhookEvent,
)

__all__ = [
    "HelloFrame",
    "GatewayFrame",
    "ack_message",
    "build_ssl_context",
    "gateway_url",
    "identify_message",
    "parse_frame",
]


@dataclass(frozen=True, slots=True)
class HelloFrame:
    """The server's reply to a successful ``identify``."""

    heartbeat_interval_ms: int


GatewayFrame = HelloFrame | DispatchEvent | UnknownDispatchEvent


def gateway_url(base_url: str) -> str:
    """Translate an HTTP API root into the gateway WebSocket URL.

    ``https://host/api`` becomes ``wss://host/api/gateway`` and
    ``http://host/api`` becomes ``ws://host/api/gateway``. Query strings and
    fragments are rejected because the gateway endpoint has no parameters.
    """
    parts = urlsplit(base_url)
    if parts.scheme not in ("http", "https"):
        raise ValueError(f"unsupported base URL scheme: {parts.scheme!r}")
    if not parts.netloc:
        raise ValueError("base URL must include a host")
    if parts.query or parts.fragment:
        raise ValueError("base URL must not contain a query or fragment")

    scheme = "wss" if parts.scheme == "https" else "ws"
    path = parts.path.rstrip("/")

    return f"{scheme}://{parts.netloc}{path}/gateway"


def identify_message(token: str) -> str:
    if not token:
        raise ValueError("an access token or bot token is required")

    return json.dumps({"op": "identify", "d": {"token": token}}, separators=(",", ":"))


def ack_message() -> str:
    return '{"op":"ack"}'


def build_ssl_context(verify: bool | str | ssl.SSLContext) -> ssl.SSLContext | None:
    """Map an httpx-style ``verify`` value onto a ``websockets`` SSL context."""
    if isinstance(verify, ssl.SSLContext):
        return verify
    if verify is True:
        return None
    if verify is False:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context
    return ssl.create_default_context(cafile=str(verify))


def parse_frame(raw: str | bytes) -> GatewayFrame | None:
    """Parse one text frame.

    Returns ``None`` for frames this client does not understand (unknown
    ``op``), so the caller can simply skip them. Raises
    :class:`~distrans_client.exceptions.GatewayProtocolError` for malformed
    JSON or a known frame with an invalid payload.
    """
    if isinstance(raw, bytes):
        try:
            raw = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise GatewayProtocolError("gateway frame is not valid UTF-8") from exc

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise GatewayProtocolError("gateway frame is not valid JSON") from exc

    if not isinstance(payload, dict):
        raise GatewayProtocolError("gateway frame must be a JSON object")

    op = payload.get("op")
    if not isinstance(op, str):
        raise GatewayProtocolError("gateway frame has no string 'op'")

    if op == "hello":
        return _parse_hello(payload)
    if op == "dispatch":
        return _parse_dispatch(payload)

    return None


def _parse_hello(payload: Mapping[str, Any]) -> HelloFrame:
    data = payload.get("d")
    if not isinstance(data, dict):
        raise GatewayProtocolError("'hello' frame has no object 'd'")

    interval = data.get("heartbeat_interval")
    if isinstance(interval, bool) or not isinstance(interval, int):
        raise GatewayProtocolError("'hello' frame has no integer 'heartbeat_interval'")
    if interval <= 0:
        raise GatewayProtocolError("'hello' heartbeat_interval must be positive")

    return HelloFrame(heartbeat_interval_ms=interval)


def _parse_dispatch(payload: Mapping[str, Any]) -> DispatchEvent | UnknownDispatchEvent:
    seq = payload.get("s")
    if isinstance(seq, bool) or not isinstance(seq, int):
        raise GatewayProtocolError("dispatch frame has no integer 's'")

    event_type = payload.get("t")
    if not isinstance(event_type, str):
        raise GatewayProtocolError("dispatch frame has no string 't'")

    data = payload.get("d")
    if not isinstance(data, dict):
        raise GatewayProtocolError("dispatch frame has no object 'd'")

    try:
        known = GatewayEventType(event_type)
    except ValueError:
        return UnknownDispatchEvent(seq=seq, event_type=event_type, data=dict(data))

    return _build_event(known, seq, data)


def _build_event(event_type: GatewayEventType, seq: int, data: Mapping[str, Any]) -> DispatchEvent:
    match event_type:
        case (
            GatewayEventType.MESSAGE_CREATED
            | GatewayEventType.MESSAGE_UPDATED
            | GatewayEventType.MESSAGE_DELETED
            | GatewayEventType.MESSAGE_PINNED
            | GatewayEventType.MESSAGE_UNPINNED
        ):
            return MessageEvent(
                seq=seq,
                type=event_type,
                id=_str(data, "id", event_type),
                channel_id=_str(data, "channel_id", event_type),
                guild_id=_str(data, "guild_id", event_type),
            )
        case GatewayEventType.REACTION_ADDED | GatewayEventType.REACTION_REMOVED:
            return MessageReactionEvent(
                seq=seq,
                type=event_type,
                id=_str(data, "id", event_type),
                channel_id=_str(data, "channel_id", event_type),
                guild_id=_str(data, "guild_id", event_type),
                user_id=_str(data, "user_id", event_type),
                emoji_id=_optional_str(data, "emoji_id", event_type),
                unicode_emoji=_optional_str(data, "unicode_emoji", event_type),
            )
        case GatewayEventType.OVERWRITE_UPDATED:
            return OverwriteEvent(
                seq=seq,
                type=event_type,
                guild_id=_str(data, "guild_id", event_type),
                channel_id=_str(data, "channel_id", event_type),
            )
        case GatewayEventType.USER_CREATED | GatewayEventType.USER_UPDATED | GatewayEventType.USER_DELETED:
            return UserEvent(seq=seq, type=event_type, id=_str(data, "id", event_type))
        case GatewayEventType.GUILD_CREATED | GatewayEventType.GUILD_UPDATED | GatewayEventType.GUILD_DELETED:
            return GuildEvent(seq=seq, type=event_type, id=_str(data, "id", event_type))
        case GatewayEventType.CHANNEL_CREATED | GatewayEventType.CHANNEL_UPDATED | GatewayEventType.CHANNEL_DELETED:
            return ChannelEvent(
                seq=seq,
                type=event_type,
                id=_str(data, "id", event_type),
                guild_id=_str(data, "guild_id", event_type),
            )
        case GatewayEventType.CHANNELS_REORDERED:
            return ChannelsReorderedEvent(
                seq=seq,
                type=event_type,
                guild_id=_str(data, "guild_id", event_type),
            )
        case GatewayEventType.ROLE_CREATED | GatewayEventType.ROLE_UPDATED | GatewayEventType.ROLE_DELETED:
            return RoleEvent(
                seq=seq,
                type=event_type,
                id=_str(data, "id", event_type),
                guild_id=_str(data, "guild_id", event_type),
            )
        case GatewayEventType.ROLE_GRANTED | GatewayEventType.ROLE_REVOKED:
            return RoleAssignmentEvent(
                seq=seq,
                type=event_type,
                id=_str(data, "id", event_type),
                guild_id=_str(data, "guild_id", event_type),
                user_id=_str(data, "user_id", event_type),
            )
        case GatewayEventType.ROLES_REORDERED:
            return RolesReorderedEvent(
                seq=seq,
                type=event_type,
                guild_id=_str(data, "guild_id", event_type),
            )
        case GatewayEventType.EMOJI_CREATED | GatewayEventType.EMOJI_UPDATED | GatewayEventType.EMOJI_DELETED:
            return EmojiEvent(
                seq=seq,
                type=event_type,
                id=_str(data, "id", event_type),
                guild_id=_str(data, "guild_id", event_type),
            )
        case GatewayEventType.WEBHOOK_CREATED | GatewayEventType.WEBHOOK_UPDATED | GatewayEventType.WEBHOOK_DELETED:
            return WebhookEvent(
                seq=seq,
                type=event_type,
                id=_str(data, "id", event_type),
                guild_id=_str(data, "guild_id", event_type),
                channel_id=_str(data, "channel_id", event_type),
            )

    raise AssertionError(f"unhandled event type: {event_type}")


def _str(data: Mapping[str, Any], key: str, event_type: GatewayEventType) -> str:
    value = data.get(key)
    if not isinstance(value, str):
        raise GatewayProtocolError(f"{event_type} event has no string {key!r}")
    return value


def _optional_str(data: Mapping[str, Any], key: str, event_type: GatewayEventType) -> str | None:
    value = data.get(key)
    if value is None or isinstance(value, str):
        return value
    raise GatewayProtocolError(f"{event_type} event field {key!r} must be a string or null")
