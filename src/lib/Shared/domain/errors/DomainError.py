class DomainError(Exception):
    """Base exception for domain errors"""

    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(DomainError):
    """Raised when a resource is not found"""

    def __init__(self, message: str):
        super().__init__(message, status_code=404)


class ValidationError(DomainError):
    """Raised when domain validation fails"""

    def __init__(self, message: str):
        super().__init__(message, status_code=422)


class ConflictError(DomainError):
    """Raised when there's a conflict with existing data"""

    def __init__(self, message: str):
        super().__init__(message, status_code=409)


class UnauthorizedError(DomainError):
    """Raised when authentication fails"""

    def __init__(self, message: str):
        super().__init__(message, status_code=401)


class ForbiddenError(DomainError):
    """Raised when user doesn't have permission"""

    def __init__(self, message: str):
        super().__init__(message, status_code=403)


class BadRequestError(DomainError):
    """Raised when the request is malformed or invalid"""

    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class RateLimitError(DomainError):
    """Raised when rate limit is exceeded"""

    def __init__(self, message: str):
        super().__init__(message, status_code=429)


class ServiceUnavailableError(DomainError):
    """Raised when a service is unavailable"""

    def __init__(self, message: str):
        super().__init__(message, status_code=503)
