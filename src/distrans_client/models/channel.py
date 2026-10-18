from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.channel_kind import ChannelKind

if TYPE_CHECKING:
    from ..models.overwrite import Overwrite


T = TypeVar("T", bound="Channel")


@_attrs_define
class Channel:
    """
    Attributes:
        id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        parent_id (None | str):
        kind (ChannelKind):
        name (str):
        topic (None | str):
        position (int): Read-only ordering within the channel's parent scope; change it through PUT
            /guilds/{guild_id}/channels/order
        last_message_id (None | str): The id of the newest non-deleted message in the channel, or null when the channel
            has no non-deleted messages.
        permissions (str): 128-bit permission mask as decimal string
        overwrites (list[Overwrite]): Full permission-overwrite list of the channel, ordered by target type then target
            id. An empty array when the channel has none. Readable by any authenticated user. Mutation is still through PUT
            /channels/{channel_id}/overwrites.
    """

    id: str
    parent_id: None | str
    kind: ChannelKind
    name: str
    topic: None | str
    position: int
    last_message_id: None | str
    permissions: str
    overwrites: list[Overwrite]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        parent_id: None | str
        parent_id = self.parent_id

        kind = self.kind.value

        name = self.name

        topic: None | str
        topic = self.topic

        position = self.position

        last_message_id: None | str
        last_message_id = self.last_message_id

        permissions = self.permissions

        overwrites = []
        for overwrites_item_data in self.overwrites:
            overwrites_item = overwrites_item_data.to_dict()
            overwrites.append(overwrites_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "parent_id": parent_id,
                "kind": kind,
                "name": name,
                "topic": topic,
                "position": position,
                "last_message_id": last_message_id,
                "permissions": permissions,
                "overwrites": overwrites,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.overwrite import Overwrite

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_parent_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        parent_id = _parse_parent_id(d.pop("parent_id"))

        kind = ChannelKind(d.pop("kind"))

        name = d.pop("name")

        def _parse_topic(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        topic = _parse_topic(d.pop("topic"))

        position = d.pop("position")

        def _parse_last_message_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        last_message_id = _parse_last_message_id(d.pop("last_message_id"))

        permissions = d.pop("permissions")

        overwrites = []
        _overwrites = d.pop("overwrites")
        for overwrites_item_data in _overwrites:
            overwrites_item = Overwrite.from_dict(overwrites_item_data)

            overwrites.append(overwrites_item)

        channel = cls(
            id=id,
            parent_id=parent_id,
            kind=kind,
            name=name,
            topic=topic,
            position=position,
            last_message_id=last_message_id,
            permissions=permissions,
            overwrites=overwrites,
        )

        channel.additional_properties = d
        return channel

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
