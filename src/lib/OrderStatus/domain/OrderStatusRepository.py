from abc import ABC, abstractmethod

from src.lib.OrderStatus.domain.OrderStatus import OrderStatus
from src.lib.OrderStatus.domain.OrderStatusSpecification import OrderStatusCommandCreate, OrderStatusCriteriaFind, OrderStatusPaginatedResponse


class OrderStatusRepository(ABC):
    """Abstract base class defining the contract for order status persistence operations.
    
    This repository interface follows the Repository pattern, providing a collection-like
    interface for accessing order status data while hiding the complexity of the underlying
    storage mechanism.
    """
    
    @abstractmethod
    def create(self, command: OrderStatusCommandCreate) -> OrderStatus:
        """Creates a new order status in the repository.
        
        Args:
            command: OrderStatusCommandCreate DTO containing the status data
            
        Returns:
            OrderStatus: The newly created order status entity
            
        Raises:
            RepositoryError: If there's an error during the creation process
        """
        pass
    
    @abstractmethod
    def find(self, criteria: OrderStatusCriteriaFind) -> OrderStatusPaginatedResponse:
        """Retrieves order statuses from the repository based on the provided criteria.
        
        Args:
            criteria: OrderStatusCriteriaFind object containing search parameters, pagination,
                     and sorting information
                     
        Returns:
            OrderStatusPaginatedResponse: A paginated response containing the matching statuses
                                        and pagination metadata
            
        Raises:
            RepositoryError: If there's an error during the search process
        """
        pass 