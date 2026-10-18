from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LimitsEmojis")


@_attrs_define
class LimitsEmojis:
    """
    Attributes:
        min_name_codepoints (int):
        max_name_codepoints (int):
    """

    min_name_codepoints: int
    max_name_codepoints: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        min_name_codepoints = self.min_name_codepoints

        max_name_codepoints = self.max_name_codepoints

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "min_name_codepoints": min_name_codepoints,
                "max_name_codepoints": max_name_codepoints,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        min_name_codepoints = d.pop("min_name_codepoints")

        max_name_codepoints = d.pop("max_name_codepoints")

        limits_emojis = cls(
            min_name_codepoints=min_name_codepoints,
            max_name_codepoints=max_name_codepoints,
        )

        limits_emojis.additional_properties = d
        return limits_emojis

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
