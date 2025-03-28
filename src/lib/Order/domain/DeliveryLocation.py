from dataclasses import dataclass
from lib.Shared.domain.errors.DomainError import ValidationError


@dataclass(frozen=True)
class DeliveryLocation:
    """Value object for handling delivery locations.
    
    This class validates and encapsulates delivery location values with the following rules:
    - Must be a string
    - Cannot be empty
    - Maximum length of 200 characters
    - Can contain letters, numbers, spaces, and basic punctuation
    - Must contain at least one comma (for separating address components)
    
    Attributes:
        value: The delivery location string value
    """
    value: str

    def __post_init__(self):
        """Validates the delivery location value."""
        if not isinstance(self.value, str):
            raise ValidationError("Value must be a string")
        if not self.value.strip():
            raise ValidationError("Delivery location cannot be empty")
        if len(self.value) > 200:
            raise ValidationError("Delivery location cannot be longer than 200 characters")
        if not self._is_valid_location(self.value):
            raise ValidationError(f"Invalid delivery location format: {self.value}")
        if ',' not in self.value:
            raise ValidationError("Delivery location must contain at least one comma to separate address components")

        object.__setattr__(self, "value", self.value.strip())

    @staticmethod
    def _is_valid_location(location: str) -> bool:
        """Validates the delivery location format.
        
        Args:
            location: The location string to validate
            
        Returns:
            bool: True if the location is valid, False otherwise
        """
        # Allow letters, numbers, spaces, and basic punctuation
        import re
        pattern = r"^[A-Za-z0-9\s.,!?;:'\"()\-]+$"
        return bool(re.match(pattern, location))

    def __eq__(self, other):
        """Compares two delivery locations for equality.
        
        Args:
            other: Another DeliveryLocation instance to compare with
            
        Returns:
            bool: True if the locations are equal, False otherwise
        """
        if not isinstance(other, DeliveryLocation):
            return NotImplemented
        return self.value.lower() == other.value.lower()

    def equals(self, other: "DeliveryLocation") -> bool:
        """Compares two delivery locations for exact equality.
        
        Args:
            other: Another DeliveryLocation instance to compare with
            
        Returns:
            bool: True if the locations are exactly equal, False otherwise
        """
        return self.value == other.value 