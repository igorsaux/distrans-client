from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmbedField")


@_attrs_define
class EmbedField:
    """A single embed field. `name` and `value` are required and follow the message-text profile (NFKC-normalized,
    forbidden codepoints stripped) bounded by `api.embeds.max_field_name_codepoints` and
    `api.embeds.max_field_value_codepoints`.

        Attributes:
            name (str):
            value (str):
            inline (bool | Unset):  Default: False.
    """

    name: str
    value: str
    inline: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        value = self.value

        inline = self.inline

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "value": value,
            }
        )
        if inline is not UNSET:
            field_dict["inline"] = inline

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name")

        value = d.pop("value")

        inline = d.pop("inline", UNSET)

        embed_field = cls(
            name=name,
            value=value,
            inline=inline,
        )

        embed_field.additional_properties = d
        return embed_field

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
