from abc import ABC
from dataclasses import dataclass
from typing import Dict, Any, ClassVar, List

from lib.Shared.domain.errors.DomainError import BadRequestError
from lib.Shared.domain.specification.BaseCommand import BaseCommand


@dataclass
class BaseUpdateCommand(BaseCommand):
    """Base class for update commands"""
    _required_fields: ClassVar[List[str]] = ["id"]

    def __post_init__(self):
        optional_fields = [field for field in self.__dict__ if field != 'cmd']

        if all(self.__dict__[field] is None for field in optional_fields):
            raise BadRequestError("At least one field is required")
        super().__post_init__()

    def to_dict(self) -> Dict[str, Any]:
        """Convert update command to dictionary, handling value objects"""
        res = super().to_dict()
        if hasattr(self, 'id'):
            res['id'] = self.id.value if hasattr(self.id, 'value') else self.id
        return res
