from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PushSubscriptionInput")


@_attrs_define
class PushSubscriptionInput:
    """A browser `PushSubscription` to register. Registering an endpoint already owned by another account takes it over
    (moves it to the caller).

        Attributes:
            endpoint (str): Absolute `http(s)` push service URL, within `api.push.max_endpoint_bytes` bytes. Stored verbatim
                (never normalized).
            p256dh (str): base64url (no padding) of the subscription's uncompressed P-256 public key (65 bytes;
                `PushSubscription.getKey('p256dh')`).
            auth (str): base64url (no padding) of the 16-byte authentication secret (`PushSubscription.getKey('auth')`).
    """

    endpoint: str
    p256dh: str
    auth: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        endpoint = self.endpoint

        p256dh = self.p256dh

        auth = self.auth

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "endpoint": endpoint,
                "p256dh": p256dh,
                "auth": auth,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        endpoint = d.pop("endpoint")

        p256dh = d.pop("p256dh")

        auth = d.pop("auth")

        push_subscription_input = cls(
            endpoint=endpoint,
            p256dh=p256dh,
            auth=auth,
        )

        push_subscription_input.additional_properties = d
        return push_subscription_input

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
