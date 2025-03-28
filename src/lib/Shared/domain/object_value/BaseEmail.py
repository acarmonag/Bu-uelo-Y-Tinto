from dataclasses import dataclass
import re
from lib.Shared.domain.errors.DomainError import ValidationError


pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


@dataclass(frozen=True)
class BaseEmail:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise ValidationError("Value must be a string")
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.value):
            raise ValidationError("Invalid email format")

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        return bool(re.match(pattern, email))

    @staticmethod
    def get_pattern() -> str:
        return pattern

    def equals(self, other: "BaseEmail") -> bool:
        return self.value == other.value
