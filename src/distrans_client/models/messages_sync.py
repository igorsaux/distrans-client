from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MessagesSync")


@_attrs_define
class MessagesSync:
    """
    Attributes:
        updated_at (int): Server cursor: the database `now()` captured at query start, in epoch milliseconds. Store it
            and pass it as the next `since`.
        messages (list[str]):
    """

    updated_at: int
    messages: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        updated_at = self.updated_at

        messages = self.messages

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "updated_at": updated_at,
                "messages": messages,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        updated_at = d.pop("updated_at")

        messages = cast(list[str], d.pop("messages"))

        messages_sync = cls(
            updated_at=updated_at,
            messages=messages,
        )

        messages_sync.additional_properties = d
        return messages_sync

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
