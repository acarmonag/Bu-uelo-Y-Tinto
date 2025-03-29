import logging
import sys
from datetime import datetime
import json

# Configuración del logger
def setup_logger():
    # Crear el logger
    logger = logging.getLogger('buuelo_y_tinto')
    logger.setLevel(logging.DEBUG)

    # Crear el formateador
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Handler para archivo
    file_handler = logging.FileHandler(f'logs/buuelo_y_tinto_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Agregar los handlers al logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Crear el logger global
logger = setup_logger()

def format_request_body(request):
    """Formatea el body de la petición de manera segura"""
    try:
        if request.content_type == 'application/json':
            return json.loads(request.body)
        elif request.content_type == 'application/x-www-form-urlencoded':
            return dict(request.POST)
        elif request.content_type == 'multipart/form-data':
            return dict(request.POST)
        return "Body no procesable"
    except:
        return "Body no procesable"

def format_response_body(response):
    """Formatea el body de la respuesta de manera segura"""
    try:
        if hasattr(response, 'content'):
            return json.loads(response.content)
        return "Respuesta no procesable"
    except:
        return "Respuesta no procesable"

# Funciones de conveniencia para diferentes tipos de logs
def log_db_connection(operation, status, details=None):
    """Registra conexiones a la base de datos"""
    status_emoji = "✅" if status == "SUCCESS" else "❌"
    logger.info(f"{status_emoji} DB Connection: {operation} - {details or ''}")

def log_db_operation(operation, status, details=None):
    """Registra operaciones de base de datos"""
    status_emoji = "✅" if status == "SUCCESS" else "❌"
    logger.info(f"{status_emoji} DB Operation: {operation} - {details or ''}")

def log_api_request(request, response, duration, status="SUCCESS"):
    """Registra peticiones API completas"""
    status_emoji = "✅" if status == "SUCCESS" else "❌"
    request_body = format_request_body(request)
    response_body = format_response_body(response)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "method": request.method,
        "path": request.path,
        "user": str(request.user) if hasattr(request, 'user') else "Anonymous",
        "status_code": response.status_code,
        "duration": f"{duration:.2f}s",
        "request_body": request_body,
        "response_body": response_body,
        "status": status
    }
    
    logger.info(f"{status_emoji} API Request: {json.dumps(log_entry, indent=2)}")

def log_auth_attempt(user_id, success, details=None):
    """Registra intentos de autenticación"""
    status = "SUCCESS" if success else "FAILED"
    status_emoji = "✅" if success else "❌"
    logger.info(f"{status_emoji} Auth Attempt - User: {user_id} - Status: {status} - {details or ''}")

def log_order_operation(operation, order_id, status, details=None):
    """Registra operaciones de órdenes"""
    status_emoji = "✅" if status == "SUCCESS" else "❌"
    logger.info(f"{status_emoji} Order Operation: {operation} - Order ID: {order_id} - Status: {status} - {details or ''}")

def log_error(error_type, error_message, details=None):
    """Registra errores"""
    logger.error(f"❌ Error Type: {error_type} - Message: {error_message} - {details or ''}")

def log_warning(warning_type, warning_message, details=None):
    """Registra advertencias"""
    logger.warning(f"⚠️ Warning Type: {warning_type} - Message: {warning_message} - {details or ''}") 