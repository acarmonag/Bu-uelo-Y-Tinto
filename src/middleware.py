import threading
from django.utils.deprecation import MiddlewareMixin
from src.logger import logger, log_api_request
import time


_thread_locals = threading.local()

def current_request():
    '''Retorna el request'''
    
    return _thread_locals


class GlobalCurrentRequestMiddleware(MiddlewareMixin):
    '''Coloca el request en el hilo local y registra logs detallados'''
    
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.start_time = None

    def process_request(self, request):
        self.start_time = time.time()
        # Log de la petición entrante
        logger.info(f"Request: {request.method} {request.path} - User: {request.user if hasattr(request, 'user') else 'Anonymous'}")
        _thread_locals.current_request = request

    def process_response(self, request, response):
        # Calcular tiempo de respuesta
        duration = time.time() - self.start_time if self.start_time else 0
        
        # Determinar el estado de la respuesta
        status = "SUCCESS" if 200 <= response.status_code < 300 else "ERROR"
        
        # Registrar la petición completa
        log_api_request(request, response, duration, status)
        
        return response

    def process_exception(self, request, exception):
        # Calcular tiempo hasta la excepción
        duration = time.time() - self.start_time if self.start_time else 0
        
        # Crear una respuesta de error para logging
        from django.http import JsonResponse
        error_response = JsonResponse(
            {"error": str(exception)},
            status=500
        )
        
        # Registrar la petición con error
        log_api_request(request, error_response, duration, "ERROR")
        
        return None