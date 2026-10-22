from __future__ import annotations

from distrans_client.models.edit_message_body import EditMessageBody
from distrans_client.models.edit_webhook_message_body import EditWebhookMessageBody
from distrans_client.models.embed import Embed
from distrans_client.models.execute_webhook_body import ExecuteWebhookBody
from distrans_client.models.message import Message
from distrans_client.models.post_message_body import PostMessageBody
from distrans_client.types import UNSET


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


def test_message_bodies_do_not_require_content() -> None:
    for body_type in (PostMessageBody, ExecuteWebhookBody, EditMessageBody, EditWebhookMessageBody):
        body = body_type()

        assert body.content is UNSET
        assert "content" not in body.to_dict()


def test_message_bodies_serialize_embeds_without_content() -> None:
    embed = Embed(title="hello")

    for body_type in (PostMessageBody, ExecuteWebhookBody, EditMessageBody, EditWebhookMessageBody):
        body = body_type(embeds=[embed])

        assert body.to_dict() == {"embeds": [embed.to_dict()]}
        assert "content" not in body.to_dict()
