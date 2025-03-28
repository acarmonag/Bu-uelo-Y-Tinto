from src.lib.Customer.domain.CustomerSpecification import CustomerCriteriaFind, CustomerPaginatedResponse
from src.lib.Customer.domain.CustomerRepository import CustomerRepository
from src.lib.Shared.domain.errors.DomainError import ValidationError


class CustomerFinder:
    """Application service responsible for finding customers.
    
    This class implements the use case for customer search, following the
    Query pattern. It orchestrates the validation and retrieval of customers
    based on search criteria.
    
    Attributes:
        repository: CustomerRepository instance for data retrieval
    """
    
    def __init__(self, repository: CustomerRepository):
        """Initialize the CustomerFinder with a repository.
        
        Args:
            repository: CustomerRepository instance for data retrieval
        """
        self.repository = repository
    
    def execute(self, criteria: CustomerCriteriaFind) -> CustomerPaginatedResponse:
        """Executes the customer search use case.
        
        This method follows a two-step process:
        1. Validates the search criteria
        2. Retrieves customers from the repository
        
        Args:
            criteria: CustomerCriteriaFind object containing search parameters,
                     pagination, and sorting information
            
        Returns:
            CustomerPaginatedResponse: A paginated response containing the matching
                                     customers and pagination metadata
            
        Raises:
            ValidationError: If the search criteria is invalid
            RepositoryError: If there's an error during retrieval
        """
        # 1. Validate criteria
        errors = criteria.validate()
        if errors:
            raise ValidationError(', '.join(errors))
        
        # 2. Find customers
        return self.repository.find(criteria) 