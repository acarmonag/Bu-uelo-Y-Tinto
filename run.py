import os
import django
from pathlib import Path

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
            print("✅ Superusuario creado exitosamente")
        else:
            print("ℹ️ El superusuario 'admin' ya existe")
    except Exception as e:
        print(f"❌ Error creando el superusuario: {str(e)}")

if __name__ == '__main__':
    create_superuser()