# ---- Base Stage ----
FROM python:3.10-slim as base

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código del proyecto
COPY . .


# ---- Test Stage ----
# Esta etapa ejecutará las pruebas. Si las pruebas fallan, 
# la construcción de la imagen de Docker se detendrá y fallará.
FROM base as test

# Inyectamos variables de entorno ficticias necesarias para que 
# la configuración cargue correctamente durante las pruebas.
ENV DB_HOST=localhost \
    DB_PORT=3306 \
    DB_USER=test \
    DB_PASSWORD=test \
    DB_NAME=test \
    SECRET_KEY=testsecret \
    ALGORITHM=HS256

# Corremos la suite de pruebas
RUN pytest tests/ -v


# ---- Production Stage ----
# Esta es la imagen final que se usará para correr la aplicación.
# Se basa en la etapa 'base', ignorando todo lo de 'test' para mantenerla limpia.
FROM base as production

# Exponer el puerto por defecto de FastAPI
EXPOSE 8000

# Comando para arrancar el servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
