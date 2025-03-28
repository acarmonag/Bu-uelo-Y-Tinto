from dataclasses import dataclass
from lib.Shared.domain.errors.DomainError import ValidationError


@dataclass(frozen=True)
class BaseDescription:
    """Value object for handling descriptions.
    
    This class validates and encapsulates description values with the following rules:
    - Must be a string
    - Cannot be empty
    - Maximum length of 500 characters
    - Can contain letters, numbers, spaces, and basic punctuation
    
    Attributes:
        value: The description string value
    """
    value: str

    def __post_init__(self):
        """Validates the description value."""
        if not isinstance(self.value, str):
            raise ValidationError("Value must be a string")
        if not self.value.strip():
            raise ValidationError("Description cannot be empty")
        if len(self.value) > 500:
            raise ValidationError("Description cannot be longer than 500 characters")
        if not self._is_valid_description(self.value):
            raise ValidationError(f"Invalid description format: {self.value}")

        object.__setattr__(self, "value", self.value.strip())

    @staticmethod
    def _is_valid_description(description: str) -> bool:
        """Validates the description format.
        
        Args:
            description: The description string to validate
            
        Returns:
            bool: True if the description is valid, False otherwise
        """
        # Allow letters, numbers, spaces, and basic punctuation
        import re
        pattern = r"^[A-Za-z0-9\s.,!?;:'\"()\-]+$"
        return bool(re.match(pattern, description))

    def __eq__(self, other):
        """Compares two descriptions for equality.
        
        Args:
            other: Another BaseDescription instance to compare with
            
        Returns:
            bool: True if the descriptions are equal, False otherwise
        """
        if not isinstance(other, BaseDescription):
            return NotImplemented
        return self.value.lower() == other.value.lower()

    def equals(self, other: "BaseDescription") -> bool:
        """Compares two descriptions for exact equality.
        
        Args:
            other: Another BaseDescription instance to compare with
            
        Returns:
            bool: True if the descriptions are exactly equal, False otherwise
        """
        return self.value == other.value 