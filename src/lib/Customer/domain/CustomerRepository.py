from abc import ABC, abstractmethod

from src.lib.Customer.domain.Customer import Customer
from src.lib.Customer.domain.CustomerSpecification import CustomerCriteriaFind, CustomerPaginatedResponse


class CustomerRepository(ABC):
    """Abstract base class defining the contract for customer persistence operations.
    
    This repository interface follows the Repository pattern, providing a collection-like
    interface for accessing customer data while hiding the complexity of the underlying
    storage mechanism.
    """
    
    @abstractmethod
    def create(self, customer: Customer) -> Customer:
        """Creates a new customer in the repository.
        
        Args:
            customer: Customer entity to be persisted
            
        Returns:
            Customer: The newly created customer entity
            
        Raises:
            RepositoryError: If there's an error during the creation process
        """
        pass
    
    @abstractmethod
    def find(self, criteria: CustomerCriteriaFind) -> CustomerPaginatedResponse:
        """Retrieves customers from the repository based on the provided criteria.
        
        Args:
            criteria: CustomerCriteriaFind object containing search parameters, pagination,
                     and sorting information
                     
        Returns:
            CustomerPaginatedResponse: A paginated response containing the matching customers
                                     and pagination metadata
            
        Raises:
            RepositoryError: If there's an error during the search process
        """
        pass