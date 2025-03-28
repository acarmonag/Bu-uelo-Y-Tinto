from decimal import Decimal
from typing import Optional

from src.lib.Shared.domain.object_value.BaseFloat import BaseFloat


class BasePrice(BaseFloat):
    """Value object for handling product prices.
    
    This class extends BaseFloat to add specific validation and formatting
    for price values. It ensures prices are:
    - Non-negative
    - Have at most 2 decimal places
    - Are properly formatted for currency display
    
    Attributes:
        value: Decimal value representing the price
    """
    
    def __init__(self, value: float | Decimal | str):
        """Initialize a price value.
        
        Args:
            value: Price value to validate and store
            
        Raises:
            ValueError: If the price is negative or invalid
        """
        super().__init__(value)
        
        # Ensure price is non-negative
        if self.value < 0:
            raise ValueError("Price cannot be negative")
            
        # Round to 2 decimal places
        self.value = Decimal(str(self.value)).quantize(
            Decimal('0.01'),
            rounding=Decimal.ROUND_HALF_UP
        )
    
    def __str__(self) -> str:
        """Returns the price formatted as currency.
        
        Returns:
            str: Price formatted with 2 decimal places
        """
        return f"{self.value:.2f}"
    
    def to_dict(self) -> dict:
        """Converts the price to a dictionary representation.
        
        Returns:
            dict: Dictionary containing the price value
        """
        return {
            "value": float(self.value)
        } 