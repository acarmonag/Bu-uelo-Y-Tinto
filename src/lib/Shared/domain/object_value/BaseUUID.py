from dataclasses import dataclass
import uuid
from typing import Optional

from lib.Shared.domain.errors.DomainError import ValidationError

@dataclass(frozen=True)
class BaseUUID:
    """Value object for PostgreSQL UUID type"""
    value: uuid.UUID

    def __post_init__(self):
        """Validate UUID value"""
        if not isinstance(self.value, uuid.UUID):
            raise ValidationError("Value must be a UUID")

    @classmethod
    def generate(cls) -> 'BaseUUID':
        """Generate a new random UUID"""
        return cls(uuid.uuid4())

    @classmethod
    def from_string(cls, value: str) -> 'BaseUUID':
        """Create UUID from string representation"""
        try:
            return cls(uuid.UUID(value))
        except ValueError:
            raise ValidationError(f"Invalid UUID string format: {value}")

    @classmethod
    def from_bytes(cls, value: bytes) -> 'BaseUUID':
        """Create UUID from bytes"""
        try:
            return cls(uuid.UUID(bytes=value))
        except ValueError:
            raise ValidationError("Invalid UUID bytes format")

    def to_string(self) -> str:
        """Convert UUID to string representation"""
        return str(self.value)

    def to_bytes(self) -> bytes:
        """Convert UUID to bytes"""
        return self.value.bytes

    def __eq__(self, other) -> bool:
        """Compare two UUIDs"""
        if not isinstance(other, BaseUUID):
            return NotImplemented
        return self.value == other.value

    def equals(self, other: 'BaseUUID') -> bool:
        """Compare two UUIDs (case-sensitive)"""
        return self.value == other.value

    def is_nil(self) -> bool:
        """Check if UUID is nil (all zeros)"""
        return self.value == uuid.UUID('00000000-0000-0000-0000-000000000000')

    def version(self) -> int:
        """Get UUID version (1-5)"""
        return self.value.version

    def variant(self) -> str:
        """Get UUID variant"""
        return str(self.value.variant)

    def hex(self) -> str:
        """Get UUID as 32-character hexadecimal string"""
        return self.value.hex

    def int(self) -> int:
        """Get UUID as integer"""
        return self.value.int