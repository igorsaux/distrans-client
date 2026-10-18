from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetMeUserdataResponse200")


@_attrs_define
class GetMeUserdataResponse200:
    """
    Attributes:
        data (Any): The stored arbitrary JSON value, or null.
        updated_at (int | None): Unix epoch in milliseconds, or null.
    """

    data: Any
    updated_at: int | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data

        updated_at: int | None
        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        data = d.pop("data")

        def _parse_updated_at(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        updated_at = _parse_updated_at(d.pop("updated_at"))

        get_me_userdata_response_200 = cls(
            data=data,
            updated_at=updated_at,
        )

        get_me_userdata_response_200.additional_properties = d
        return get_me_userdata_response_200

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
