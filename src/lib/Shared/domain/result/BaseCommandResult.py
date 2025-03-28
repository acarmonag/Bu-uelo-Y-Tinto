from dataclasses import dataclass, field
from typing import Optional

from lib.Shared.domain.result.BaseResult import BaseResult


@dataclass
class BaseCommandResult(BaseResult):
    """Base class for command operation results"""
    affected_rows: int = 0
    operation_type: str = field(default="unknown")
    resource_id: Optional[str] = None

    def set_affected_rows(self, affected_rows: int) -> None:
        """Set the number of affected rows"""
        if affected_rows < 0:
            raise ValueError("Affected rows cannot be negative")
        self.affected_rows = affected_rows

    def set_resource_id(self, resource_id: str) -> None:
        """Set the affected resource ID"""
        self.resource_id = resource_id

    def __post_init__(self) -> None:
        """Validate command result"""
        if self.affected_rows < 0:
            raise ValueError("Affected rows cannot be negative")
        super().__post_init__()
