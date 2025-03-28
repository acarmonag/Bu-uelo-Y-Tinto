import re
from dataclasses import dataclass
from bson import ObjectId

from lib.Shared.domain.errors.DomainError import ValidationError

pattern = r"^[0-9a-fA-F]{24}$"


@dataclass(frozen=True)
class BaseMongoId:
    value: ObjectId

    def __post_init__(self):
        if not isinstance(self.value, ObjectId):
            raise ValidationError("Value must be a MongoDB ObjectId")

    def equals(self, other: "BaseMongoId") -> bool:
        return self.value == other.value

    @staticmethod
    def get_pattern() -> str:
        return pattern
