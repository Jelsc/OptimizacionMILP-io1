# Imagen ligera de Python. Usa 3.12-slim hasta que 3.13 esté disponible
FROM python:3.12-slim

# Evita byte-code y mantiene salida interactiva
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código y la BD
COPY . .

# Puerto de Streamlit
EXPOSE 8501

CMD ["streamlit", "run", "interface/streamlit_app.py", \
     "--server.port=8501", "--server.address=0.0.0.0"]
