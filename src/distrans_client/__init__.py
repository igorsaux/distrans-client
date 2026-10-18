"""Low-level Python client for the Distrans API.

The generated modules (``api``, ``models``, ``client``, ``errors``, ``types``) are
produced by ``scripts/generate.py`` from ``openapi/openapi.yml`` and must not be
edited by hand. Hand-written code lives in ``facade``, ``async_facade``,
``exceptions``, ``gateway``, ``helpers`` and ``retry``.
"""

from __future__ import annotations

from . import api, models, types
from .async_facade import AsyncDistransClient
from .client import AuthenticatedClient, Client
from .errors import UnexpectedStatus
from .exceptions import (
    DistransAPIError,
    DistransDownloadError,
    DistransError,
    DistransGatewayError,
    GatewayAuthError,
    GatewayClosedError,
    GatewayConnectionError,
    GatewayHandshakeError,
    GatewayProtocolError,
)
from .facade import DistransClient
from .gateway import (
    AsyncGateway,
    ChannelEvent,
    ChannelsReorderedEvent,
    DispatchEvent,
    EmojiEvent,
    Gateway,
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
from .helpers import emoji_token, no_mentions
from .retry import RetryPolicy
from .types import UNSET, File

__all__ = [
    "UNSET",
    "AsyncDistransClient",
    "AsyncGateway",
    "AuthenticatedClient",
    "ChannelEvent",
    "ChannelsReorderedEvent",
    "Client",
    "DispatchEvent",
    "DistransAPIError",
    "DistransClient",
    "DistransDownloadError",
    "DistransError",
    "DistransGatewayError",
    "EmojiEvent",
    "File",
    "Gateway",
    "GatewayAuthError",
    "GatewayClosedError",
    "GatewayConnectionError",
    "GatewayEventType",
    "GatewayHandshakeError",
    "GatewayProtocolError",
    "GuildEvent",
    "MessageEvent",
    "MessageReactionEvent",
    "OverwriteEvent",
    "RetryPolicy",
    "RoleAssignmentEvent",
    "RoleEvent",
    "RolesReorderedEvent",
    "UnexpectedStatus",
    "UnknownDispatchEvent",
    "UserEvent",
    "WebhookEvent",
    "api",
    "emoji_token",
    "models",
    "no_mentions",
    "types",
]
