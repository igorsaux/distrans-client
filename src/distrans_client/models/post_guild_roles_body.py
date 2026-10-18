from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostGuildRolesBody")


@_attrs_define
class PostGuildRolesBody:
    """
    Attributes:
        name (str): Max `api.roles.max_name_codepoints`; forbidden codepoints (Cc/Cf, zero-width, BiDi, ...) are
            rejected with 400 "'name' is invalid".
        permissions (str): 128-bit permission mask as decimal string
        color (int | None | Unset):
        mentionable (bool | None | Unset): Defaults to true when absent
    """

    name: str
    permissions: str
    color: int | None | Unset = UNSET
    mentionable: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        permissions = self.permissions

        color: int | None | Unset
        if isinstance(self.color, Unset):
            color = UNSET
        else:
            color = self.color

        mentionable: bool | None | Unset
        if isinstance(self.mentionable, Unset):
            mentionable = UNSET
        else:
            mentionable = self.mentionable

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "permissions": permissions,
            }
        )
        if color is not UNSET:
            field_dict["color"] = color
        if mentionable is not UNSET:
            field_dict["mentionable"] = mentionable

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name")

        permissions = d.pop("permissions")

        def _parse_color(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        color = _parse_color(d.pop("color", UNSET))

        def _parse_mentionable(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        mentionable = _parse_mentionable(d.pop("mentionable", UNSET))

        post_guild_roles_body = cls(
            name=name,
            permissions=permissions,
            color=color,
            mentionable=mentionable,
        )

        post_guild_roles_body.additional_properties = d
        return post_guild_roles_body

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
