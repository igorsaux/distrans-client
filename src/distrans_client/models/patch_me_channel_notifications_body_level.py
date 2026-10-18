from enum import StrEnum


class PatchMeChannelNotificationsBodyLevel(StrEnum):
    ALL_MESSAGES = "all_messages"
    INHERIT = "inherit"
    NOTHING = "nothing"
    ONLY_MENTIONS = "only_mentions"

    def __str__(self) -> str:
        return str(self.value)
