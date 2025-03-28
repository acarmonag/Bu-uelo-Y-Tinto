from abc import ABC
from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional
from datetime import datetime, UTC

from lib.Shared.domain.errors.DomainError import ValidationError
from lib.Shared.domain.object_value.BaseDate import BaseDate

T = TypeVar('T')


@dataclass
class BaseEntity(Generic[T], ABC):
    """Base class for all domain entities
    
    Attributes:
        id: Unique identifier of the entity (required)
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: T
    created_at: BaseDate
    updated_at: BaseDate

    def __post_init__(self):
        """Validate entity after initialization"""
        self._validate_dates()
        self._validate_id()

    def _validate_dates(self) -> None:
        """Validate date fields"""
        if self.created_at.value > self.updated_at.value:
            raise ValidationError("Created date cannot be after updated date")

    def _validate_id(self) -> None:
        """Validate ID field is not None"""
        if self.id is None:
            raise ValidationError("ID cannot be None")
