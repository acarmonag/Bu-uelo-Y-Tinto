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

# Creamos el directorio de logs y establecemos los permisos
RUN mkdir -p /app/logs && \
    chmod 777 /app/logs

# Copiamos el archivo de requerimientos dentro del contenedor
COPY requirements.txt .

# Instalamos las dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiamos todo el código del proyecto al contenedor
COPY . .

# Aseguramos que la carpeta de logs tenga los permisos correctos después de copiar el código
RUN chmod 777 /app/logs

# Exponemos el puerto en el que la app va a correr
EXPOSE 8000

# Comando por defecto para iniciar el servidor de desarrollo de Django
CMD ["sh", "-c", "python manage.py migrate && python run.py && python manage.py runserver 0.0.0.0:8000"]