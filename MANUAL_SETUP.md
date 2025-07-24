# Manual Setup Guide for Resume Matcher (Windows)

Este archivo contiene los pasos manuales para instalar Resume Matcher en Windows sin ejecutar scripts de PowerShell.

## Prerrequisitos

1. **Node.js** >= v18 (https://nodejs.org/)
2. **Python** >= 3.8 (https://python.org/)
3. **Git** (https://git-scm.com/)

## Pasos de Instalación Manual

### 1. Instalar uv (Python package manager)
```cmd
pip install uv
```

### 2. Instalar dependencias del Frontend
```cmd
cd apps\frontend
npm install
cd ..\..
```

### 3. Configurar el Backend Python
```cmd
cd apps\backend
uv venv
uv pip install .
cd ..\..
```

### 4. Instalar dependencias raíz
```cmd
npm install
```

## Ejecutar el Proyecto

### Desarrollo (ambos servicios)
```cmd
npm run dev
```

### Solo Frontend
```cmd
npm run dev:frontend
```

### Solo Backend
```cmd
npm run dev:backend
```

### Producción
```cmd
npm run build
npm run start
```

## Puertos

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Troubleshooting

Si tienes problemas con uv, puedes usar pip directamente:
```cmd
cd apps\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
