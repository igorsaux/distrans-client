from enum import StrEnum


class OverwriteType(StrEnum):
    MEMBER = "member"
    ROLE = "role"

    def __str__(self) -> str:
        return str(self.value)
