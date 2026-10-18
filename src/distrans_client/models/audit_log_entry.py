from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.audit_log_entry_action import AuditLogEntryAction

T = TypeVar("T", bound="AuditLogEntry")


@_attrs_define
class AuditLogEntry:
    """One audit-log entry. `target_id`, `target_user_id` and `channel_id` identify the target of the action and may be
    null depending on `action`: channel actions carry `channel_id`, role/emoji/webhook/message actions carry `target_id`
    (with `channel_id` for webhooks/messages), `role_overwrite_update` carries `channel_id` plus `target_id` (role) and
    `member_overwrite_update` carries `channel_id` plus `target_user_id` (member), role grant/revoke carry `target_id`
    (role) and `target_user_id` (member), and guild actions and the reorder actions carry neither.

        Attributes:
            id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
            actor_id (None | str):
            action (AuditLogEntryAction):
            target_id (None | str):
            target_user_id (None | str):
            channel_id (None | str):
            created_at (int): Unix epoch milliseconds.
    """

    id: str
    actor_id: None | str
    action: AuditLogEntryAction
    target_id: None | str
    target_user_id: None | str
    channel_id: None | str
    created_at: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        actor_id: None | str
        actor_id = self.actor_id

        action = self.action.value

        target_id: None | str
        target_id = self.target_id

        target_user_id: None | str
        target_user_id = self.target_user_id

        channel_id: None | str
        channel_id = self.channel_id

        created_at = self.created_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "actor_id": actor_id,
                "action": action,
                "target_id": target_id,
                "target_user_id": target_user_id,
                "channel_id": channel_id,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        def _parse_actor_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        actor_id = _parse_actor_id(d.pop("actor_id"))

        action = AuditLogEntryAction(d.pop("action"))

        def _parse_target_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        target_id = _parse_target_id(d.pop("target_id"))

        def _parse_target_user_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        target_user_id = _parse_target_user_id(d.pop("target_user_id"))

        def _parse_channel_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        channel_id = _parse_channel_id(d.pop("channel_id"))

        created_at = d.pop("created_at")

        audit_log_entry = cls(
            id=id,
            actor_id=actor_id,
            action=action,
            target_id=target_id,
            target_user_id=target_user_id,
            channel_id=channel_id,
            created_at=created_at,
        )

        audit_log_entry.additional_properties = d
        return audit_log_entry

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
