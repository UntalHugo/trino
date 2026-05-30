FROM python:3.12-slim

# Evita que Python escriba archivos .pyc y que bufferee stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema necesarias para psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependencias de Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia todo el proyecto al contenedor
COPY . .

# Puerto que expone Django
EXPOSE 8000

# Comando por defecto: levanta el servidor de desarrollo
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
