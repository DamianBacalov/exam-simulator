#!/bin/bash
# Salir inmediatamente si un comando falla
set -e

echo "Generando nuevos archivos de migración..."
python manage.py makemigrations

echo "Aplicando migraciones a la base de datos..."
python manage.py migrate

echo "Creando superusuario (si no existe)..."
# El comando createsuperuser --noinput leerá estas variables de entorno de Django.
# Usamos "|| true" para que el script no falle si el usuario ya fue creado en arranques anteriores.
python manage.py createsuperuser \
    --noinput \
    --username "$DJANGO_SUPERUSER_USERNAME" \
    --email "$DJANGO_SUPERUSER_EMAIL" || true

echo "Iniciando el servidor de desarrollo..."
# Reemplaza esta línea por Gunicorn (ej. exec gunicorn config.wsgi:application -b 0.0.0.0:8000) si es para producción
exec python manage.py runserver 0.0.0.0:8000