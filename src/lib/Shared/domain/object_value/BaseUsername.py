import re
from dataclasses import dataclass
from lib.Shared.domain.errors.DomainError import ValidationError

username_pattern = r"^[a-zA-Z0-9._-]{3,30}$"


@dataclass(frozen=True)
class BaseUsername:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise ValidationError("Value must be a string")
        if not re.match(r'^[a-zA-Z0-9_-]{3,20}$', self.value):
            raise ValidationError("Username must be between 3 and 20 characters and can only contain letters, numbers, underscores and hyphens")

        cleaned = self.value.strip()
        if not self._is_valid_username(cleaned):
            raise ValidationError(f"Invalid username format: {self.value}")

        object.__setattr__(self, "value", cleaned)

    @staticmethod
    def _is_valid_username(username: str) -> bool:
        if not bool(re.match(username_pattern, username)):
            return False

        if username[0] in "._-" or username[-1] in "._-":
            return False

        if any(x in username for x in ["__", "--", "..", "_.", "._", "-.", ".-", "_-", "-_"]):
            return False

        return True

    @staticmethod
    def get_pattern() -> str:
        return username_pattern

    def equals(self, other: "BaseUsername") -> bool:
        return self.value == other.value
