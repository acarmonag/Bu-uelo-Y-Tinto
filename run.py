import os
import django
from pathlib import Path
from src.logger import logger, log_db_operation

# Configurar el módulo de settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Inicializar Django
django.setup()

# Importar el modelo de usuario personalizado
from infrastructure.models.user import User

def create_superuser():
    try:
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='adminpassword'
            )
            log_db_operation("CREATE_SUPERUSER", "Superusuario 'admin' creado exitosamente")
            print("✅ Superusuario creado exitosamente")
        else:
            log_db_operation("CHECK_SUPERUSER", "El superusuario 'admin' ya existe")
            print("ℹ️ El superusuario 'admin' ya existe")
    except Exception as e:
        logger.error(f"Error creando el superusuario: {str(e)}")
        print(f"❌ Error creando el superusuario: {str(e)}")

if __name__ == '__main__':
    logger.info("Iniciando aplicación Bu-uelo y Tinto")
    create_superuser()
    logger.info("Aplicación iniciada correctamente")