from __future__ import annotations

import json
import ssl

import pytest

from distrans_client.exceptions import GatewayProtocolError
from distrans_client.gateway import (
    ChannelEvent,
    ChannelsReorderedEvent,
    EmojiEvent,
    GatewayEventType,
    GuildEvent,
    HelloFrame,
    MessageEvent,
    MessageReactionEvent,
    OverwriteEvent,
    RoleAssignmentEvent,
    RoleEvent,
    RolesReorderedEvent,
    UnknownDispatchEvent,
    UserEvent,
    WebhookEvent,
    ack_message,
    build_ssl_context,
    gateway_url,
    identify_message,
    parse_frame,
)

EVENT_DATA: dict[str, dict[str, object]] = {
    "message_created": {"id": "1", "channel_id": "2", "guild_id": "3"},
    "message_updated": {"id": "1", "channel_id": "2", "guild_id": "3"},
    "message_deleted": {"id": "1", "channel_id": "2", "guild_id": "3"},
    "message_pinned": {"id": "1", "channel_id": "2", "guild_id": "3"},
    "message_unpinned": {"id": "1", "channel_id": "2", "guild_id": "3"},
    "overwrite_updated": {"guild_id": "3", "channel_id": "2"},
    "user_created": {"id": "1"},
    "user_updated": {"id": "1"},
    "user_deleted": {"id": "1"},
    "guild_created": {"id": "3"},
    "guild_updated": {"id": "3"},
    "guild_deleted": {"id": "3"},
    "channel_created": {"id": "2", "guild_id": "3"},
    "channel_updated": {"id": "2", "guild_id": "3"},
    "channel_deleted": {"id": "2", "guild_id": "3"},
    "channels_reordered": {"guild_id": "3"},
    "role_created": {"id": "4", "guild_id": "3"},
    "role_updated": {"id": "4", "guild_id": "3"},
    "role_deleted": {"id": "4", "guild_id": "3"},
    "role_granted": {"id": "4", "guild_id": "3", "user_id": "5"},
    "role_revoked": {"id": "4", "guild_id": "3", "user_id": "5"},
    "roles_reordered": {"guild_id": "3"},
    "emoji_created": {"id": "6", "guild_id": "3"},
    "emoji_updated": {"id": "6", "guild_id": "3"},
    "emoji_deleted": {"id": "6", "guild_id": "3"},
    "reaction_added": {
        "id": "1",
        "channel_id": "2",
        "guild_id": "3",
        "user_id": "5",
        "emoji_id": None,
        "unicode_emoji": "thumbsup",
    },
    "reaction_removed": {
        "id": "1",
        "channel_id": "2",
        "guild_id": "3",
        "user_id": "5",
        "emoji_id": "6",
        "unicode_emoji": None,
    },
    "webhook_created": {"id": "7", "guild_id": "3", "channel_id": "2"},
    "webhook_updated": {"id": "7", "guild_id": "3", "channel_id": "2"},
    "webhook_deleted": {"id": "7", "guild_id": "3", "channel_id": "2"},
}

EXPECTED_CLASSES = {
    "message_created": MessageEvent,
    "message_updated": MessageEvent,
    "message_deleted": MessageEvent,
    "message_pinned": MessageEvent,
    "message_unpinned": MessageEvent,
    "overwrite_updated": OverwriteEvent,
    "user_created": UserEvent,
    "user_updated": UserEvent,
    "user_deleted": UserEvent,
    "guild_created": GuildEvent,
    "guild_updated": GuildEvent,
    "guild_deleted": GuildEvent,
    "channel_created": ChannelEvent,
    "channel_updated": ChannelEvent,
    "channel_deleted": ChannelEvent,
    "channels_reordered": ChannelsReorderedEvent,
    "role_created": RoleEvent,
    "role_updated": RoleEvent,
    "role_deleted": RoleEvent,
    "role_granted": RoleAssignmentEvent,
    "role_revoked": RoleAssignmentEvent,
    "roles_reordered": RolesReorderedEvent,
    "emoji_created": EmojiEvent,
    "emoji_updated": EmojiEvent,
    "emoji_deleted": EmojiEvent,
    "reaction_added": MessageReactionEvent,
    "reaction_removed": MessageReactionEvent,
    "webhook_created": WebhookEvent,
    "webhook_updated": WebhookEvent,
    "webhook_deleted": WebhookEvent,
}


def frame(event_type: str, seq: int = 1) -> str:
    return json.dumps(
        {"op": "dispatch", "s": seq, "t": event_type, "d": EVENT_DATA[event_type]},
    )


def test_event_data_covers_every_event_type() -> None:
    assert {value.value for value in GatewayEventType} == set(EVENT_DATA)
    assert set(EXPECTED_CLASSES) == set(EVENT_DATA)


