from enum import StrEnum


class ChannelKind(StrEnum):
    CATEGORY = "category"
    CHANNEL = "channel"

    def __str__(self) -> str:
        return str(self.value)
