import re
from dataclasses import dataclass

from lib.Shared.domain.errors.DomainError import ValidationError

mac_pattern = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$|^([0-9A-Fa-f]{4}\.){2}([0-9A-Fa-f]{4})$"


@dataclass(frozen=True)
class BaseMac:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise ValidationError("Value must be a string")
        if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', self.value):
            raise ValidationError("Invalid MAC address format")

        cleaned = self.value.strip().lower()
        if not self._is_valid_mac(cleaned):
            raise ValidationError(f"Invalid MAC address format: {self.value}")

        object.__setattr__(self, "value", cleaned)

    @staticmethod
    def _is_valid_mac(mac: str) -> bool:
        return bool(re.match(mac_pattern, mac))

    @staticmethod
    def get_pattern() -> str:
        return mac_pattern

    def equals(self, other: "BaseMac") -> bool:
        return self.value == other.value

    def to_canonical(self) -> str:
        mac_digits = re.sub(r'[:.-]', '', self.value)

        if len(mac_digits) == 12:
            return ':'.join(mac_digits[i:i + 2] for i in range(0, 12, 2))

        return self.value