@pytest.mark.parametrize("event_type", EVENT_DATA)
def test_parse_every_event_type(event_type: str) -> None:
    event = parse_frame(frame(event_type))

    assert isinstance(event, EXPECTED_CLASSES[event_type])
    assert event.type is GatewayEventType(event_type)
    assert event.seq == 1


def test_gateway_url_translates_scheme_and_appends_path() -> None:
    assert gateway_url("https://chat.example.com/api") == "wss://chat.example.com/api/gateway"
    assert gateway_url("http://localhost:8080/api") == "ws://localhost:8080/api/gateway"
    assert gateway_url("http://localhost:8080/api/") == "ws://localhost:8080/api/gateway"
    assert gateway_url("https://chat.example.com") == "wss://chat.example.com/gateway"


def test_gateway_url_rejects_unsupported_urls() -> None:
    with pytest.raises(ValueError):
        gateway_url("ftp://chat.example.com/api")
    with pytest.raises(ValueError):
        gateway_url("https://chat.example.com/api?token=secret")
    with pytest.raises(ValueError):
        gateway_url("https:///api")


def test_identify_and_ack_frames() -> None:
    assert json.loads(identify_message("jwt")) == {"op": "identify", "d": {"token": "jwt"}}
    assert json.loads(ack_message()) == {"op": "ack"}

    with pytest.raises(ValueError):
        identify_message("")


def test_parse_hello() -> None:
    hello = parse_frame('{"op":"hello","d":{"heartbeat_interval":40000}}')

    assert hello == HelloFrame(heartbeat_interval_ms=40000)


@pytest.mark.parametrize("interval", [0, -1, "40000", None, True])
def test_parse_hello_rejects_invalid_interval(interval: object) -> None:
    with pytest.raises(GatewayProtocolError):
        parse_frame(json.dumps({"op": "hello", "d": {"heartbeat_interval": interval}}))


def test_reaction_event_keeps_nullable_emoji_fields() -> None:
    event = parse_frame(frame("reaction_added"))

    assert isinstance(event, MessageReactionEvent)
    assert event.emoji_id is None
    assert event.unicode_emoji == "thumbsup"
    assert event.message_id == "1"

    custom = parse_frame(frame("reaction_removed"))
    assert isinstance(custom, MessageReactionEvent)
    assert custom.emoji_id == "6"
    assert custom.unicode_emoji is None


def test_event_aliases() -> None:
    assert parse_frame(frame("message_created")).message_id == "1"  # type: ignore[union-attr]
    assert parse_frame(frame("role_granted")).role_id == "4"  # type: ignore[union-attr]
    assert parse_frame(frame("webhook_created")).webhook_id == "7"  # type: ignore[union-attr]


def test_unknown_event_type_is_preserved() -> None:
    event = parse_frame('{"op":"dispatch","s":9,"t":"future_event","d":{"x":1}}')

    assert isinstance(event, UnknownDispatchEvent)
    assert event.seq == 9
    assert event.event_type == "future_event"
    assert event.data == {"x": 1}


@pytest.mark.parametrize("op", ["heartbeat_ack", "reconnect", ""])
def test_unknown_op_is_skipped(op: str) -> None:
    assert parse_frame(json.dumps({"op": op})) is None


def test_bytes_frame_is_decoded() -> None:
    event = parse_frame(frame("user_created").encode())

    assert isinstance(event, UserEvent)


@pytest.mark.parametrize(
    "raw",
    [
        "not json",
        "[]",
        '"hello"',
        "{}",
        '{"op":1}',
        '{"op":"dispatch","t":"user_created","d":{"id":"1"}}',
        '{"op":"dispatch","s":1,"d":{"id":"1"}}',
        '{"op":"dispatch","s":1,"t":"user_created"}',
        '{"op":"dispatch","s":1,"t":"user_created","d":[]}',
        '{"op":"dispatch","s":1,"t":"user_created","d":{}}',
        '{"op":"dispatch","s":1,"t":"message_created","d":{"id":"1"}}',
        '{"op":"dispatch","s":1,"t":"reaction_added","d":{"id":"1","channel_id":"2",'
        '"guild_id":"3","user_id":"5","emoji_id":1}}',
    ],
)
def test_malformed_frames_raise(raw: str) -> None:
    with pytest.raises(GatewayProtocolError):
        parse_frame(raw)


def test_binary_frame_is_rejected() -> None:
    with pytest.raises(GatewayProtocolError):
        parse_frame(b"\xff\xfe\x00")


def test_build_ssl_context() -> None:
    assert build_ssl_context(True) is None

    insecure = build_ssl_context(False)
    assert isinstance(insecure, ssl.SSLContext)
    assert insecure.check_hostname is False
    assert insecure.verify_mode is ssl.CERT_NONE

    context = ssl.create_default_context()
    assert build_ssl_context(context) is context
