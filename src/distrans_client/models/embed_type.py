from enum import StrEnum


class EmbedType(StrEnum):
    RICH = "rich"

    def __str__(self) -> str:
        return str(self.value)
