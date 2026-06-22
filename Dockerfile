# Usamos una versión 'slim' para que el contenedor sea más ligero
FROM python:3.10-slim

# Instalamos dependencias del sistema necesarias para MySQL y procesado de imágenes/PDF
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Primero copiamos solo el requirements para aprovechar el caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Luego copiamos el resto del código
COPY . .

# Exponemos el puerto por defecto de Flask
EXPOSE 5000

CMD ["python", "app.py"]