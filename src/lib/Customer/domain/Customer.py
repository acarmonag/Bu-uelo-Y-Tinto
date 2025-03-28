from dataclasses import dataclass

from src.lib.Shared.domain.object_value.BaseUUID import BaseUUID
from src.lib.Shared.domain.object_value.BaseName import BaseName
from src.lib.Shared.domain.object_value.BaseEmail import BaseEmail
from src.lib.Shared.domain.object_value.BasePassword import BasePassword
from src.lib.Shared.domain.object_value.BasePhone import BasePhone
from src.lib.Shared.domain.object_value.BaseDate import BaseDate
from src.lib.Shared.domain.errors.DomainError import ValidationError

@dataclass
class Customer:
    id: BaseUUID
    name: BaseName
    email: BaseEmail
    password: BasePassword
    phone: BasePhone
    created_at: BaseDate
    updated_at: BaseDate
    deleted_at: BaseDate
    
    def __post_init__(self):
        self._validate()
    
    def _validate(self):
        """Validar la integridad del objeto"""
        if self.created_at.value > self.updated_at.value:
            raise ValidationError("Created date cannot be after updated date")
            
        if self.deleted_at and self.deleted_at.value < self.created_at.value:
            raise ValidationError("Deleted date cannot be before created date")