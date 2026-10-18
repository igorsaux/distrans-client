from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LimitsMessages")


@_attrs_define
class LimitsMessages:
    """
    Attributes:
        max_messages_limit (int):
        max_codepoints_per_message (int):
        max_reactions (int):
        max_reactions_users_limit (int):
        max_embeds (int):
        max_attachments (int):
        max_mention_users (int):
        max_mention_roles (int):
        max_allowed_mention_users (int):
        max_allowed_mention_roles (int):
    """

    max_messages_limit: int
    max_codepoints_per_message: int
    max_reactions: int
    max_reactions_users_limit: int
    max_embeds: int
    max_attachments: int
    max_mention_users: int
    max_mention_roles: int
    max_allowed_mention_users: int
    max_allowed_mention_roles: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_messages_limit = self.max_messages_limit

        max_codepoints_per_message = self.max_codepoints_per_message

        max_reactions = self.max_reactions

        max_reactions_users_limit = self.max_reactions_users_limit

        max_embeds = self.max_embeds

        max_attachments = self.max_attachments

        max_mention_users = self.max_mention_users

        max_mention_roles = self.max_mention_roles

        max_allowed_mention_users = self.max_allowed_mention_users

        max_allowed_mention_roles = self.max_allowed_mention_roles

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "max_messages_limit": max_messages_limit,
                "max_codepoints_per_message": max_codepoints_per_message,
                "max_reactions": max_reactions,
                "max_reactions_users_limit": max_reactions_users_limit,
                "max_embeds": max_embeds,
                "max_attachments": max_attachments,
                "max_mention_users": max_mention_users,
                "max_mention_roles": max_mention_roles,
                "max_allowed_mention_users": max_allowed_mention_users,
                "max_allowed_mention_roles": max_allowed_mention_roles,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        max_messages_limit = d.pop("max_messages_limit")

        max_codepoints_per_message = d.pop("max_codepoints_per_message")

        max_reactions = d.pop("max_reactions")

        max_reactions_users_limit = d.pop("max_reactions_users_limit")

        max_embeds = d.pop("max_embeds")

        max_attachments = d.pop("max_attachments")

        max_mention_users = d.pop("max_mention_users")

        max_mention_roles = d.pop("max_mention_roles")

        max_allowed_mention_users = d.pop("max_allowed_mention_users")

        max_allowed_mention_roles = d.pop("max_allowed_mention_roles")

        limits_messages = cls(
            max_messages_limit=max_messages_limit,
            max_codepoints_per_message=max_codepoints_per_message,
            max_reactions=max_reactions,
            max_reactions_users_limit=max_reactions_users_limit,
            max_embeds=max_embeds,
            max_attachments=max_attachments,
            max_mention_users=max_mention_users,
            max_mention_roles=max_mention_roles,
            max_allowed_mention_users=max_allowed_mention_users,
            max_allowed_mention_roles=max_allowed_mention_roles,
        )

        limits_messages.additional_properties = d
        return limits_messages

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
