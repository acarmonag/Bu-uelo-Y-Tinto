from dataclasses import dataclass
from lib.Shared.domain.errors.DomainError import ValidationError

port_pattern = r"^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"


@dataclass(frozen=True)
class BasePort:
    value: int

    def __post_init__(self):
        if not isinstance(self.value, int):
            raise ValidationError("Value must be an integer")
        if not 1 <= self.value <= 65535:
            raise ValidationError("Port must be between 1 and 65535")

    @staticmethod
    def _is_valid_port(port: int) -> bool:
        return 1 <= port <= 65535

    @staticmethod
    def get_port_range() -> tuple:
        return (1, 65535)

    def equals(self, other: "BasePort") -> bool:
        return self.value == other.value
