from dataclasses import dataclass

from lib.Shared.domain.errors.DomainError import ValidationError


@dataclass(frozen=True)
class BaseBoolean:
    value: bool

    def __post_init__(self):
        if not isinstance(self.value, bool):
            raise ValidationError("Value must be a boolean")

    def equals(self, other: "BaseBoolean") -> bool:
        return self.value == other.value
