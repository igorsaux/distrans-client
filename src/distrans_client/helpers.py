"""Small hand-written helpers for working with generated models."""

from __future__ import annotations

from .models.allowed_mentions import AllowedMentions
from .models.emoji import Emoji

__all__ = ["emoji_token", "no_mentions"]


def emoji_token(emoji: Emoji) -> str:
    """Serialize a custom emoji as the wire token ``<:name:id>``."""
    return f"<:{emoji.name}:{emoji.id}>"


def no_mentions() -> AllowedMentions:
    """Return a fresh ``AllowedMentions(parse=[])`` that suppresses every mention."""
    return AllowedMentions(parse=[])
