from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Guild")


@_attrs_define
class Guild:
    """
    Attributes:
        id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        name (str):
        avatar_hash (None | str): XXHash64 of the stored webp avatar, 16 lowercase hex chars; null when the guild has no
            avatar. Fetch the image from `GET /guilds/{guild_id}/avatar?hash={avatar_hash}`.
    """

    id: str
    name: str
    avatar_hash: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        avatar_hash: None | str
        avatar_hash = self.avatar_hash

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "avatar_hash": avatar_hash,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        def _parse_avatar_hash(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        avatar_hash = _parse_avatar_hash(d.pop("avatar_hash"))

        guild = cls(
            id=id,
            name=name,
            avatar_hash=avatar_hash,
        )

        guild.additional_properties = d
        return guild

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
