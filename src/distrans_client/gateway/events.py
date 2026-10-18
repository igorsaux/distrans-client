"""Typed gateway dispatch events.

Every dispatch frame sent by the server has the shape::

    {"op": "dispatch", "s": <seq>, "t": "<event type>", "d": {...}}

The classes in this module mirror the payload of ``d``. They are frozen
dataclasses, so a received event can be compared, stored and shared freely.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

__all__ = [
    "ChannelEvent",
    "ChannelsReorderedEvent",
    "DispatchEvent",
    "EmojiEvent",
    "GatewayEventType",
    "GuildEvent",
    "MessageEvent",
    "MessageReactionEvent",
    "OverwriteEvent",
    "RoleAssignmentEvent",
    "RoleEvent",
    "RolesReorderedEvent",
    "UnknownDispatchEvent",
    "UserEvent",
    "WebhookEvent",
]


class GatewayEventType(StrEnum):
    """Values of the ``t`` field of a dispatch frame."""

    MESSAGE_CREATED = "message_created"
    MESSAGE_UPDATED = "message_updated"
    MESSAGE_DELETED = "message_deleted"
    MESSAGE_PINNED = "message_pinned"
    MESSAGE_UNPINNED = "message_unpinned"
    OVERWRITE_UPDATED = "overwrite_updated"
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"
    GUILD_CREATED = "guild_created"
    GUILD_UPDATED = "guild_updated"
    GUILD_DELETED = "guild_deleted"
    CHANNEL_CREATED = "channel_created"
    CHANNEL_UPDATED = "channel_updated"
    CHANNEL_DELETED = "channel_deleted"
    CHANNELS_REORDERED = "channels_reordered"
    ROLE_CREATED = "role_created"
    ROLE_UPDATED = "role_updated"
    ROLE_DELETED = "role_deleted"
    ROLE_GRANTED = "role_granted"
    ROLE_REVOKED = "role_revoked"
    ROLES_REORDERED = "roles_reordered"
    EMOJI_CREATED = "emoji_created"
    EMOJI_UPDATED = "emoji_updated"
    EMOJI_DELETED = "emoji_deleted"
    REACTION_ADDED = "reaction_added"
    REACTION_REMOVED = "reaction_removed"
    WEBHOOK_CREATED = "webhook_created"
    WEBHOOK_UPDATED = "webhook_updated"
    WEBHOOK_DELETED = "webhook_deleted"


@dataclass(frozen=True, slots=True)
class DispatchEvent:
    """Base class for parsed dispatch frames.

    Attributes:
        seq: The per-connection sequence number from the ``s`` field. It starts
            at 1 and only grows; gaps mean events were lost.
        type: The event type from the ``t`` field.
    """

    seq: int
    type: GatewayEventType


@dataclass(frozen=True, slots=True)
class MessageEvent(DispatchEvent):
    """``message_created``, ``message_updated``, ``message_deleted``,
    ``message_pinned`` and ``message_unpinned``."""

    id: str
    channel_id: str
    guild_id: str

    @property
    def message_id(self) -> str:
        """Alias of :attr:`id`, which is the affected message id."""
        return self.id


@dataclass(frozen=True, slots=True)
class MessageReactionEvent(DispatchEvent):
    """``reaction_added`` and ``reaction_removed``."""

    id: str
    channel_id: str
    guild_id: str
    user_id: str
    emoji_id: str | None
    unicode_emoji: str | None

    @property
    def message_id(self) -> str:
        """Alias of :attr:`id`, which is the affected message id."""
        return self.id


@dataclass(frozen=True, slots=True)
class OverwriteEvent(DispatchEvent):
    """``overwrite_updated``."""

    guild_id: str
    channel_id: str


@dataclass(frozen=True, slots=True)
class UserEvent(DispatchEvent):
    """``user_created``, ``user_updated`` and ``user_deleted``."""

    id: str

    @property
    def user_id(self) -> str:
        """Alias of :attr:`id`, which is the affected user id."""
        return self.id


@dataclass(frozen=True, slots=True)
class GuildEvent(DispatchEvent):
    """``guild_created``, ``guild_updated`` and ``guild_deleted``."""

    id: str

    @property
    def guild_id(self) -> str:
        """Alias of :attr:`id`, which is the affected guild id."""
        return self.id


@dataclass(frozen=True, slots=True)
class ChannelEvent(DispatchEvent):
    """``channel_created``, ``channel_updated`` and ``channel_deleted``."""

    id: str
    guild_id: str

    @property
    def channel_id(self) -> str:
        """Alias of :attr:`id`, which is the affected channel id."""
        return self.id


@dataclass(frozen=True, slots=True)
class ChannelsReorderedEvent(DispatchEvent):
    """``channels_reordered``; refetch the guild's channel list."""

    guild_id: str


@dataclass(frozen=True, slots=True)
class RoleEvent(DispatchEvent):
    """``role_created``, ``role_updated`` and ``role_deleted``."""

    id: str
    guild_id: str

    @property
    def role_id(self) -> str:
        """Alias of :attr:`id`, which is the affected role id."""
        return self.id


@dataclass(frozen=True, slots=True)
class RoleAssignmentEvent(DispatchEvent):
    """``role_granted`` and ``role_revoked`` for one user."""

    id: str
    guild_id: str
    user_id: str

    @property
    def role_id(self) -> str:
        """Alias of :attr:`id`, which is the affected role id."""
        return self.id


@dataclass(frozen=True, slots=True)
class RolesReorderedEvent(DispatchEvent):
    """``roles_reordered``; refetch the guild's role list."""

    guild_id: str


@dataclass(frozen=True, slots=True)
class EmojiEvent(DispatchEvent):
    """``emoji_created``, ``emoji_updated`` and ``emoji_deleted``."""

    id: str
    guild_id: str

    @property
    def emoji_id(self) -> str:
        """Alias of :attr:`id`, which is the affected emoji id."""
        return self.id


@dataclass(frozen=True, slots=True)
class WebhookEvent(DispatchEvent):
    """``webhook_created``, ``webhook_updated`` and ``webhook_deleted``."""

    id: str
    guild_id: str
    channel_id: str

    @property
    def webhook_id(self) -> str:
        """Alias of :attr:`id`, which is the affected webhook id."""
        return self.id


@dataclass(frozen=True, slots=True)
class UnknownDispatchEvent:
    """A dispatch frame whose ``t`` is not known to this client version.

    Forward compatibility: the payload is kept as-is so callers can inspect it
    instead of losing the event. A newer server may add event types.
    """

    seq: int
    event_type: str
    data: Mapping[str, Any]
