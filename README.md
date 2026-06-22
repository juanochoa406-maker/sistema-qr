# Sistema de Gestión Documental con Validación QR

Sistema web desarrollado para la captura, generación, inyección de códigos QR y validación documental.

## Estructura del Repositorio
- `app.py`: Código fuente del backend (Flask).
- `docker-compose.yml`: Orquestación de contenedores.
- `Dockerfile`: Definición de la imagen de la aplicación.
- `init.sql`: Script de inicialización de la base de datos MySQL.
- `requirements.txt`: Dependencias del proyecto.
- `doc/`: Carpeta que contiene los diagramas técnicos:
    - Flujo del sistema
    - Diagrama de casos de uso
    - Diagrama Entidad-Relación (DER)

## Requisitos
- Docker y Docker Compose instalados.

## Instalación y Ejecución
1. Clonar el repositorio.
2. Abrir la terminal en la carpeta raíz.
3. Ejecutar: `docker compose up --build -d`
4. Acceder en el navegador a: `http://localhost:5000`