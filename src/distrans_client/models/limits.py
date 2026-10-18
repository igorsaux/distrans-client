from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.limits_audit_log import LimitsAuditLog
    from ..models.limits_auth import LimitsAuth
    from ..models.limits_channels import LimitsChannels
    from ..models.limits_embeds import LimitsEmbeds
    from ..models.limits_emojis import LimitsEmojis
    from ..models.limits_files import LimitsFiles
    from ..models.limits_guilds import LimitsGuilds
    from ..models.limits_media import LimitsMedia
    from ..models.limits_messages import LimitsMessages
    from ..models.limits_push import LimitsPush
    from ..models.limits_roles import LimitsRoles
    from ..models.limits_search import LimitsSearch
    from ..models.limits_sync import LimitsSync
    from ..models.limits_users import LimitsUsers
    from ..models.limits_webhooks import LimitsWebhooks


T = TypeVar("T", bound="Limits")


@_attrs_define
class Limits:
    """
    Attributes:
        guilds (LimitsGuilds):
        channels (LimitsChannels):
        messages (LimitsMessages):
        search (LimitsSearch):
        sync (LimitsSync):
        audit_log (LimitsAuditLog):
        embeds (LimitsEmbeds):
        roles (LimitsRoles):
        emojis (LimitsEmojis):
        users (LimitsUsers):
        auth (LimitsAuth):
        media (LimitsMedia):
        files (LimitsFiles):
        push (LimitsPush): Browser Web Push availability. When `enabled` is false the subscription endpoints still store
            rows but no notification is delivered. `vapid_public_key` is the base64url `applicationServerKey` the client
            passes to `PushManager.subscribe`.
        webhooks (LimitsWebhooks):
    """

    guilds: LimitsGuilds
    channels: LimitsChannels
    messages: LimitsMessages
    search: LimitsSearch
    sync: LimitsSync
    audit_log: LimitsAuditLog
    embeds: LimitsEmbeds
    roles: LimitsRoles
    emojis: LimitsEmojis
    users: LimitsUsers
    auth: LimitsAuth
    media: LimitsMedia
    files: LimitsFiles
    push: LimitsPush
    webhooks: LimitsWebhooks
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        guilds = self.guilds.to_dict()

        channels = self.channels.to_dict()

        messages = self.messages.to_dict()

        search = self.search.to_dict()

        sync = self.sync.to_dict()

        audit_log = self.audit_log.to_dict()

        embeds = self.embeds.to_dict()

        roles = self.roles.to_dict()

        emojis = self.emojis.to_dict()

        users = self.users.to_dict()

        auth = self.auth.to_dict()

        media = self.media.to_dict()

        files = self.files.to_dict()

        push = self.push.to_dict()

        webhooks = self.webhooks.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "guilds": guilds,
                "channels": channels,
                "messages": messages,
                "search": search,
                "sync": sync,
                "audit_log": audit_log,
                "embeds": embeds,
                "roles": roles,
                "emojis": emojis,
                "users": users,
                "auth": auth,
                "media": media,
                "files": files,
                "push": push,
                "webhooks": webhooks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.limits_audit_log import LimitsAuditLog
        from ..models.limits_auth import LimitsAuth
        from ..models.limits_channels import LimitsChannels
        from ..models.limits_embeds import LimitsEmbeds
        from ..models.limits_emojis import LimitsEmojis
        from ..models.limits_files import LimitsFiles
        from ..models.limits_guilds import LimitsGuilds
        from ..models.limits_media import LimitsMedia
        from ..models.limits_messages import LimitsMessages
        from ..models.limits_push import LimitsPush
        from ..models.limits_roles import LimitsRoles
        from ..models.limits_search import LimitsSearch
        from ..models.limits_sync import LimitsSync
        from ..models.limits_users import LimitsUsers
        from ..models.limits_webhooks import LimitsWebhooks

        d = dict(src_dict)
        guilds = LimitsGuilds.from_dict(d.pop("guilds"))

        channels = LimitsChannels.from_dict(d.pop("channels"))

        messages = LimitsMessages.from_dict(d.pop("messages"))

        search = LimitsSearch.from_dict(d.pop("search"))

        sync = LimitsSync.from_dict(d.pop("sync"))

        audit_log = LimitsAuditLog.from_dict(d.pop("audit_log"))

        embeds = LimitsEmbeds.from_dict(d.pop("embeds"))

        roles = LimitsRoles.from_dict(d.pop("roles"))

        emojis = LimitsEmojis.from_dict(d.pop("emojis"))

        users = LimitsUsers.from_dict(d.pop("users"))

        auth = LimitsAuth.from_dict(d.pop("auth"))

        media = LimitsMedia.from_dict(d.pop("media"))

        files = LimitsFiles.from_dict(d.pop("files"))

        push = LimitsPush.from_dict(d.pop("push"))

        webhooks = LimitsWebhooks.from_dict(d.pop("webhooks"))

        limits = cls(
            guilds=guilds,
            channels=channels,
            messages=messages,
            search=search,
            sync=sync,
            audit_log=audit_log,
            embeds=embeds,
            roles=roles,
            emojis=emojis,
            users=users,
            auth=auth,
            media=media,
            files=files,
            push=push,
            webhooks=webhooks,
        )

        limits.additional_properties = d
        return limits

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
