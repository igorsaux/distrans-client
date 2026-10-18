from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.embed import Embed


T = TypeVar("T", bound="EditMessageBody")


@_attrs_define
class EditMessageBody:
    """
    Attributes:
        content (str):
        embeds (list[Embed] | None | Unset): Replaces the message's embeds. `null` or `[]` clears them; absent leaves
            them unchanged; at most `api.messages.max_embeds` are accepted.
    """

    content: str
    embeds: list[Embed] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content = self.content

        embeds: list[dict[str, Any]] | None | Unset
        if isinstance(self.embeds, Unset):
            embeds = UNSET
        elif isinstance(self.embeds, list):
            embeds = []
            for embeds_type_0_item_data in self.embeds:
                embeds_type_0_item = embeds_type_0_item_data.to_dict()
                embeds.append(embeds_type_0_item)

        else:
            embeds = self.embeds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
            }
        )
        if embeds is not UNSET:
            field_dict["embeds"] = embeds

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.embed import Embed

        d = dict(src_dict)
        content = d.pop("content")

        def _parse_embeds(data: object) -> list[Embed] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                embeds_type_0 = []
                _embeds_type_0 = data
                for embeds_type_0_item_data in _embeds_type_0:
                    embeds_type_0_item = Embed.from_dict(embeds_type_0_item_data)

                    embeds_type_0.append(embeds_type_0_item)

                return embeds_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Embed] | None | Unset, data)

        embeds = _parse_embeds(d.pop("embeds", UNSET))

        edit_message_body = cls(
            content=content,
            embeds=embeds,
        )

        edit_message_body.additional_properties = d
        return edit_message_body

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
