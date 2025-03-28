from dataclasses import dataclass
from lib.Shared.domain.errors.DomainError import ValidationError


@dataclass(frozen=True)
class BaseFloat:
    """Value object for handling float values.
    
    This class validates and encapsulates float values with the following rules:
    - Must be a float or convertible to float
    - Cannot be negative
    - Maximum of 2 decimal places
    - Maximum value of 1,000,000
    
    Attributes:
        value: The float value
    """
    value: float

    def __post_init__(self):
        """Validates the float value."""
        if not isinstance(self.value, (int, float)):
            raise ValidationError("Value must be a number")
            
        # Convert to float and round to 2 decimal places
        float_value = round(float(self.value), 2)
        
        if float_value < 0:
            raise ValidationError("Value cannot be negative")
            
        if float_value > 1_000_000:
            raise ValidationError("Value cannot be greater than 1,000,000")
            
        object.__setattr__(self, "value", float_value)

    def __eq__(self, other):
        """Compares two float values for equality.
        
        Args:
            other: Another BaseFloat instance to compare with
            
        Returns:
            bool: True if the values are equal, False otherwise
        """
        if not isinstance(other, BaseFloat):
            return NotImplemented
        return self.value == other.value

    def equals(self, other: "BaseFloat") -> bool:
        """Compares two float values for exact equality.
        
        Args:
            other: Another BaseFloat instance to compare with
            
        Returns:
            bool: True if the values are exactly equal, False otherwise
        """
        return self.value == other.value

    def to_string(self) -> str:
        """Converts the float value to a string with 2 decimal places.
        
        Returns:
            str: The float value as a string
        """
        return f"{self.value:.2f}"

    def to_int(self) -> int:
        """Converts the float value to an integer.
        
        Returns:
            int: The float value as an integer
        """
        return int(self.value) 