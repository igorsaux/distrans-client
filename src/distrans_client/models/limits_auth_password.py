from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LimitsAuthPassword")


@_attrs_define
class LimitsAuthPassword:
    """
    Attributes:
        min_codepoints (int):
        max_codepoints (int):
        max_bytes (int):
    """

    min_codepoints: int
    max_codepoints: int
    max_bytes: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        min_codepoints = self.min_codepoints

        max_codepoints = self.max_codepoints

        max_bytes = self.max_bytes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "min_codepoints": min_codepoints,
                "max_codepoints": max_codepoints,
                "max_bytes": max_bytes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        min_codepoints = d.pop("min_codepoints")

        max_codepoints = d.pop("max_codepoints")

        max_bytes = d.pop("max_bytes")

        limits_auth_password = cls(
            min_codepoints=min_codepoints,
            max_codepoints=max_codepoints,
            max_bytes=max_bytes,
        )

        limits_auth_password.additional_properties = d
        return limits_auth_password

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
