# Usamos una imagen base de Python
FROM python:3.10-slim

# Instalamos las dependencias necesarias para psycopg2 y PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de requerimientos dentro del contenedor
COPY requirements.txt .

# Instalamos las dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiamos todo el código del proyecto al contenedor
COPY . .

# Exponemos el puerto en el que la app va a correr
EXPOSE 8000

# Comando por defecto para iniciar el servidor de desarrollo de Django
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
