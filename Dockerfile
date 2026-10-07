# 1. Usar una versión de Python más reciente y anclada a Debian Bookworm
FROM python:3.12-slim-bookworm

# 2. Configurar variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Crear un usuario y grupo del sistema sin privilegios
RUN groupadd --system django && \
    useradd --system -g django -d /app django

# 4. Establecer el directorio de trabajo y asegurar sus permisos
RUN mkdir -p /app && chown django:django /app
WORKDIR /app

# 5. Actualizar el SO base para parchar vulnerabilidades críticas (CVEs)
# y limpiar la caché para mantener la imagen ligera.
# Si en el futuro necesitas dependencias del sistema (ej. Postgres con libpq5),
# puedes instalarlas con apt-get install -y --no-install-recommends <paquetes>
RUN apt-get update && apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# 6. Instalar dependencias de Python
COPY --chown=django:django requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 7. Copiar el código del proyecto
COPY --chown=django:django . /app/

# 8. Dar permisos al entrypoint y asegurar la propiedad de los archivos al usuario 'django'
RUN sed -i 's/\r$//' /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh && \
    chown -R django:django /app

# 9. Cambiar del usuario root al usuario seguro
USER django

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]