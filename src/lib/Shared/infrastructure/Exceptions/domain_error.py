from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime

from lib.Shared.domain.errors.DomainError import DomainError


async def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.message,
            "status": exc.status_code,
            "error": {
                "type": exc.__class__.__name__,
                "details": exc.details,
                "timestamp": datetime.utcnow().isoformat(),
                "path": request.url.path
            }
        }
    )
