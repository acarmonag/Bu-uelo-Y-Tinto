from abc import ABC
from dataclasses import dataclass
from typing import Dict, Any, TypeVar, Generic, Optional, ClassVar, List

from lib.Shared.domain.object_value.BaseDate import BaseDate

T = TypeVar('T')


@dataclass
class BaseCriteria(Generic[T], ABC):
    """Base class for all domain query criteria"""
    _required_fields: ClassVar[List[str]] = []

    id: Optional[T] = None
    created_at: Optional[BaseDate] = None

    def __post_init__(self):
        """Validate required fields"""
        for field_name in self._required_fields:
            if not getattr(self, field_name):
                raise ValueError(f"{field_name} is required")

    def to_dict(self) -> Dict[str, Any]:
        """Convert criteria to dictionary, handling value objects"""
        res = {}
        for key, value in self.__dict__.items():
            if key == "password":
                res[key] = value.encrypted_value.hex()
            elif value is not None:
                res[key] = value.value if hasattr(value, 'value') else value

        return res
