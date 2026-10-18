from enum import StrEnum


class GuildSyncOverwritesItemType(StrEnum):
    MEMBER = "member"
    ROLE = "role"

    def __str__(self) -> str:
        return str(self.value)
