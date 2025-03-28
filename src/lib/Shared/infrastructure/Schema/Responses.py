from typing import TypeVar, Generic, Dict, Any, Optional

from pydantic import BaseModel

T = TypeVar("T")
StatusCode = TypeVar("StatusCode", bound=int)


class SuccessResponse(BaseModel, Generic[T]):
    message: str
    status: int = 200
    data: Optional[T] = None


class ErrorResponse(BaseModel, Generic[StatusCode]):
    message: str
    status: StatusCode
    error: Dict[str, Any]
