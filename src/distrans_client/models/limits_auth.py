from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.limits_auth_password import LimitsAuthPassword


T = TypeVar("T", bound="LimitsAuth")


@_attrs_define
class LimitsAuth:
    """
    Attributes:
        password (LimitsAuthPassword):
    """

    password: LimitsAuthPassword
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        password = self.password.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "password": password,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.limits_auth_password import LimitsAuthPassword

        d = dict(src_dict)
        password = LimitsAuthPassword.from_dict(d.pop("password"))

        limits_auth = cls(
            password=password,
        )

        limits_auth.additional_properties = d
        return limits_auth

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
