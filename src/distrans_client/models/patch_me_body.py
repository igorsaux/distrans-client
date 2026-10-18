from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchMeBody")


@_attrs_define
class PatchMeBody:
    """
    Attributes:
        current_password (str): Current password. Required for every PATCH and verified against the stored hash
            (mismatch → 401 "Bad password"); max `auth.password.max_password_len` in bytes.
        username (str | Unset): New username. Same validation as account creation: min/max
            `api.users.min/max_username_codepoints`, allowlist `a-z`, `0-9`, `.`, `_` (first/last alphanumeric, no `..`),
            reserved names rejected with 400 "'username' is reserved". A username already in use is rejected with 409
            "Username is already used". Not nullable: an explicit `null` is a 400 "'username' is not a string".
        display_name (None | str | Unset): Min `api.users.min_display_name_codepoints`, max
            `api.users.max_display_name_codepoints`; forbidden codepoints (Cc/Cf, zero-width, BiDi, ...) are rejected with
            400 "'display_name' is invalid".
        password (str | Unset): New password. Min/max per `auth.password` (`min_password_codepoints` /
            `max_password_codepoints`, additionally `max_password_len` in bytes). Requires `current_password` and must
            differ from it. On success all refresh tokens of the user are revoked except the one in the `refresh_token`
            cookie when the cookie is sent, otherwise every refresh token of the user is revoked; all of the user's push
            subscriptions are removed in both cases, so the client must re-register the current device.
    """

    current_password: str
    username: str | Unset = UNSET
    display_name: None | str | Unset = UNSET
    password: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        current_password = self.current_password

        username = self.username

        display_name: None | str | Unset
        if isinstance(self.display_name, Unset):
            display_name = UNSET
        else:
            display_name = self.display_name

        password = self.password

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "current_password": current_password,
            }
        )
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
        current_password = d.pop("current_password")

        username = d.pop("username", UNSET)

        def _parse_display_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        display_name = _parse_display_name(d.pop("display_name", UNSET))

        password = d.pop("password", UNSET)

        patch_me_body = cls(
            current_password=current_password,
            username=username,
            display_name=display_name,
            password=password,
        )

        patch_me_body.additional_properties = d
        return patch_me_body

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
