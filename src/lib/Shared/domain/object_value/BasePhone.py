from dataclasses import dataclass
import re
from typing import Optional

from lib.Shared.domain.errors.DomainError import ValidationError


@dataclass(frozen=True)
class BasePhone:
    """Value object for phone numbers with international format"""
    value: str

    def __post_init__(self):
        """Validate phone number format"""
        if not isinstance(self.value, str):
            raise ValidationError("Phone number must be a string")
        
        # Validate international phone format (e.g., +573128949458)
        pattern = r'^\+[1-9]\d{1,14}$'
        if not re.match(pattern, self.value):
            raise ValidationError(f"Invalid phone number format: {self.value}. Must start with '+' followed by country code and number.")
        
        # Ensure the total length is reasonable (typically between 8 and 15 digits plus the '+')
        if len(self.value) < 8 or len(self.value) > 16:
            raise ValidationError(f"Phone number has invalid length: {len(self.value)} chars. Expected between 8 and 16.")

    @classmethod
    def from_string(cls, value: str) -> 'BasePhone':
        """Create phone from string representation"""
        return cls(value)
    
    @classmethod
    def from_parts(cls, country_code: str, number: str) -> 'BasePhone':
        """Create phone from country code and number parts"""
        # Remove leading zeros from country code if present
        clean_country_code = country_code.lstrip('0')
        
        # Remove any non-digit characters from number
        clean_number = re.sub(r'\D', '', number)
        
        # Ensure country code starts with '+'
        if not clean_country_code.startswith('+'):
            clean_country_code = '+' + clean_country_code
            
        return cls(f"{clean_country_code}{clean_number}")
    
    def to_string(self) -> str:
        """Convert phone to string representation"""
        return self.value
    
    def get_country_code(self) -> str:
        """Extract country code from phone number"""
        # Match the + and following digits until first non-digit boundary would appear
        match = re.match(r'^\+(\d+)', self.value)
        if match:
            return '+' + match.group(1)
        return ''
    
    def get_number_without_country_code(self) -> str:
        """Get number without country code"""
        country_code = self.get_country_code()
        if country_code:
            return self.value[len(country_code):]
        return self.value
    
    def format_national(self) -> str:
        """Format as national number without country code"""
        return self.get_number_without_country_code()
    
    def format_international(self) -> str:
        """Format as international number (already in that format)"""
        return self.value
    
    def format_e164(self) -> str:
        """Format as E.164 standard (already in that format)"""
        return self.value
    
    def format_readable(self) -> str:
        """Format in a human-readable way with spaces"""
        country_code = self.get_country_code()
        number = self.get_number_without_country_code()
        
        # Group the number for readability (may need customization based on country)
        if len(number) <= 4:
            return f"{country_code} {number}"
        elif len(number) <= 7:
            return f"{country_code} {number[:3]} {number[3:]}"
        else:
            # For longer numbers, group in blocks of 3 or 4 digits
            groups = []
            while number:
                groups.append(number[:3])
                number = number[3:]
            return f"{country_code} " + " ".join(groups)
    
    def __eq__(self, other) -> bool:
        """Compare two phone numbers"""
        if not isinstance(other, BasePhone):
            return NotImplemented
        return self.value == other.value
    
    def equals(self, other: 'BasePhone') -> bool:
        """Compare two phone numbers (case-sensitive)"""
        return self.value == other.value
    
    def is_mobile(self) -> bool:
        """Attempt to determine if this is likely a mobile number"""
        # This is a simplified approach - actual implementation would need
        # country-specific rules which would be quite complex
        # For Colombia (+57), mobile numbers typically start with 3
        if self.value.startswith('+57'):
            return self.get_number_without_country_code().startswith('3')
        
        # For other countries, this is a placeholder and would need specific rules
        return True
    
    def anonymize(self) -> str:
        """Return an anonymized version of the phone number"""
        country_code = self.get_country_code()
        number = self.get_number_without_country_code()
        
        # Keep first 2 and last 2 digits, replace the rest with 'x'
        if len(number) > 4:
            return f"{country_code}{number[:2]}{'x' * (len(number) - 4)}{number[-2:]}"
        return f"{country_code}{'x' * len(number)}"