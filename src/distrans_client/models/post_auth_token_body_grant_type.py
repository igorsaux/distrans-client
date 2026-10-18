from enum import StrEnum


class PostAuthTokenBodyGrantType(StrEnum):
    PASSWORD = "password"

    def __str__(self) -> str:
        return str(self.value)
