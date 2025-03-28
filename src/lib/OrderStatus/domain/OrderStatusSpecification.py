from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from src.lib.OrderStatus.domain.OrderStatus import OrderStatus


@dataclass
class OrderStatusCommandCreate:
    """Data Transfer Object for creating a new order status.
    
    Attributes:
        name: Name of the status (e.g., 'pending', 'processing')
        description: Detailed description of what the status means
    """
    name: str
    description: str
    
    def validate(self) -> List[str]:
        """Validates basic command data.
        
        Returns:
            List of validation error messages. Empty list if validation passes.
        """
        errors = []
        if not self.name:
            errors.append("Name is required")
        if not self.description:
            errors.append("Description is required")
        return errors


@dataclass
class OrderStatusCommandUpdate:
    """Data Transfer Object for updating an existing order status.
    
    Attributes:
        id: Order status unique identifier
        name: Optional new name for the status
        description: Optional new description for the status
    """
    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    
    def validate(self) -> List[str]:
        """Validates update command data.
        
        Returns:
            List of validation error messages. Empty list if validation passes.
        """
        errors = []
        if not self.id:
            errors.append("Order status ID is required")
        return errors


@dataclass
class BaseCriteriaFind:
    """Base class for search criteria with pagination and sorting.
    
    Attributes:
        page: Current page number (1-based)
        limit: Number of items per page
        order_by: Field to sort by
        order_direction: Sort direction ('asc' or 'desc')
    """
    page: int = 1
    limit: int = 10
    order_by: str = "created_at"
    order_direction: str = "desc"  # asc or desc
    
    def get_pagination(self) -> Dict[str, int]:
        """Calculates pagination parameters.
        
        Returns:
            Dictionary containing page, limit, and offset values.
        """
        return {
            "page": self.page,
            "limit": self.limit,
            "offset": (self.page - 1) * self.limit
        }
    
    def get_order(self) -> Dict[str, str]:
        """Gets sorting parameters.
        
        Returns:
            Dictionary containing field and direction for sorting.
        """
        return {
            "field": self.order_by,
            "direction": self.order_direction
        }


@dataclass
class OrderStatusCriteriaFind(BaseCriteriaFind):
    """Search criteria specific to order status queries.
    
    Attributes:
        id: Optional status ID to filter by
        name: Optional name to filter by
        is_deleted: Optional flag to filter by deletion status
    """
    id: Optional[str] = None
    name: Optional[str] = None
    is_deleted: Optional[bool] = None
    
    def to_filters(self) -> Dict[str, Any]:
        """Converts criteria to query filters.
        
        Returns:
            Dictionary containing all non-null filter parameters.
        """
        filters = {}
        if self.id:
            filters["id"] = self.id
        if self.name:
            filters["name"] = self.name
        if self.is_deleted is not None:
            filters["is_deleted"] = self.is_deleted
        return filters


@dataclass
class OrderStatusPaginatedResponse:
    """Paginated response for order status listings.
    
    Attributes:
        items: List of order status entities
        total: Total number of statuses matching the criteria
        page: Current page number
        limit: Number of items per page
        pages: Total number of pages
    """
    items: List[OrderStatus]
    total: int
    page: int
    limit: int
    pages: int
    
    @classmethod
    def create(cls, items: List['OrderStatus'], total: int, criteria: BaseCriteriaFind) -> 'OrderStatusPaginatedResponse':
        """Creates a paginated response from search results.
        
        Args:
            items: List of order status entities
            total: Total number of statuses matching the criteria
            criteria: Search criteria used for the query
            
        Returns:
            OrderStatusPaginatedResponse instance with calculated pagination
        """
        pages = (total + criteria.limit - 1) // criteria.limit if criteria.limit > 0 else 0
        return cls(
            items=items,
            total=total,
            page=criteria.page,
            limit=criteria.limit,
            pages=pages
        ) 