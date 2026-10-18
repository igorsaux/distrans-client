from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.patch_me_guild_notifications_body_level import (
    PatchMeGuildNotificationsBodyLevel,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchMeGuildNotificationsBody")


@_attrs_define
class PatchMeGuildNotificationsBody:
    """
    Attributes:
        level (PatchMeGuildNotificationsBodyLevel | Unset):
        suppress_everyone (bool | Unset):
        suppress_roles (bool | Unset):
        push (bool | Unset):
    """

    level: PatchMeGuildNotificationsBodyLevel | Unset = UNSET
    suppress_everyone: bool | Unset = UNSET
    suppress_roles: bool | Unset = UNSET
    push: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        level: str | Unset = UNSET
        if not isinstance(self.level, Unset):
            level = self.level.value

        suppress_everyone = self.suppress_everyone

        suppress_roles = self.suppress_roles

        push = self.push

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if level is not UNSET:
            field_dict["level"] = level
        if suppress_everyone is not UNSET:
            field_dict["suppress_everyone"] = suppress_everyone
        if suppress_roles is not UNSET:
            field_dict["suppress_roles"] = suppress_roles
        if push is not UNSET:
            field_dict["push"] = push

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        _level = d.pop("level", UNSET)
        level: PatchMeGuildNotificationsBodyLevel | Unset
        if isinstance(_level, Unset):
            level = UNSET
        else:
            level = PatchMeGuildNotificationsBodyLevel(_level)

        suppress_everyone = d.pop("suppress_everyone", UNSET)

        suppress_roles = d.pop("suppress_roles", UNSET)

        push = d.pop("push", UNSET)

        patch_me_guild_notifications_body = cls(
            level=level,
            suppress_everyone=suppress_everyone,
            suppress_roles=suppress_roles,
            push=push,
        )

        patch_me_guild_notifications_body.additional_properties = d
        return patch_me_guild_notifications_body

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
