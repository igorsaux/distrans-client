from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchRoleBody")


@_attrs_define
class PatchRoleBody:
    """
    Attributes:
        name (str | Unset): Max `api.roles.max_name_codepoints`; forbidden codepoints (Cc/Cf, zero-width, BiDi, ...) are
            rejected with 400 "'name' is invalid".
        permissions (str | Unset): 128-bit permission mask as decimal string
        color (int | None | Unset): null clears the color
        mentionable (bool | Unset): Absent leaves the value unchanged
    """

    name: str | Unset = UNSET
    permissions: str | Unset = UNSET
    color: int | None | Unset = UNSET
    mentionable: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        permissions = self.permissions

        color: int | None | Unset
        if isinstance(self.color, Unset):
            color = UNSET
        else:
            color = self.color

        mentionable = self.mentionable

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if color is not UNSET:
            field_dict["color"] = color
        if mentionable is not UNSET:
            field_dict["mentionable"] = mentionable

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        permissions = d.pop("permissions", UNSET)

        def _parse_color(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        color = _parse_color(d.pop("color", UNSET))

        mentionable = d.pop("mentionable", UNSET)

        patch_role_body = cls(
            name=name,
            permissions=permissions,
            color=color,
            mentionable=mentionable,
        )

        patch_role_body.additional_properties = d
        return patch_role_body

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
