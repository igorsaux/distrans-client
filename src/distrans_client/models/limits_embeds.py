from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LimitsEmbeds")


@_attrs_define
class LimitsEmbeds:
    """
    Attributes:
        max_title_codepoints (int):
        max_description_codepoints (int):
        max_fields (int):
        max_footer_codepoints (int):
        max_author_name_codepoints (int):
        max_field_name_codepoints (int):
        max_field_value_codepoints (int):
        max_url_codepoints (int):
        max_total_codepoints (int):
    """

    max_title_codepoints: int
    max_description_codepoints: int
    max_fields: int
    max_footer_codepoints: int
    max_author_name_codepoints: int
    max_field_name_codepoints: int
    max_field_value_codepoints: int
    max_url_codepoints: int
    max_total_codepoints: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_title_codepoints = self.max_title_codepoints

        max_description_codepoints = self.max_description_codepoints

        max_fields = self.max_fields

        max_footer_codepoints = self.max_footer_codepoints

        max_author_name_codepoints = self.max_author_name_codepoints

        max_field_name_codepoints = self.max_field_name_codepoints

        max_field_value_codepoints = self.max_field_value_codepoints

        max_url_codepoints = self.max_url_codepoints

        max_total_codepoints = self.max_total_codepoints

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "max_title_codepoints": max_title_codepoints,
                "max_description_codepoints": max_description_codepoints,
                "max_fields": max_fields,
                "max_footer_codepoints": max_footer_codepoints,
                "max_author_name_codepoints": max_author_name_codepoints,
                "max_field_name_codepoints": max_field_name_codepoints,
                "max_field_value_codepoints": max_field_value_codepoints,
                "max_url_codepoints": max_url_codepoints,
                "max_total_codepoints": max_total_codepoints,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        max_title_codepoints = d.pop("max_title_codepoints")

        max_description_codepoints = d.pop("max_description_codepoints")

        max_fields = d.pop("max_fields")

        max_footer_codepoints = d.pop("max_footer_codepoints")

        max_author_name_codepoints = d.pop("max_author_name_codepoints")

        max_field_name_codepoints = d.pop("max_field_name_codepoints")

        max_field_value_codepoints = d.pop("max_field_value_codepoints")

        max_url_codepoints = d.pop("max_url_codepoints")

        max_total_codepoints = d.pop("max_total_codepoints")

        limits_embeds = cls(
            max_title_codepoints=max_title_codepoints,
            max_description_codepoints=max_description_codepoints,
            max_fields=max_fields,
            max_footer_codepoints=max_footer_codepoints,
            max_author_name_codepoints=max_author_name_codepoints,
            max_field_name_codepoints=max_field_name_codepoints,
            max_field_value_codepoints=max_field_value_codepoints,
            max_url_codepoints=max_url_codepoints,
            max_total_codepoints=max_total_codepoints,
        )

        limits_embeds.additional_properties = d
        return limits_embeds

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
