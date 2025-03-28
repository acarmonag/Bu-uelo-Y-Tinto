from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.lib.Shared.domain.errors.DomainError import ValidationError
from src.lib.Shared.domain.object_value.BaseDescription import BaseDescription
from src.lib.Shared.domain.object_value.BaseImageUrl import BaseImageUrl
from src.lib.Shared.domain.object_value.BaseName import BaseName
from src.lib.Shared.domain.object_value.BasePrice import BasePrice
from src.lib.Shared.domain.object_value.BaseUUID import BaseUUID
from src.lib.Shared.domain.object_value.BaseBoolean import BaseBoolean
from src.lib.Shared.domain.object_value.BaseDate import BaseDate


@dataclass
class Product:
    """Product entity representing a product in the system.
    
    This class represents a product with all its attributes and business rules.
    It follows the Domain-Driven Design principles and encapsulates all
    product-related business logic.
    
    Attributes:
        id: Unique identifier for the product
        name: Product name
        description: Product description
        price: Product price
        image: URL to product image
        available: Whether the product is available
        created_at: Creation timestamp
        updated_at: Last update timestamp
        deleted_at: Soft deletion timestamp (if deleted)
    """
    
    id: BaseUUID
    name: BaseName
    description: BaseDescription
    price: BasePrice
    image: BaseImageUrl
    available: BaseBoolean
    created_at: BaseDate
    updated_at: BaseDate
    deleted_at: Optional[BaseDate] = None
    
    def __post_init__(self):
        """Validates the integrity of the product entity."""
        self._validate()
    
    def _validate(self):
        """Validates the business rules of the product.
        
        Raises:
            ValidationError: If any business rule is violated
        """
        if self.created_at.value > self.updated_at.value:
            raise ValidationError("Created date cannot be after updated date")
            
        if self.deleted_at and self.deleted_at.value < self.created_at.value:
            raise ValidationError("Deleted date cannot be before created date")
    
    def to_dict(self) -> dict:
        """Converts the product to a dictionary representation.
        
        Returns:
            dict: Dictionary containing all product attributes
        """
        return {
            "id": str(self.id),
            "name": str(self.name),
            "description": str(self.description),
            "price": self.price.to_dict(),
            "image": self.image.to_dict(),
            "available": self.available.value,
            "created_at": self.created_at.value.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.value.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.value.isoformat() if self.deleted_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        """Creates a Product instance from a dictionary.
        
        Args:
            data: Dictionary containing product data
            
        Returns:
            Product: New Product instance
        """
        return cls(
            id=BaseUUID(data["id"]),
            name=BaseName(data["name"]),
            description=BaseDescription(data["description"]),
            price=BasePrice(data["price"]["value"]),
            image=BaseImageUrl(data["image"]["value"]),
            available=BaseBoolean(data["available"]),
            created_at=BaseDate(datetime.fromisoformat(data["created_at"])) if data.get("created_at") else None,
            updated_at=BaseDate(datetime.fromisoformat(data["updated_at"])) if data.get("updated_at") else None,
            deleted_at=BaseDate(datetime.fromisoformat(data["deleted_at"])) if data.get("deleted_at") else None
        ) 