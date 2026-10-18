from __future__ import annotations

from distrans_client.models.message import Message


def message_payload() -> dict:
    return {
        "id": "1",
        "channel_id": "2",
        "author_id": None,
        "webhook_id": "3",
        "content": "hello",
        "created_at": 1_700_000_000_000,
        "reply_to_id": None,
        "edited_at": None,
        "embeds": None,
        "attachments": [],
        "mention_everyone": False,
        "mentions": [],
        "mention_roles": [],
        "pinned": False,
        "reactions": None,
    }


def test_message_round_trip() -> None:
    payload = message_payload()
    message = Message.from_dict(payload)

    assert message.id == "1"
    assert message.author_id is None
    assert message.webhook_id == "3"
    assert message.to_dict() == payload


def test_message_nullable_fields_are_required() -> None:
    message = Message.from_dict(message_payload())

    assert message.reply_to_id is None
    assert message.edited_at is None
    assert message.reactions is None
