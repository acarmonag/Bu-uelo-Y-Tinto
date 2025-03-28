from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from src.lib.Customer.domain.Customer import Customer


@dataclass
class CustomerCommandCreate:
    """Data Transfer Object for creating a new customer.
    
    Attributes:
        name: Customer's full name
        email: Customer's email address
        password: Customer's password (min 8 characters)
        phone: Customer's phone number in international format
    """
    name: str
    email: str
    password: str
    phone: str
    
    def validate(self) -> List[str]:
        """Validates basic command data.
        
        Returns:
            List of validation error messages. Empty list if validation passes.
        """
        errors = []
        if not self.name:
            errors.append("Name is required")
        if not self.email or "@" not in self.email:
            errors.append("Valid email is required")
        if not self.password or len(self.password) < 8:
            errors.append("Password must be at least 8 characters")
        if not self.phone:
            errors.append("Phone is required")
        return errors


@dataclass
class CustomerCommandUpdate:
    """Data Transfer Object for updating an existing customer.
    
    Attributes:
        id: Customer's unique identifier
        name: Optional new name for the customer
        email: Optional new email for the customer
        phone: Optional new phone number for the customer
    """
    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    
    def validate(self) -> List[str]:
        """Validates update command data.
        
        Returns:
            List of validation error messages. Empty list if validation passes.
        """
        errors = []
        if not self.id:
            errors.append("Customer ID is required")
        if self.email and "@" not in self.email:
            errors.append("Email must be valid")
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
class CustomerCriteriaFind(BaseCriteriaFind):
    """Search criteria specific to customer queries.
    
    Attributes:
        id: Optional customer ID to filter by
        name: Optional name to filter by
        email: Optional email to filter by
        phone: Optional phone number to filter by
        is_deleted: Optional flag to filter by deletion status
    """
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
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
        if self.email:
            filters["email"] = self.email
        if self.phone:
            filters["phone"] = self.phone
        if self.is_deleted is not None:
            filters["is_deleted"] = self.is_deleted
        return filters


@dataclass
class CustomerPaginatedResponse:
    """Paginated response for customer listings.
    
    Attributes:
        items: List of customer entities
        total: Total number of customers matching the criteria
        page: Current page number
        limit: Number of items per page
        pages: Total number of pages
    """
    items: List[Customer]
    total: int
    page: int
    limit: int
    pages: int
    
    @classmethod
    def create(cls, items: List[Customer], total: int, criteria: BaseCriteriaFind) -> 'CustomerPaginatedResponse':
        """Creates a paginated response from search results.
        
        Args:
            items: List of customer entities
            total: Total number of customers matching the criteria
            criteria: Search criteria used for the query
            
        Returns:
            CustomerPaginatedResponse instance with calculated pagination
        """
        pages = (total + criteria.limit - 1) // criteria.limit if criteria.limit > 0 else 0
        return cls(
            items=items,
            total=total,
            page=criteria.page,
            limit=criteria.limit,
            pages=pages
        )