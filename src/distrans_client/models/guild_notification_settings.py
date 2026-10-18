from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.guild_notification_settings_level import GuildNotificationSettingsLevel

T = TypeVar("T", bound="GuildNotificationSettings")


@_attrs_define
class GuildNotificationSettings:
    """The caller's notification settings for a guild.

    Attributes:
        level (GuildNotificationSettingsLevel): Default `all_messages`. `only_mentions` notifies only on mentions;
            `nothing` suppresses all notifications for the guild.
        suppress_everyone (bool): Ignore @everyone and @here. Default false.
        suppress_roles (bool): Do not notify on role mentions. Default false.
        push (bool): Whether the guild may produce browser push notifications. Default true.
    """

    level: GuildNotificationSettingsLevel
    suppress_everyone: bool
    suppress_roles: bool
    push: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        level = self.level.value

        suppress_everyone = self.suppress_everyone

        suppress_roles = self.suppress_roles

        push = self.push

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "level": level,
                "suppress_everyone": suppress_everyone,
                "suppress_roles": suppress_roles,
                "push": push,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        level = GuildNotificationSettingsLevel(d.pop("level"))

        suppress_everyone = d.pop("suppress_everyone")

        suppress_roles = d.pop("suppress_roles")

        push = d.pop("push")

        guild_notification_settings = cls(
            level=level,
            suppress_everyone=suppress_everyone,
            suppress_roles=suppress_roles,
            push=push,
        )

        guild_notification_settings.additional_properties = d
        return guild_notification_settings

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
