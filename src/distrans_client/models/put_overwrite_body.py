from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.put_overwrite_body_type import PutOverwriteBodyType

T = TypeVar("T", bound="PutOverwriteBody")


@_attrs_define
class PutOverwriteBody:
    """
    Attributes:
        target_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        type_ (PutOverwriteBodyType):
        allow (str): 128-bit permission mask as decimal string
        deny (str): 128-bit permission mask as decimal string
    """

    target_id: str
    type_: PutOverwriteBodyType
    allow: str
    deny: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target_id = self.target_id

        type_ = self.type_.value

        allow = self.allow

        deny = self.deny

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "target_id": target_id,
                "type": type_,
                "allow": allow,
                "deny": deny,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        target_id = d.pop("target_id")

        type_ = PutOverwriteBodyType(d.pop("type"))

        allow = d.pop("allow")

        deny = d.pop("deny")

        put_overwrite_body = cls(
            target_id=target_id,
            type_=type_,
            allow=allow,
            deny=deny,
        )

        put_overwrite_body.additional_properties = d
        return put_overwrite_body

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
