from src.lib.Order.domain.OrderSpecification import OrderCriteriaFind, OrderPaginatedResponse
from src.lib.Order.domain.OrderRepository import OrderRepository
from src.lib.Shared.domain.errors.DomainError import ValidationError


class OrderFinder:
    """Application service responsible for finding orders.
    
    This class implements the use case for order search, following the
    Query pattern. It orchestrates the validation and retrieval of orders
    based on search criteria.
    
    Attributes:
        repository: OrderRepository instance for data retrieval
    """
    
    def __init__(self, repository: OrderRepository):
        """Initialize the OrderFinder with a repository.
        
        Args:
            repository: OrderRepository instance for data retrieval
        """
        self.repository = repository
    
    def execute(self, criteria: OrderCriteriaFind) -> OrderPaginatedResponse:
        """Executes the order search use case.
        
        This method follows a two-step process:
        1. Validates the search criteria
        2. Retrieves orders from the repository
        
        Args:
            criteria: OrderCriteriaFind object containing search parameters,
                     pagination, and sorting information
            
        Returns:
            OrderPaginatedResponse: A paginated response containing the matching
                                  orders and pagination metadata
            
        Raises:
            ValidationError: If the search criteria is invalid
            RepositoryError: If there's an error during retrieval
        """
        # 1. Validate criteria
        errors = criteria.validate()
        if errors:
            raise ValidationError(', '.join(errors))
        
        # 2. Find orders
        return self.repository.find(criteria) 