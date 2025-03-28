from dataclasses import dataclass
import re
from lib.Shared.domain.errors.DomainError import ValidationError


pattern = r"^[A-Za-z0-9 ]{2,100}$"


@dataclass(frozen=True)
class BaseName:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise ValidationError("Value must be a string")
        if not self.value.strip():
            raise ValidationError("Name cannot be empty")
        if len(self.value) > 100:
            raise ValidationError("Name cannot be longer than 100 characters")
        if not self._is_valid_name(self.value):
            raise ValidationError(f"Invalid name format: {self.value}")

        object.__setattr__(self, "value", self.value.strip())

    @staticmethod
    def _is_valid_name(name: str) -> bool:
        return bool(re.match(pattern, name))

    @staticmethod
    def get_pattern() -> str:
        return pattern

    def __eq__(self, other):
        if not isinstance(other, BaseName):
            return NotImplemented
        return self.value.lower() == other.value.lower()

    def equals(self, other: "BaseName") -> bool:
        return self.value == other.value
