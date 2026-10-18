from enum import StrEnum


class SearchGuildMessagesSort(StrEnum):
    NEWEST = "newest"
    OLDEST = "oldest"

    def __str__(self) -> str:
        return str(self.value)
