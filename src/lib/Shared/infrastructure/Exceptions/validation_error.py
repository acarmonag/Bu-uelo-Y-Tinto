from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from lib.Shared.infrastructure.Schema.Responses import ErrorResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {
        'type': 'ValidationError',
        'details': {}
    }

    for error in exc.errors():
        location = error.get("loc", [])
        error_type = error.get("type")
        field = location[-1] if location else ""

        # Para campos extra no permitidos
        if error_type == "extra_forbidden":
            errors['details'][field] = {
                'error': 'field not allowed in schema',
                'received': error.get("input")
            }
            continue

        # Para campos requeridos y otros errores
        errors['details'][field] = {
            'error': error.get("msg", "Invalid value"),
            'received': error.get("input")
        }

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            message="Schema validation failed",
            error=errors,
            status=422
        ).dict()
    )
