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

# Copia el resto del código
COPY . .

# Arranca Gunicorn (Railway expone la variable $PORT)
CMD ["gunicorn", "inventarios.wsgi:application", "--bind", "0.0.0.0:${PORT}"]
