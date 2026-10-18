from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LimitsUsers")


@_attrs_define
class LimitsUsers:
    """
    Attributes:
        min_username_codepoints (int):
        max_username_codepoints (int):
        min_display_name_codepoints (int):
        max_display_name_codepoints (int):
        max_userdata_bytes (int):
    """

    min_username_codepoints: int
    max_username_codepoints: int
    min_display_name_codepoints: int
    max_display_name_codepoints: int
    max_userdata_bytes: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        min_username_codepoints = self.min_username_codepoints

        max_username_codepoints = self.max_username_codepoints

        min_display_name_codepoints = self.min_display_name_codepoints

        max_display_name_codepoints = self.max_display_name_codepoints

        max_userdata_bytes = self.max_userdata_bytes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "min_username_codepoints": min_username_codepoints,
                "max_username_codepoints": max_username_codepoints,
                "min_display_name_codepoints": min_display_name_codepoints,
                "max_display_name_codepoints": max_display_name_codepoints,
                "max_userdata_bytes": max_userdata_bytes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        min_username_codepoints = d.pop("min_username_codepoints")

        max_username_codepoints = d.pop("max_username_codepoints")

        min_display_name_codepoints = d.pop("min_display_name_codepoints")

        max_display_name_codepoints = d.pop("max_display_name_codepoints")

        max_userdata_bytes = d.pop("max_userdata_bytes")

        limits_users = cls(
            min_username_codepoints=min_username_codepoints,
            max_username_codepoints=max_username_codepoints,
            min_display_name_codepoints=min_display_name_codepoints,
            max_display_name_codepoints=max_display_name_codepoints,
            max_userdata_bytes=max_userdata_bytes,
        )

        limits_users.additional_properties = d
        return limits_users

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
