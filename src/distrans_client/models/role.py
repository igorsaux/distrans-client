from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Role")


@_attrs_define
class Role:
    """
    Attributes:
        id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        name (str): Max `api.roles.max_name_codepoints`; forbidden codepoints (Cc/Cf, zero-width, BiDi, ...) are
            rejected on create/modify with 400 "'name' is invalid".
        position (int): Read-only unique rank within the guild (@everyone is always 0); change it through PUT
            /guilds/{guild_id}/roles/order
        permissions (str): 128-bit permission mask as decimal string
        color (int | None):
        mentionable (bool): Whether members may mention this role. Defaults to `true` on creation; role mentions are
            gated by it (together with the `mention_everyone` permission for `@everyone`).
    """

    id: str
    name: str
    position: int
    permissions: str
    color: int | None
    mentionable: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        position = self.position

        permissions = self.permissions

        color: int | None
        color = self.color

        mentionable = self.mentionable

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "position": position,
                "permissions": permissions,
                "color": color,
                "mentionable": mentionable,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        position = d.pop("position")

        permissions = d.pop("permissions")

        def _parse_color(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        color = _parse_color(d.pop("color"))

        mentionable = d.pop("mentionable")

        role = cls(
            id=id,
            name=name,
            position=position,
            permissions=permissions,
            color=color,
            mentionable=mentionable,
        )

        role.additional_properties = d
        return role

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
