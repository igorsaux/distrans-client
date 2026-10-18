from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostSystemUserBody")


@_attrs_define
class PostSystemUserBody:
    """
    Attributes:
        username (str): Allowlist `a-z`, `0-9`, `.`, `_`; the first and the last characters must be alphanumeric; `..`
            is forbidden; max `api.users.max_username_codepoints`, min `api.users.min_username_codepoints`; reserved names
            are rejected.
        id (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        password (str | Unset): Forbidden for bots
        is_bot (bool | Unset):
        display_name (str | Unset): Max `api.users.max_display_name_codepoints`
    """

    username: str
    id: str | Unset = UNSET
    password: str | Unset = UNSET
    is_bot: bool | Unset = UNSET
    display_name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        id = self.id

        password = self.password

        is_bot = self.is_bot

        display_name = self.display_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if password is not UNSET:
            field_dict["password"] = password
        if is_bot is not UNSET:
            field_dict["is_bot"] = is_bot
        if display_name is not UNSET:
            field_dict["display_name"] = display_name

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        username = d.pop("username")

        id = d.pop("id", UNSET)

        password = d.pop("password", UNSET)

        is_bot = d.pop("is_bot", UNSET)

        display_name = d.pop("display_name", UNSET)

        post_system_user_body = cls(
            username=username,
            id=id,
            password=password,
            is_bot=is_bot,
            display_name=display_name,
        )

        post_system_user_body.additional_properties = d
        return post_system_user_body

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
