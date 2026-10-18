from enum import StrEnum


class GuildNotificationSettingsLevel(StrEnum):
    ALL_MESSAGES = "all_messages"
    NOTHING = "nothing"
    ONLY_MENTIONS = "only_mentions"

    def __str__(self) -> str:
        return str(self.value)
