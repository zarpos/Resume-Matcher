# Dockerfile simplificado para Resume Matcher
FROM python:3.11-slim

# Instalar dependencias del sistema y Node.js
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Instalar uv para Python
RUN pip install uv

# Configurar directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Configurar backend Python
WORKDIR /app/apps/backend
RUN uv venv && uv pip install .

# Configurar frontend
WORKDIR /app/apps/frontend
RUN npm install

# Configurar dependencias raíz
WORKDIR /app
RUN npm install

# Crear script de inicio que funcione
RUN echo '#!/bin/bash\n\
echo "Iniciando Resume Matcher..."\n\
echo "Backend: http://localhost:8000"\n\
echo "Frontend: http://localhost:3000"\n\
cd /app/apps/backend && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 &\n\
cd /app/apps/frontend && npm run dev -- --hostname 0.0.0.0 &\n\
wait\n\
' > /start.sh && chmod +x /start.sh

# Exponer puertos
EXPOSE 3000 8000

# Comando de inicio
CMD ["/start.sh"]
