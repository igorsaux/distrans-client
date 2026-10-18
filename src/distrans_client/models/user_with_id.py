from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UserWithId")


@_attrs_define
class UserWithId:
    """
    Attributes:
        username (str):
        display_name (None | str):
        avatar_hash (None | str): XXHash64 of the stored webp avatar, 16 lowercase hex chars; null when the user has no
            avatar. Fetch the image from `GET /users/{user_id}/avatar?hash={avatar_hash}`.
        is_bot (bool):
        id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
    """

    username: str
    display_name: None | str
    avatar_hash: None | str
    is_bot: bool
    id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        display_name: None | str
        display_name = self.display_name

        avatar_hash: None | str
        avatar_hash = self.avatar_hash

        is_bot = self.is_bot

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "display_name": display_name,
                "avatar_hash": avatar_hash,
                "is_bot": is_bot,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        username = d.pop("username")

        def _parse_display_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        display_name = _parse_display_name(d.pop("display_name"))

        def _parse_avatar_hash(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        avatar_hash = _parse_avatar_hash(d.pop("avatar_hash"))

        is_bot = d.pop("is_bot")

        id = d.pop("id")

        user_with_id = cls(
            username=username,
            display_name=display_name,
            avatar_hash=avatar_hash,
            is_bot=is_bot,
            id=id,
        )

        user_with_id.additional_properties = d
        return user_with_id

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
