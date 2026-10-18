from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.guild_sync_overwrites_item import GuildSyncOverwritesItem


T = TypeVar("T", bound="GuildSync")


@_attrs_define
class GuildSync:
    """
    Attributes:
        updated_at (int): Server cursor: the database `now()` captured at query start, in epoch milliseconds. Store it
            and pass it as the next `since`.
        channels (list[str]):
        roles (list[str]):
        emojis (list[str]):
        overwrites (list[GuildSyncOverwritesItem]):
        member_roles (list[str]): The caller's complete current role-id set in this guild.
    """

    updated_at: int
    channels: list[str]
    roles: list[str]
    emojis: list[str]
    overwrites: list[GuildSyncOverwritesItem]
    member_roles: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        updated_at = self.updated_at

        channels = self.channels

        roles = self.roles

        emojis = self.emojis

        overwrites = []
        for overwrites_item_data in self.overwrites:
            overwrites_item = overwrites_item_data.to_dict()
            overwrites.append(overwrites_item)

        member_roles = self.member_roles

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "updated_at": updated_at,
                "channels": channels,
                "roles": roles,
                "emojis": emojis,
                "overwrites": overwrites,
                "member_roles": member_roles,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.guild_sync_overwrites_item import GuildSyncOverwritesItem

        d = dict(src_dict)
        updated_at = d.pop("updated_at")

        channels = cast(list[str], d.pop("channels"))

        roles = cast(list[str], d.pop("roles"))

        emojis = cast(list[str], d.pop("emojis"))

        overwrites = []
        _overwrites = d.pop("overwrites")
        for overwrites_item_data in _overwrites:
            overwrites_item = GuildSyncOverwritesItem.from_dict(overwrites_item_data)

            overwrites.append(overwrites_item)

        member_roles = cast(list[str], d.pop("member_roles"))

        guild_sync = cls(
            updated_at=updated_at,
            channels=channels,
            roles=roles,
            emojis=emojis,
            overwrites=overwrites,
            member_roles=member_roles,
        )

        guild_sync.additional_properties = d
        return guild_sync

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
