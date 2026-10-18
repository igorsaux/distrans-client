from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.channel_notification_settings_effective_level import (
    ChannelNotificationSettingsEffectiveLevel,
)
from ..models.channel_notification_settings_level import (
    ChannelNotificationSettingsLevel,
)

T = TypeVar("T", bound="ChannelNotificationSettings")


@_attrs_define
class ChannelNotificationSettings:
    """The caller's notification settings for a text channel or category.

    Attributes:
        level (ChannelNotificationSettingsLevel): The stored level. Default `inherit`: fall back to the parent category
            (text channels) and then the guild. `nothing` suppresses notifications for the channel regardless of the guild.
        effective_level (ChannelNotificationSettingsEffectiveLevel): The fully resolved level (never `inherit`),
            following the chain channel -> parent category -> guild. Lets a client render the "use default" option's current
            value without extra requests.
    """

    level: ChannelNotificationSettingsLevel
    effective_level: ChannelNotificationSettingsEffectiveLevel
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        level = self.level.value

        effective_level = self.effective_level.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "level": level,
                "effective_level": effective_level,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        level = ChannelNotificationSettingsLevel(d.pop("level"))

        effective_level = ChannelNotificationSettingsEffectiveLevel(
            d.pop("effective_level")
        )

        channel_notification_settings = cls(
            level=level,
            effective_level=effective_level,
        )

        channel_notification_settings.additional_properties = d
        return channel_notification_settings

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
