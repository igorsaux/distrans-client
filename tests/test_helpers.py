from __future__ import annotations

from distrans_client import emoji_token, no_mentions
from distrans_client.models.emoji import Emoji


def test_emoji_token() -> None:
    emoji = Emoji(id="1", name="cat", icon_hash="x")
    assert emoji_token(emoji) == "<:cat:1>"


def test_no_mentions_returns_fresh_object() -> None:
    first = no_mentions()
    second = no_mentions()

    assert first is not second
    assert first.parse == []
    assert second.parse == []
