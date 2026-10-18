from enum import StrEnum


class AuditLogEntryAction(StrEnum):
    CHANNEL_CREATE = "channel_create"
    CHANNEL_DELETE = "channel_delete"
    CHANNEL_NAME_UPDATE = "channel_name_update"
    CHANNEL_PARENT_UPDATE = "channel_parent_update"
    CHANNEL_REORDER = "channel_reorder"
    CHANNEL_TOPIC_UPDATE = "channel_topic_update"
    EMOJI_CREATE = "emoji_create"
    EMOJI_DELETE = "emoji_delete"
    EMOJI_ICON_UPDATE = "emoji_icon_update"
    EMOJI_NAME_UPDATE = "emoji_name_update"
    GUILD_AVATAR_DELETE = "guild_avatar_delete"
    GUILD_AVATAR_UPDATE = "guild_avatar_update"
    GUILD_NAME_UPDATE = "guild_name_update"
    MEMBER_OVERWRITE_UPDATE = "member_overwrite_update"
    MESSAGE_DELETE = "message_delete"
    MESSAGE_PIN = "message_pin"
    MESSAGE_UNPIN = "message_unpin"
    ROLE_COLOR_UPDATE = "role_color_update"
    ROLE_CREATE = "role_create"
    ROLE_DELETE = "role_delete"
    ROLE_GRANT = "role_grant"
    ROLE_MENTIONABLE_UPDATE = "role_mentionable_update"
    ROLE_NAME_UPDATE = "role_name_update"
    ROLE_OVERWRITE_UPDATE = "role_overwrite_update"
    ROLE_PERMISSIONS_UPDATE = "role_permissions_update"
    ROLE_REORDER = "role_reorder"
    ROLE_REVOKE = "role_revoke"
    WEBHOOK_AVATAR_DELETE = "webhook_avatar_delete"
    WEBHOOK_AVATAR_UPDATE = "webhook_avatar_update"
    WEBHOOK_CREATE = "webhook_create"
    WEBHOOK_DELETE = "webhook_delete"
    WEBHOOK_NAME_UPDATE = "webhook_name_update"

    def __str__(self) -> str:
        return str(self.value)
