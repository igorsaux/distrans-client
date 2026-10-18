from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WebhookToken")


@_attrs_define
class WebhookToken:
    """The create-only response of `POST /api/channels/{channel_id}/webhooks`. The plaintext `token` is shown exactly once
    and never returned again (list/get never include it); only its sha256 is stored.

        Attributes:
            id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
            token (str): base64url (no padding) execute token. Present it in the path of `POST
                /api/webhooks/{webhook_id}/{token}`.
    """

    id: str
    token: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        token = self.token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "token": token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        token = d.pop("token")

        webhook_token = cls(
            id=id,
            token=token,
        )

        webhook_token.additional_properties = d
        return webhook_token

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
