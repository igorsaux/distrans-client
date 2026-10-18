from enum import StrEnum


class PostGuildChannelBodyKind(StrEnum):
    CATEGORY = "category"
    CHANNEL = "channel"

    def __str__(self) -> str:
        return str(self.value)
