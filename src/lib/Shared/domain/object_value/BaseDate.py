from dataclasses import dataclass
from datetime import datetime, timezone

from lib.Shared.domain.errors.DomainError import ValidationError


@dataclass(frozen=True)
class BaseDate:
    value: datetime

    def __post_init__(self):
        if not isinstance(self.value, datetime):
            raise ValidationError("Value must be a datetime")

        if self.value.tzinfo is not None:
            object.__setattr__(self, "value", self.value.replace(tzinfo=None))

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        if self.value > now:
            raise ValidationError(f"Date cannot be in the future: {self.value}")

    @staticmethod
    def _is_valid_date(date: datetime) -> bool:
        return isinstance(date, datetime)

    @classmethod
    def now(cls) -> "BaseDate":
        return cls(datetime.now().replace(tzinfo=None))

    @classmethod
    def from_timestamp(cls, timestamp: float) -> "BaseDate":
        return cls(datetime.fromtimestamp(timestamp).replace(tzinfo=None))

    def to_iso_string(self) -> str:
        return self.value.isoformat()

    def to_timestamp(self) -> float:
        return self.value.timestamp()

    def equals(self, other: "BaseDate") -> bool:
        return self.value == other.value

    def get_formated(self) -> str:
        return self.value.strftime("%Y-%m-%d %H:%M:%S")
