from dataclasses import dataclass, field
from .BaseResult import BaseResult


@dataclass
class BaseQueryResult(BaseResult):
    """Base class for query operation results"""
    total: int = 0
    page: int = 0
    per_page: int = 0
    total_pages: int = field(init=False)
    has_next: bool = field(init=False)
    has_previous: bool = field(init=False)

    def __post_init__(self) -> None:
        """Validate and compute pagination data"""
        if self.total < 0 or self.page < 0 or self.per_page < 0:
            raise ValueError("Total, page and per_page cannot be negative")
        
        if self.per_page == 0:
            raise ValueError("per_page cannot be zero")
            
        self.total_pages = (self.total + self.per_page - 1) // self.per_page
        self.has_next = self.page < self.total_pages
        self.has_previous = self.page > 1
        
        super().__post_init__()

    @property
    def offset(self) -> int:
        """Calculate the offset for pagination"""
        return (self.page - 1) * self.per_page