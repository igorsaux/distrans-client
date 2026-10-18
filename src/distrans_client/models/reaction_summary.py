from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ReactionSummary")


@_attrs_define
class ReactionSummary:
    """Exactly one of `emoji_id` / `unicode_emoji` is set; `count` is the number of non-deleted users who reacted with that
    emoji (equal to the length of `GET /messages/{message_id}/reactions/users` for it) and `me` is whether the caller
    did.

        Attributes:
            emoji_id (None | str):
            unicode_emoji (None | str):
            count (int):
            me (bool):
    """

    emoji_id: None | str
    unicode_emoji: None | str
    count: int
    me: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        emoji_id: None | str
        emoji_id = self.emoji_id

        unicode_emoji: None | str
        unicode_emoji = self.unicode_emoji

        count = self.count

        me = self.me

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "emoji_id": emoji_id,
                "unicode_emoji": unicode_emoji,
                "count": count,
                "me": me,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_emoji_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        emoji_id = _parse_emoji_id(d.pop("emoji_id"))

        def _parse_unicode_emoji(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        unicode_emoji = _parse_unicode_emoji(d.pop("unicode_emoji"))

        count = d.pop("count")

        me = d.pop("me")

        reaction_summary = cls(
            emoji_id=emoji_id,
            unicode_emoji=unicode_emoji,
            count=count,
            me=me,
        )

        reaction_summary.additional_properties = d
        return reaction_summary

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
