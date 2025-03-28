from src.lib.Order.domain.Order import Order
from src.lib.Order.domain.OrderSpecification import OrderCommandCreate
from src.lib.Order.domain.OrderRepository import OrderRepository
from src.lib.Shared.domain.errors.DomainError import ValidationError


class OrderCreator:
    """Application service responsible for creating new orders.
    
    This class implements the use case for order creation, following the
    Command pattern. It orchestrates the validation and persistence of new orders.
    
    Attributes:
        repository: OrderRepository instance for data persistence
    """
    
    def __init__(self, repository: OrderRepository):
        """Initialize the OrderCreator with a repository.
        
        Args:
            repository: OrderRepository instance for data persistence
        """
        self.repository = repository
    
    def execute(self, command: OrderCommandCreate) -> Order:
        """Executes the order creation use case.
        
        This method follows a two-step process:
        1. Validates the input command
        2. Persists the command through the repository
        
        Args:
            command: OrderCommandCreate DTO containing the order data
            
        Returns:
            Order: The newly created and persisted order entity
            
        Raises:
            ValidationError: If the command data is invalid
            RepositoryError: If there's an error during persistence
        """
        # 1. Validate command
        errors = command.validate()
        if errors:
            raise ValidationError(', '.join(errors))
        
        # 2. Save to repository
        saved_order = self.repository.create(command)
        
        return saved_order 