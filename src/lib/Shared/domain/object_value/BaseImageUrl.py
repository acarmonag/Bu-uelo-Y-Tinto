from urllib.parse import urlparse
from typing import Optional

from src.lib.Shared.domain.object_value.BaseString import BaseString


class BaseImageUrl(BaseString):
    """Value object for handling product image URLs.
    
    This class extends BaseString to add specific validation for image URLs.
    It ensures URLs are:
    - Valid URLs
    - Have appropriate image file extensions
    - Are properly formatted
    
    Attributes:
        value: String value representing the image URL
    """
    
    def __init__(self, value: str):
        """Initialize an image URL value.
        
        Args:
            value: URL value to validate and store
            
        Raises:
            ValueError: If the URL is invalid or not an image URL
        """
        super().__init__(value)
        
        # Validate URL format
        try:
            result = urlparse(self.value)
            if not all([result.scheme, result.netloc]):
                raise ValueError("Invalid URL format")
        except Exception:
            raise ValueError("Invalid URL format")
        
        # Validate image extension
        valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        if not any(self.value.lower().endswith(ext) for ext in valid_extensions):
            raise ValueError("URL must point to a valid image file")
    
    def to_dict(self) -> dict:
        """Converts the image URL to a dictionary representation.
        
        Returns:
            dict: Dictionary containing the image URL value
        """
        return {
            "value": self.value
        } 