from dataclasses import dataclass

from src.lib.Shared.domain.object_value.BaseUUID import BaseUUID
from src.lib.Shared.domain.object_value.BaseName import BaseName
from src.lib.Shared.domain.object_value.BaseDate import BaseDate
from src.lib.Shared.domain.object_value.BaseFloat import BaseFloat
from src.lib.Order.domain.DeliveryLocation import DeliveryLocation
from src.lib.Shared.domain.errors.DomainError import ValidationError


@dataclass
class Order:
    """Domain entity representing an order.
    
    This entity represents a customer's order with its status and delivery details.
    
    Attributes:
        id: Unique identifier for the order
        customer_name: Name of the customer who placed the order
        order_status_name: Name of the current order status
        delivery_location: Location where the order should be delivered
        total: Total amount of the order
        created_at: Timestamp when the order was created
        updated_at: Timestamp when the order was last updated
        deleted_at: Timestamp when the order was deleted (if applicable)
    """
    id: BaseUUID
    customer_name: BaseName
    order_status_name: BaseName
    delivery_location: DeliveryLocation
    total: BaseFloat
    created_at: BaseDate
    updated_at: BaseDate
    deleted_at: BaseDate
    
    def __post_init__(self):
        """Validates the integrity of the order entity."""
        self._validate()
    
    def _validate(self):
        """Validates the business rules of the order.
        
        Raises:
            ValidationError: If any business rule is violated
        """
        if self.created_at.value > self.updated_at.value:
            raise ValidationError("Created date cannot be after updated date")
            
        if self.deleted_at and self.deleted_at.value < self.created_at.value:
            raise ValidationError("Deleted date cannot be before created date")
            
        if self.total < 0:
            raise ValidationError("Total amount cannot be negative") 