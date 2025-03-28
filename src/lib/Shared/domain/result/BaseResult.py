from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime, UTC

from lib.Shared.domain.errors.DomainError import DomainError


@dataclass
class BaseResult:
    """Base class for all domain operation results"""
    message: Optional[str] = None
    error: Optional[str] = None
    status: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))

    def set_status(self, status: int) -> None:
        """Set the status code"""
        if not 100 <= status <= 599:
            raise ValueError("Status code must be between 100 and 599")
        self.status = status

    def set_message(self, message: str) -> None:
        """Set the success message"""
        self.message = message
        self.error = None

    def set_error(self, error: str) -> None:
        """Set the error message"""
        self.error = error
        self.message = None

    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to the result"""
        self.metadata[key] = value

    def __post_init__(self) -> None:
        """Validate result after initialization"""
        if self.message is None and self.error is None:
            raise DomainError("At least one of the fields 'message' or 'error' must be filled")
