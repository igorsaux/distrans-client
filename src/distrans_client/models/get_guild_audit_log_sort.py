from enum import StrEnum


class GetGuildAuditLogSort(StrEnum):
    NEWEST = "newest"
    OLDEST = "oldest"

    def __str__(self) -> str:
        return str(self.value)
