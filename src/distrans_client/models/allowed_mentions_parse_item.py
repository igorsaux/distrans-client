from enum import StrEnum


class AllowedMentionsParseItem(StrEnum):
    EVERYONE = "everyone"
    ROLES = "roles"
    USERS = "users"

    def __str__(self) -> str:
        return str(self.value)
