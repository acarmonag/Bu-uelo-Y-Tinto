from abc import ABC, abstractmethod

from src.lib.Order.domain.Order import Order
from src.lib.Order.domain.OrderSpecification import OrderCommandCreate, OrderCriteriaFind, OrderPaginatedResponse


class OrderRepository(ABC):
    """Repository interface for Order persistence operations.
    
    This interface defines the contract for Order persistence operations,
    following the Repository pattern. It provides methods for CRUD operations
    and querying orders.
    """
    
    @abstractmethod
    def create(self, command: OrderCommandCreate) -> Order:
        """Creates a new order in the repository.
        
        Args:
            command: OrderCommandCreate DTO containing the order data
            
        Returns:
            Order: The newly created order entity
            
        Raises:
            RepositoryError: If there's an error during the creation process
        """
        pass
    
    @abstractmethod
    def save(self, order: Order) -> Order:
        """Saves a new order to the repository.
        
        Args:
            order: Order entity to save
            
        Returns:
            Order: The saved order with any generated IDs
            
        Raises:
            RepositoryError: If there's an error during save
        """
        pass
    
    @abstractmethod
    def update(self, order: Order) -> Order:
        """Updates an existing order in the repository.
        
        Args:
            order: Order entity to update
            
        Returns:
            Order: The updated order
            
        Raises:
            RepositoryError: If there's an error during update
            OrderNotFoundError: If the order doesn't exist
        """
        pass
    
    @abstractmethod
    def find(self, criteria: OrderCriteriaFind) -> OrderPaginatedResponse:
        """Finds orders based on search criteria.
        
        Args:
            criteria: OrderCriteriaFind object containing search parameters
            
        Returns:
            OrderPaginatedResponse: Paginated response with matching orders
            
        Raises:
            RepositoryError: If there's an error during retrieval
        """
        pass