FROM python:3.11-slim

WORKDIR /app

# 1. Evitamos archivos basura y forzamos logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 2. IMPORTANTE: Ponemos el radar de Python en /app para que 
# encuentre la carpeta 'backend' y los imports funcionen.
ENV PYTHONPATH=/app

# Instalación de dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3. Instalamos dependencias (asumiendo que requirements.txt está en ./backend/)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. CAMBIO CLAVE: Copiamos el contenido en una subcarpeta llamada 'backend'
# Así, el archivo main.py estará en /app/backend/main.py
COPY . ./backend

# 5. Creamos la carpeta de persistencia
RUN mkdir -p /app/backend/data && chmod 777 /app/backend/data

EXPOSE 8000

# 6. Nos movemos a la subcarpeta para que Uvicorn vea el archivo main.py
WORKDIR /app/backend

# Al ejecutar main:app desde aquí, Python buscará 'backend.state' y lo 
# encontrará porque estamos dentro de /app y el PYTHONPATH apunta a /app.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]