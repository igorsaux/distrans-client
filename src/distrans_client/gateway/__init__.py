"""WebSocket gateway support for Distrans.

The gateway is a JSON frame protocol on top of a WebSocket upgrade. Use
:class:`Gateway` for synchronous code and :class:`AsyncGateway` for asyncio, or
obtain one from :meth:`distrans_client.DistransClient.gateway` and
:meth:`distrans_client.AsyncDistransClient.gateway`.
"""

from __future__ import annotations

from ..exceptions import (
    DistransGatewayError,
    GatewayAuthError,
    GatewayClosedError,
    GatewayConnectionError,
    GatewayHandshakeError,
    GatewayProtocolError,
)
from .aio import AsyncGateway
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
from .protocol import HelloFrame, ack_message, build_ssl_context, gateway_url, identify_message, parse_frame
from .sync import Gateway

__all__ = [
    "AsyncGateway",
    "ChannelEvent",
    "ChannelsReorderedEvent",
    "DispatchEvent",
    "DistransGatewayError",
    "EmojiEvent",
    "Gateway",
    "GatewayAuthError",
    "GatewayClosedError",
    "GatewayConnectionError",
    "GatewayEventType",
    "GatewayHandshakeError",
    "GatewayProtocolError",
    "GuildEvent",
    "HelloFrame",
    "MessageEvent",
    "MessageReactionEvent",
    "OverwriteEvent",
    "RoleAssignmentEvent",
    "RoleEvent",
    "RolesReorderedEvent",
    "UnknownDispatchEvent",
    "UserEvent",
    "WebhookEvent",
    "ack_message",
    "build_ssl_context",
    "gateway_url",
    "identify_message",
    "parse_frame",
]
