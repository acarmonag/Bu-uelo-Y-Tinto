from src.lib.Product.domain.ProductSpecification import ProductCriteriaFind, ProductPaginatedResponse
from src.lib.Product.domain.ProductRepository import ProductRepository
from src.lib.Shared.domain.errors.DomainError import ValidationError


class ProductFinder:
    """Application service responsible for finding products.
    
    This class implements the use case for product search, following the
    Query pattern. It orchestrates the validation and retrieval of products
    based on search criteria.
    
    Attributes:
        repository: ProductRepository instance for data retrieval
    """
    
    def __init__(self, repository: ProductRepository):
        """Initialize the ProductFinder with a repository.
        
        Args:
            repository: ProductRepository instance for data retrieval
        """
        self.repository = repository
    
    def execute(self, criteria: ProductCriteriaFind) -> ProductPaginatedResponse:
        """Executes the product search use case.
        
        This method follows a two-step process:
        1. Validates the search criteria
        2. Retrieves products from the repository
        
        Args:
            criteria: ProductCriteriaFind object containing search parameters,
                     pagination, and sorting information
            
        Returns:
            ProductPaginatedResponse: A paginated response containing the matching
                                    products and pagination metadata
            
        Raises:
            ValidationError: If the search criteria is invalid
            RepositoryError: If there's an error during retrieval
        """
        # 1. Validate criteria
        errors = criteria.validate()
        if errors:
            raise ValidationError(', '.join(errors))
        
        # 2. Find products
        return self.repository.find(criteria) 