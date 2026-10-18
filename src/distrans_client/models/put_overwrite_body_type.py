from enum import StrEnum


class PutOverwriteBodyType(StrEnum):
    MEMBER = "member"
    ROLE = "role"

    def __str__(self) -> str:
        return str(self.value)
