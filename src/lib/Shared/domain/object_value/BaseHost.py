import ipaddress
import re
from dataclasses import dataclass
from lib.Shared.domain.errors.DomainError import ValidationError

host_pattern = r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$|^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$"


@dataclass(frozen=True)
class BaseHost:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise ValidationError("Value must be a string")
        if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9](?:\.[a-zA-Z]{2,})+$', self.value):
            raise ValidationError("Invalid hostname format")

        cleaned = self.value.strip()
        if not self._is_valid_host(cleaned):
            raise ValidationError(f"Invalid host format: {self.value}")

        object.__setattr__(self, "value", cleaned)

    @staticmethod
    def _is_valid_host(host: str) -> bool:
        if not bool(re.match(host_pattern, host)):
            return False

        # Para IPs, hacer validación adicional
        if all(c.isdigit() or c == '.' for c in host):
            try:
                ipaddress.ip_address(host)
                return True
            except ValueError:
                return False

        return True  # Es un nombre de dominio válido según regex

    @staticmethod
    def get_pattern() -> str:
        return host_pattern

    def equals(self, other: "BaseHost") -> bool:
        return self.value == other.value
