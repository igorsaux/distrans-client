from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.patch_me_channel_notifications_body_level import (
    PatchMeChannelNotificationsBodyLevel,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchMeChannelNotificationsBody")


@_attrs_define
class PatchMeChannelNotificationsBody:
    """
    Attributes:
        level (PatchMeChannelNotificationsBodyLevel | Unset):
    """

    level: PatchMeChannelNotificationsBodyLevel | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        level: str | Unset = UNSET
        if not isinstance(self.level, Unset):
            level = self.level.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if level is not UNSET:
            field_dict["level"] = level

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        _level = d.pop("level", UNSET)
        level: PatchMeChannelNotificationsBodyLevel | Unset
        if isinstance(_level, Unset):
            level = UNSET
        else:
            level = PatchMeChannelNotificationsBodyLevel(_level)

        patch_me_channel_notifications_body = cls(
            level=level,
        )

        patch_me_channel_notifications_body.additional_properties = d
        return patch_me_channel_notifications_body

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
