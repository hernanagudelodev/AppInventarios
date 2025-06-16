# Imagen base ligera con Python 3.12
FROM python:3.12-slim

# Instala las dependencias de sistema que WeasyPrint necesita
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libcairo2 \
        pango1.0-tools \
        libpango-1.0-0 \
        libgdk-pixbuf2.0-0 \
        libffi-dev \
        fonts-dejavu-core && \
    rm -rf /var/lib/apt/lists/*

# Carpeta de trabajo
WORKDIR /app

# Instala dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código de la app
COPY . .

# -----------------------------
# Variables necesarias en build
# -----------------------------
# 1) Decláralas como argumentos:
ARG SECRET_KEY
ARG DATABASE_URL

# 2) Expónlas como variables de entorno,
#    con un fallback si vienen vacías:
ENV SECRET_KEY=${SECRET_KEY:-build-time-key}
ENV DATABASE_URL=${DATABASE_URL:-sqlite:///build.db}

# -----------------------------
# Recolecta los estáticos
# -----------------------------
RUN python manage.py collectstatic --noinput

# Arranca Gunicorn (Railway expone la variable $PORT)
CMD ["sh", "-c", "gunicorn inventarios.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]

