from src.lib.Order.domain.Order import Order
from src.lib.Order.domain.OrderRepository import OrderRepository
from src.lib.Order.domain.OrderSpecification import OrderCommandUpdate
from src.lib.Shared.domain.errors.DomainError import ValidationError, NotFoundError


class OrderUpdater:
    """Application service responsible for updating orders.
    
    This class implements the use case for order updates, following the
    Command pattern. It orchestrates the validation and persistence of
    order updates.
    
    Attributes:
        repository: OrderRepository instance for data persistence
    """
    
    def __init__(self, repository: OrderRepository):
        """Initialize the OrderUpdater with a repository.
        
        Args:
            repository: OrderRepository instance for data persistence
        """
        self.repository = repository
    
    def execute(self, command: OrderCommandUpdate) -> Order:
        """Executes the order update use case.
        
        This method follows a three-step process:
        1. Validates the update command
        2. Retrieves the existing order
        3. Updates and persists the order
        
        Args:
            command: OrderCommandUpdate object containing the update data
            
        Returns:
            Order: The updated order entity
            
        Raises:
            ValidationError: If the update command is invalid
            NotFoundError: If the order doesn't exist
            RepositoryError: If there's an error during persistence
        """
        # 1. Validate command
        errors = command.validate()
        if errors:
            raise ValidationError(', '.join(errors))
        
        # 2. Get existing order
        existing_order = self.repository.find_by_id(command.id)
        if not existing_order:
            raise NotFoundError(f"Order with ID {command.id} not found")
        
        # 3. Update order
        updated_order = existing_order.update(
            name=command.name,
            email=command.email,
            phone=command.phone
        )
        
        # 4. Persist changes
        return self.repository.update(updated_order) 