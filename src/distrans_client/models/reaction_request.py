from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReactionRequest")


@_attrs_define
class ReactionRequest:
    """Exactly one of `emoji_id` / `unicode_emoji` must be present; the emoji is identified by the two columns of
    `app.message_reactions`.

        Attributes:
            emoji_id (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
            unicode_emoji (str | Unset): Exactly one emoji sequence in any qualification form (fully-qualified, minimally-
                qualified or unqualified) or a regional indicator symbol (raw UTF-8, not percent-encoded). Stored in its
                canonical fully-qualified form.
    """

    emoji_id: str | Unset = UNSET
    unicode_emoji: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        emoji_id = self.emoji_id

        unicode_emoji = self.unicode_emoji

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if emoji_id is not UNSET:
            field_dict["emoji_id"] = emoji_id
        if unicode_emoji is not UNSET:
            field_dict["unicode_emoji"] = unicode_emoji

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        emoji_id = d.pop("emoji_id", UNSET)

        unicode_emoji = d.pop("unicode_emoji", UNSET)

        reaction_request = cls(
            emoji_id=emoji_id,
            unicode_emoji=unicode_emoji,
        )

        reaction_request.additional_properties = d
        return reaction_request

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
