from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from src.lib.Product.domain.Product import Product


@dataclass
class ProductCriteriaFind:
    """Data Transfer Object for product search criteria.
    
    This class encapsulates all parameters needed for searching products,
    including pagination and sorting information.
    
    Attributes:
        page: Page number for pagination (1-based)
        limit: Number of items per page
        order_by: Field to sort by
        order_direction: Sort direction ('asc' or 'desc')
        name: Optional name filter
        min_price: Optional minimum price filter
        max_price: Optional maximum price filter
        available: Optional availability filter
    """
    
    page: int = 1
    limit: int = 10
    order_by: str = "created_at"
    order_direction: str = "desc"
    name: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    available: Optional[bool] = None
    
    def validate(self) -> List[str]:
        """Validates the search criteria.
        
        Returns:
            List[str]: List of validation error messages. Empty list if validation passes.
        """
        errors = []
        
        # Validate pagination
        if self.page < 1:
            errors.append("Page number must be greater than 0")
        if self.limit < 1:
            errors.append("Limit must be greater than 0")
        if self.limit > 100:
            errors.append("Limit cannot be greater than 100")
            
        # Validate sorting
        valid_fields = ["id", "name", "price", "available", "created_at", "updated_at"]
        if self.order_by not in valid_fields:
            errors.append(f"Invalid sort field. Must be one of: {', '.join(valid_fields)}")
            
        if self.order_direction not in ["asc", "desc"]:
            errors.append("Sort direction must be 'asc' or 'desc'")
            
        # Validate price range
        if self.min_price is not None and self.min_price < 0:
            errors.append("Minimum price cannot be negative")
            
        if self.max_price is not None and self.max_price < 0:
            errors.append("Maximum price cannot be negative")
            
        if (self.min_price is not None and self.max_price is not None and 
            self.min_price > self.max_price):
            errors.append("Minimum price cannot be greater than maximum price")
            
        return errors


@dataclass
class ProductPaginatedResponse:
    """Data Transfer Object for paginated product responses.
    
    This class encapsulates the response data for paginated product queries,
    including both the products and pagination metadata.
    
    Attributes:
        items: List of products in the current page
        total: Total number of products matching the criteria
        page: Current page number
        limit: Number of items per page
        total_pages: Total number of pages
    """
    
    items: List[Product]
    total: int
    page: int
    limit: int
    total_pages: int
    
    def to_dict(self) -> dict:
        """Converts the response to a dictionary representation.
        
        Returns:
            dict: Dictionary containing the response data
        """
        return {
            "items": [product.to_dict() for product in self.items],
            "total": self.total,
            "page": self.page,
            "limit": self.limit,
            "total_pages": self.total_pages
        } 