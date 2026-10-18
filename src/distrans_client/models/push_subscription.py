from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PushSubscription")


@_attrs_define
class PushSubscription:
    """A stored browser push subscription (secrets omitted). An endpoint is globally unique: it belongs to exactly one
    account (the one currently logged in in that browser profile).

        Attributes:
            id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
            endpoint (str): The push service URL from `PushSubscription.endpoint`.
            created_at (int): Unix epoch in milliseconds.
    """

    id: str
    endpoint: str
    created_at: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        endpoint = self.endpoint

        created_at = self.created_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "endpoint": endpoint,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        endpoint = d.pop("endpoint")

        created_at = d.pop("created_at")

        push_subscription = cls(
            id=id,
            endpoint=endpoint,
            created_at=created_at,
        )

        push_subscription.additional_properties = d
        return push_subscription

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
