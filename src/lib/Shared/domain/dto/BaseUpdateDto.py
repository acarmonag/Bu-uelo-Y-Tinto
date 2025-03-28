from dataclasses import dataclass

from lib.Shared.domain.errors.DomainError import BadRequestError


@dataclass
class BaseUpdateDto:
    def __post_init__(self):
        optional_fields = [field for field in self.__dict__ if field != 'cmd']

        if all(self.__dict__[field] is None for field in optional_fields):
            raise BadRequestError("At least one field is required")
