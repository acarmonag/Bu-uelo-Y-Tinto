from dataclasses import dataclass

from lib.Shared.domain.errors.DomainError import NotFoundError
from lib.Shared.domain.result.BaseCommandResult import BaseCommandResult


@dataclass
class DeleteResult(BaseCommandResult):
    """Result class for delete operations"""
    should_raise_error: bool = True
    model_name: str = "Resource"

    def __post_init__(self):
        if self.should_raise_error and self.affected_rows <= 0:
            self.set_status(404)
            raise NotFoundError(f"{self.model_name} not found")

        super().__post_init__()
