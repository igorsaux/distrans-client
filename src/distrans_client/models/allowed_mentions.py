from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.allowed_mentions_parse_item import AllowedMentionsParseItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="AllowedMentions")


@_attrs_define
class AllowedMentions:
    """Controls which mentions parsed from the message content take effect. It is validated against the presence of
    mentions in `content` (phantom ids are silently ignored) and never rewrites the content. `parse` is mutually
    exclusive with `users`/`roles`.

        Attributes:
            parse (list[AllowedMentionsParseItem] | Unset): Mention kinds to parse; an empty array suppresses every mention.
                Mutually exclusive with `users`/`roles`.
            users (list[str] | Unset): User ids allowed to be mentioned; at most `api.messages.max_allowed_mention_users`.
                Disables all other kinds.
            roles (list[str] | Unset): Role ids allowed to be mentioned; at most `api.messages.max_allowed_mention_roles`.
                Disables all other kinds.
    """

    parse: list[AllowedMentionsParseItem] | Unset = UNSET
    users: list[str] | Unset = UNSET
    roles: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        parse: list[str] | Unset = UNSET
        if not isinstance(self.parse, Unset):
            parse = []
            for parse_item_data in self.parse:
                parse_item = parse_item_data.value
                parse.append(parse_item)

        users: list[str] | Unset = UNSET
        if not isinstance(self.users, Unset):
            users = self.users

        roles: list[str] | Unset = UNSET
        if not isinstance(self.roles, Unset):
            roles = self.roles

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if parse is not UNSET:
            field_dict["parse"] = parse
        if users is not UNSET:
            field_dict["users"] = users
        if roles is not UNSET:
            field_dict["roles"] = roles

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        _parse = d.pop("parse", UNSET)
        parse: list[AllowedMentionsParseItem] | Unset = UNSET
        if _parse is not UNSET:
            parse = []
            for parse_item_data in _parse:
                parse_item = AllowedMentionsParseItem(parse_item_data)

                parse.append(parse_item)

        users = cast(list[str], d.pop("users", UNSET))

        roles = cast(list[str], d.pop("roles", UNSET))

        allowed_mentions = cls(
            parse=parse,
            users=users,
            roles=roles,
        )

        allowed_mentions.additional_properties = d
        return allowed_mentions

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
