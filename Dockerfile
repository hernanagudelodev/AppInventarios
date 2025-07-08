# Imagen base ligera con Python 3.12
FROM python:3.12-slim

# Dependencias de sistema para WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential libcairo2 pango1.0-tools libpango-1.0-0 \
        libgdk-pixbuf2.0-0 libffi-dev fonts-dejavu-core && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código de la app
COPY . .

# ---------- Variables disponibles en build ----------
ARG SECRET_KEY
ARG DATABASE_URL
ENV SECRET_KEY=${SECRET_KEY:-build-time-key}
ENV DATABASE_URL=${DATABASE_URL:-sqlite:///build.db}

# ---------- Collectstatic ----------
RUN python manage.py collectstatic --noinput

# ---------- Arranque ----------
CMD ["sh","-c","gunicorn inventarios.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3 --timeout 120"]
