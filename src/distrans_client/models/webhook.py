from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Webhook")


@_attrs_define
class Webhook:
    """A per-channel webhook. It carries no owner: management is gated purely by the channel's `create_webhooks` /
    `modify_webhooks` / `delete_webhooks` permissions. The execute token is never included.

        Attributes:
            id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
            guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
            channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
            name (str): Max `api.webhooks.max_name_codepoints`; forbidden codepoints are rejected with 400 "'name' is
                invalid".
            avatar_hash (None | str): Hex XXHash64 of the stored WebP avatar (16 lowercase hex chars); null when unset.
            created_at (int): Unix epoch, milliseconds.
            deleted_at (int | None): Set when the webhook is soft-deleted. A deleted webhook is gone for management/execute
                (404) but still returned by `GET /api/webhooks/{webhook_id}` so its messages keep rendering name/avatar.
    """

    id: str
    guild_id: str
    channel_id: str
    name: str
    avatar_hash: None | str
    created_at: int
    deleted_at: int | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        guild_id = self.guild_id

        channel_id = self.channel_id

        name = self.name

        avatar_hash: None | str
        avatar_hash = self.avatar_hash

        created_at = self.created_at

        deleted_at: int | None
        deleted_at = self.deleted_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "guild_id": guild_id,
                "channel_id": channel_id,
                "name": name,
                "avatar_hash": avatar_hash,
                "created_at": created_at,
                "deleted_at": deleted_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        guild_id = d.pop("guild_id")

        channel_id = d.pop("channel_id")

        name = d.pop("name")

        def _parse_avatar_hash(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        avatar_hash = _parse_avatar_hash(d.pop("avatar_hash"))

        created_at = d.pop("created_at")

        def _parse_deleted_at(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        deleted_at = _parse_deleted_at(d.pop("deleted_at"))

        webhook = cls(
            id=id,
            guild_id=guild_id,
            channel_id=channel_id,
            name=name,
            avatar_hash=avatar_hash,
            created_at=created_at,
            deleted_at=deleted_at,
        )

        webhook.additional_properties = d
        return webhook

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
