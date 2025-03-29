from functools import wraps
from src.logger import log_db_operation
import time

def log_database_operation(operation_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                log_db_operation(
                    operation_name,
                    "SUCCESS",
                    f"Duration: {duration:.2f}s"
                )
                return result
            except Exception as e:
                duration = time.time() - start_time
                log_db_operation(
                    operation_name,
                    "ERROR",
                    f"Error: {str(e)} - Duration: {duration:.2f}s"
                )
                raise
        return wrapper
    return decorator 