from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.allowed_mentions import AllowedMentions
    from ..models.embed import Embed


T = TypeVar("T", bound="ExecuteWebhookBody")


@_attrs_define
class ExecuteWebhookBody:
    """
    Attributes:
        content (str):
        reply_to_id (None | str | Unset):
        embeds (list[Embed] | None | Unset):
        allowed_mentions (AllowedMentions | None | Unset):
    """

    content: str
    reply_to_id: None | str | Unset = UNSET
    embeds: list[Embed] | None | Unset = UNSET
    allowed_mentions: AllowedMentions | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.allowed_mentions import AllowedMentions

        content = self.content

        reply_to_id: None | str | Unset
        if isinstance(self.reply_to_id, Unset):
            reply_to_id = UNSET
        else:
            reply_to_id = self.reply_to_id

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

        allowed_mentions: dict[str, Any] | None | Unset
        if isinstance(self.allowed_mentions, Unset):
            allowed_mentions = UNSET
        elif isinstance(self.allowed_mentions, AllowedMentions):
            allowed_mentions = self.allowed_mentions.to_dict()
        else:
            allowed_mentions = self.allowed_mentions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
            }
        )
        if reply_to_id is not UNSET:
            field_dict["reply_to_id"] = reply_to_id
        if embeds is not UNSET:
            field_dict["embeds"] = embeds
        if allowed_mentions is not UNSET:
            field_dict["allowed_mentions"] = allowed_mentions

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.allowed_mentions import AllowedMentions
        from ..models.embed import Embed

        d = dict(src_dict)
        content = d.pop("content")

        def _parse_reply_to_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reply_to_id = _parse_reply_to_id(d.pop("reply_to_id", UNSET))

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

        def _parse_allowed_mentions(data: object) -> AllowedMentions | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                allowed_mentions_type_1 = AllowedMentions.from_dict(data)

                return allowed_mentions_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AllowedMentions | None | Unset, data)

        allowed_mentions = _parse_allowed_mentions(d.pop("allowed_mentions", UNSET))

        execute_webhook_body = cls(
            content=content,
            reply_to_id=reply_to_id,
            embeds=embeds,
            allowed_mentions=allowed_mentions,
        )

        execute_webhook_body.additional_properties = d
        return execute_webhook_body

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
