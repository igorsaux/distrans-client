from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Emoji")


@_attrs_define
class Emoji:
    """
    Attributes:
        id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        name (str): Unique within the guild.
        icon_hash (str): XXHash64 of the stored webp icon, 16 lowercase hex chars. Fetch the image from `GET
            /emojis/{emoji_id}/icon?hash={icon_hash}`.
    """

    id: str
    name: str
    icon_hash: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        icon_hash = self.icon_hash

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "icon_hash": icon_hash,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        icon_hash = d.pop("icon_hash")

        emoji = cls(
            id=id,
            name=name,
            icon_hash=icon_hash,
        )

        emoji.additional_properties = d
        return emoji

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
