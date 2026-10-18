from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.post_guild_channel_body_kind import PostGuildChannelBodyKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="PostGuildChannelBody")


@_attrs_define
class PostGuildChannelBody:
    """
    Attributes:
        name (str): Max `api.channels.max_name_codepoints`
        kind (PostGuildChannelBodyKind):
        topic (str | Unset): Only for kind="channel"; max `api.channels.max_topic_codepoints`
        parent_id (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
    """

    name: str
    kind: PostGuildChannelBodyKind
    topic: str | Unset = UNSET
    parent_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        kind = self.kind.value

        topic = self.topic

        parent_id = self.parent_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "kind": kind,
            }
        )
        if topic is not UNSET:
            field_dict["topic"] = topic
        if parent_id is not UNSET:
            field_dict["parent_id"] = parent_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name")

        kind = PostGuildChannelBodyKind(d.pop("kind"))

        topic = d.pop("topic", UNSET)

        parent_id = d.pop("parent_id", UNSET)

        post_guild_channel_body = cls(
            name=name,
            kind=kind,
            topic=topic,
            parent_id=parent_id,
        )

        post_guild_channel_body.additional_properties = d
        return post_guild_channel_body

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
