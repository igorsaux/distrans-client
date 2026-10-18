from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LimitsPush")


@_attrs_define
class LimitsPush:
    """Browser Web Push availability. When `enabled` is false the subscription endpoints still store rows but no
    notification is delivered. `vapid_public_key` is the base64url `applicationServerKey` the client passes to
    `PushManager.subscribe`.

        Attributes:
            enabled (bool):
            vapid_public_key (str):
            max_subscriptions_per_user (int):
    """

    enabled: bool
    vapid_public_key: str
    max_subscriptions_per_user: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        vapid_public_key = self.vapid_public_key

        max_subscriptions_per_user = self.max_subscriptions_per_user

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "vapid_public_key": vapid_public_key,
                "max_subscriptions_per_user": max_subscriptions_per_user,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        vapid_public_key = d.pop("vapid_public_key")

        max_subscriptions_per_user = d.pop("max_subscriptions_per_user")

        limits_push = cls(
            enabled=enabled,
            vapid_public_key=vapid_public_key,
            max_subscriptions_per_user=max_subscriptions_per_user,
        )

        limits_push.additional_properties = d
        return limits_push

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
