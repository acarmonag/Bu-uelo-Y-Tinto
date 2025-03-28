from dataclasses import dataclass

from src.lib.Shared.domain.object_value.BaseUUID import BaseUUID
from src.lib.Shared.domain.object_value.BaseName import BaseName
from src.lib.Shared.domain.object_value.BaseDescription import BaseDescription
from src.lib.Shared.domain.object_value.BaseDate import BaseDate
from src.lib.Shared.domain.errors.DomainError import ValidationError


@dataclass
class OrderStatus:
    """Domain entity representing an order status.
    
    This entity represents the different states an order can be in,
    such as 'pending', 'processing', 'completed', etc.
    
    Attributes:
        id: Unique identifier for the status
        name: Name of the status (e.g., 'pending', 'processing')
        description: Detailed description of what the status means
        created_at: Timestamp when the status was created
        updated_at: Timestamp when the status was last updated
        deleted_at: Timestamp when the status was deleted (if applicable)
    """
    id: BaseUUID
    name: BaseName
    description: BaseDescription
    created_at: BaseDate
    updated_at: BaseDate
    deleted_at: BaseDate
    
    def __post_init__(self):
        """Validates the integrity of the order status entity."""
        self._validate()
    
    def _validate(self):
        """Validates the business rules of the order status.
        
        Raises:
            ValidationError: If any business rule is violated
        """
        if self.created_at.value > self.updated_at.value:
            raise ValidationError("Created date cannot be after updated date")
            
        if self.deleted_at and self.deleted_at.value < self.created_at.value:
            raise ValidationError("Deleted date cannot be before created date") 