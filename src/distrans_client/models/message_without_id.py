from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.attachment import Attachment
    from ..models.embed import Embed
    from ..models.reaction_summary import ReactionSummary


T = TypeVar("T", bound="MessageWithoutId")


@_attrs_define
class MessageWithoutId:
    """
    Attributes:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        author_id (None | str): Author user id; null for a webhook message (which carries `webhook_id` instead).
            `author_id` and `webhook_id` are mutually exclusive.
        webhook_id (None | str): Webhook id when the message was posted by a webhook; null for a user message. Use `GET
            /api/webhooks/{webhook_id}` to resolve its name/avatar.
        content (str): Sanitized message body (forbidden codepoints stripped on receipt)
        created_at (int): Unix epoch, milliseconds
        reply_to_id (None | str):
        edited_at (int | None): Unix epoch, milliseconds
        embeds (list[Embed] | None): Null (absent) when the message has no embeds. The server serializes unset optional
            embed fields as explicit nulls and always emits `fields` as an array.
        attachments (list[Attachment]): Ordered attachments of the message; an empty array when there are none.
        mention_everyone (bool): True when the content contains `@everyone`/`@here` and it was left enabled by
            `allowed_mentions`.
        mentions (list[str]): User ids mentioned in the content (`<@id>` / `<@!id>`), in first-appearance order,
            deduplicated. Ids of missing or deleted users are dropped.
        mention_roles (list[str]): Role ids mentioned in the content (`<@&id>`) that belong to the message's guild, in
            first-appearance order, deduplicated.
        pinned (bool): True when the message is pinned in its channel.
        reactions (list[ReactionSummary] | None): Inline aggregated reactions of the message, ordered by the first time
            each emoji was used; null when the message has none. `me` is caller-specific.
    """

    channel_id: str
    author_id: None | str
    webhook_id: None | str
    content: str
    created_at: int
    reply_to_id: None | str
    edited_at: int | None
    embeds: list[Embed] | None
    attachments: list[Attachment]
    mention_everyone: bool
    mentions: list[str]
    mention_roles: list[str]
    pinned: bool
    reactions: list[ReactionSummary] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        channel_id = self.channel_id

        author_id: None | str
        author_id = self.author_id

        webhook_id: None | str
        webhook_id = self.webhook_id

        content = self.content

        created_at = self.created_at

        reply_to_id: None | str
        reply_to_id = self.reply_to_id

        edited_at: int | None
        edited_at = self.edited_at

        embeds: list[dict[str, Any]] | None
        if isinstance(self.embeds, list):
            embeds = []
            for embeds_type_0_item_data in self.embeds:
                embeds_type_0_item = embeds_type_0_item_data.to_dict()
                embeds.append(embeds_type_0_item)

        else:
            embeds = self.embeds

        attachments = []
        for attachments_item_data in self.attachments:
            attachments_item = attachments_item_data.to_dict()
            attachments.append(attachments_item)

        mention_everyone = self.mention_everyone

        mentions = self.mentions

        mention_roles = self.mention_roles

        pinned = self.pinned

        reactions: list[dict[str, Any]] | None
        if isinstance(self.reactions, list):
            reactions = []
            for reactions_type_0_item_data in self.reactions:
                reactions_type_0_item = reactions_type_0_item_data.to_dict()
                reactions.append(reactions_type_0_item)

        else:
            reactions = self.reactions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channel_id": channel_id,
                "author_id": author_id,
                "webhook_id": webhook_id,
                "content": content,
                "created_at": created_at,
                "reply_to_id": reply_to_id,
                "edited_at": edited_at,
                "embeds": embeds,
                "attachments": attachments,
                "mention_everyone": mention_everyone,
                "mentions": mentions,
                "mention_roles": mention_roles,
                "pinned": pinned,
                "reactions": reactions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.attachment import Attachment
        from ..models.embed import Embed
        from ..models.reaction_summary import ReactionSummary

        d = dict(src_dict)
        channel_id = d.pop("channel_id")

        def _parse_author_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        author_id = _parse_author_id(d.pop("author_id"))

        def _parse_webhook_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        webhook_id = _parse_webhook_id(d.pop("webhook_id"))

        content = d.pop("content")

        created_at = d.pop("created_at")

        def _parse_reply_to_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        reply_to_id = _parse_reply_to_id(d.pop("reply_to_id"))

        def _parse_edited_at(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        edited_at = _parse_edited_at(d.pop("edited_at"))

        def _parse_embeds(data: object) -> list[Embed] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                embeds_type_0 = []
                _embeds_type_0 = data
                for embeds_type_0_item_data in _embeds_type_0:
                    embeds_type_0_item = Embed.from_dict(embeds_type_0_item_data)

                    embeds_type_0.append(embeds_type_0_item)

                return embeds_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Embed] | None, data)

        embeds = _parse_embeds(d.pop("embeds"))

        attachments = []
        _attachments = d.pop("attachments")
        for attachments_item_data in _attachments:
            attachments_item = Attachment.from_dict(attachments_item_data)

            attachments.append(attachments_item)

        mention_everyone = d.pop("mention_everyone")

        mentions = cast(list[str], d.pop("mentions"))

        mention_roles = cast(list[str], d.pop("mention_roles"))

        pinned = d.pop("pinned")

        def _parse_reactions(data: object) -> list[ReactionSummary] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                reactions_type_0 = []
                _reactions_type_0 = data
                for reactions_type_0_item_data in _reactions_type_0:
                    reactions_type_0_item = ReactionSummary.from_dict(
                        reactions_type_0_item_data
                    )

                    reactions_type_0.append(reactions_type_0_item)

                return reactions_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ReactionSummary] | None, data)

        reactions = _parse_reactions(d.pop("reactions"))

        message_without_id = cls(
            channel_id=channel_id,
            author_id=author_id,
            webhook_id=webhook_id,
            content=content,
            created_at=created_at,
            reply_to_id=reply_to_id,
            edited_at=edited_at,
            embeds=embeds,
            attachments=attachments,
            mention_everyone=mention_everyone,
            mentions=mentions,
            mention_roles=mention_roles,
            pinned=pinned,
            reactions=reactions,
        )

        message_without_id.additional_properties = d
        return message_without_id

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
