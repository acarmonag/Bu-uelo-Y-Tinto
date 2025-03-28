from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from src.lib.Order.domain.Order import Order
from src.lib.Shared.domain.errors.DomainError import ValidationError
from src.lib.Shared.domain.object_value.BaseFloat import BaseFloat


@dataclass
class OrderCommandCreate:
    """Data Transfer Object for creating a new order.
    
    Attributes:
        customer_name: Name of the customer who placed the order
        order_status_name: Name of the current order status
        delivery_location: Location where the order should be delivered
        total: Total amount of the order
    """
    customer_name: str
    order_status_name: str
    delivery_location: str
    total: float
    
    def validate(self) -> List[str]:
        """Validates basic command data.
        
        Returns:
            List of validation error messages. Empty list if validation passes.
        """
        errors = []
        if not self.customer_name:
            errors.append("Customer name is required")
        if not self.order_status_name:
            errors.append("Order status name is required")
        if not self.delivery_location:
            errors.append("Delivery location is required")
        try:
            BaseFloat(self.total)
        except ValidationError as e:
            errors.append(str(e))
        return errors


@dataclass
class OrderCommandUpdate:
    """Data Transfer Object for updating an existing order.
    
    Attributes:
        id: Order unique identifier
        customer_name: Optional new customer name
        order_status_name: Optional new order status name
        delivery_location: Optional new delivery location
        total: Optional new total amount
    """
    id: str
    customer_name: Optional[str] = None
    order_status_name: Optional[str] = None
    delivery_location: Optional[str] = None
    total: Optional[float] = None
    
    def validate(self) -> List[str]:
        """Validates update command data.
        
        Returns:
            List of validation error messages. Empty list if validation passes.
        """
        errors = []
        if not self.id:
            errors.append("Order ID is required")
        if self.total is not None:
            try:
                BaseFloat(self.total)
            except ValidationError as e:
                errors.append(str(e))
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
class OrderCriteriaFind(BaseCriteriaFind):
    """Search criteria specific to order queries.
    
    Attributes:
        id: Optional order ID to filter by
        customer_name: Optional customer name to filter by
        order_status_name: Optional order status name to filter by
        is_deleted: Optional flag to filter by deletion status
    """
    id: Optional[str] = None
    customer_name: Optional[str] = None
    order_status_name: Optional[str] = None
    is_deleted: Optional[bool] = None
    
    def to_filters(self) -> Dict[str, Any]:
        """Converts criteria to query filters.
        
        Returns:
            Dictionary containing all non-null filter parameters.
        """
        filters = {}
        if self.id:
            filters["id"] = self.id
        if self.customer_name:
            filters["customer_name"] = self.customer_name
        if self.order_status_name:
            filters["order_status_name"] = self.order_status_name
        if self.is_deleted is not None:
            filters["is_deleted"] = self.is_deleted
        return filters


@dataclass
class OrderPaginatedResponse:
    """Paginated response for order listings.
    
    Attributes:
        items: List of order entities
        total: Total number of orders matching the criteria
        page: Current page number
        limit: Number of items per page
        pages: Total number of pages
    """
    items: List[Order]
    total: int
    page: int
    limit: int
    pages: int
    
    @classmethod
    def create(cls, items: List[Order], total: int, criteria: BaseCriteriaFind) -> 'OrderPaginatedResponse':
        """Creates a paginated response from search results.
        
        Args:
            items: List of order entities
            total: Total number of orders matching the criteria
            criteria: Search criteria used for the query
            
        Returns:
            OrderPaginatedResponse instance with calculated pagination
        """
        pages = (total + criteria.limit - 1) // criteria.limit if criteria.limit > 0 else 0
        return cls(
            items=items,
            total=total,
            page=criteria.page,
            limit=criteria.limit,
            pages=pages
        ) 