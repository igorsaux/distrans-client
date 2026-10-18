from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchSystemUserBody")


@_attrs_define
class PatchSystemUserBody:
    """
    Attributes:
        username (str | Unset): Allowlist `a-z`, `0-9`, `.`, `_`; the first and the last characters must be
            alphanumeric; `..` is forbidden; max `api.users.max_username_codepoints`, min
            `api.users.min_username_codepoints`; reserved names are rejected.
        display_name (None | str | Unset): Min `api.users.min_display_name_codepoints`, max
            `api.users.max_display_name_codepoints`.
        password (None | str | Unset): Min `auth.password.min_password_codepoints`, max
            `auth.password.max_password_codepoints` codepoints and `auth.password.max_password_len` bytes; forbidden for
            bots.
    """

    username: str | Unset = UNSET
    display_name: None | str | Unset = UNSET
    password: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        display_name: None | str | Unset
        if isinstance(self.display_name, Unset):
            display_name = UNSET
        else:
            display_name = self.display_name

        password: None | str | Unset
        if isinstance(self.password, Unset):
            password = UNSET
        else:
            password = self.password

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if username is not UNSET:
            field_dict["username"] = username
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if password is not UNSET:
            field_dict["password"] = password

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        username = d.pop("username", UNSET)

        def _parse_display_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        display_name = _parse_display_name(d.pop("display_name", UNSET))

        def _parse_password(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        password = _parse_password(d.pop("password", UNSET))

        patch_system_user_body = cls(
            username=username,
            display_name=display_name,
            password=password,
        )

        patch_system_user_body.additional_properties = d
        return patch_system_user_body

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
