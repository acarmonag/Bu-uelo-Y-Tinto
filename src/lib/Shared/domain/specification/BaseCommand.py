from abc import ABC
from dataclasses import dataclass
from typing import Dict, Any, ClassVar, List


@dataclass
class BaseCommand(ABC):
    """Base class for all domain commands"""
    _required_fields: ClassVar[List[str]] = []

    def __post_init__(self):
        """Validate required fields"""
        for field_name in self._required_fields:
            if not getattr(self, field_name):
                raise ValueError(f"{field_name} is required")

    def to_dict(self) -> Dict[str, Any]:
        """Convert command to dictionary, handling value objects"""
        res = {}
        for key, value in self.__dict__.items():
            if value is not None:
                res[key] = value.value if hasattr(value, 'value') else value
        return res
