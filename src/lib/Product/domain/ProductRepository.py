from abc import ABC, abstractmethod
from typing import Optional

from src.lib.Product.domain.Product import Product
from src.lib.Product.domain.ProductSpecification import ProductCriteriaFind, ProductPaginatedResponse


class ProductRepository(ABC):
    """Repository interface for Product persistence operations.
    
    This interface defines the contract for Product persistence operations,
    following the Repository pattern. It provides methods for querying products.
    """
    
    @abstractmethod
    def find_by_id(self, product_id: str) -> Optional[Product]:
        """Finds a product by its ID.
        
        Args:
            product_id: Unique identifier of the product
            
        Returns:
            Optional[Product]: The found product or None if not found
            
        Raises:
            RepositoryError: If there's an error during retrieval
        """
        pass
    
    @abstractmethod
    def find(self, criteria: ProductCriteriaFind) -> ProductPaginatedResponse:
        """Finds products based on search criteria.
        
        Args:
            criteria: ProductCriteriaFind object containing search parameters
            
        Returns:
            ProductPaginatedResponse: Paginated response with matching products
            
        Raises:
            RepositoryError: If there's an error during retrieval
        """
        pass 