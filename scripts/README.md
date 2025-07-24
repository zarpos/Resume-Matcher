# 📁 Scripts Personalizados de Resume Matcher

Esta carpeta contiene scripts adicionales creados para facilitar la instalación, configuración y mantenimiento de Resume Matcher con Docker y Ollama.

## 📂 Estructura de Carpetas

### 🚀 `/automation` - Scripts de Automatización
Scripts para instalación y gestión automática del proyecto.

- **`iniciar_resume_matcher.py`** - Script principal de instalación y configuración
  - ✅ Verifica e instala Docker Desktop
  - ✅ Verifica e instala Ollama
  - ✅ Descarga modelos necesarios (gemma3:4b + nomic-embed-text)
  - ✅ Construye imagen Docker
  - ✅ Inicia contenedores
  - ✅ Verificación completa de servicios

- **`parar_resume_matcher.py`** - Script de limpieza completa
  - 🛑 Detiene todos los contenedores
  - 🗑️ Elimina imágenes Docker
  - 🧹 Limpia volúmenes y redes
  - 🤖 Gestiona modelos Ollama
  - 📁 Limpia archivos temporales

### 🔧 `/maintenance` - Scripts de Mantenimiento
Scripts para mantener el sistema funcionando correctamente.

- **`mantener_ollama_activo.py`** - Mantiene modelos Ollama en memoria
  - 🤖 Previene timeouts de modelos
  - ⏰ Ping cada 3 minutos
  - 🔄 Mantiene gemma3:4b activo
  - 💾 Evita recargas de modelos

### 🧪 `/testing` - Scripts de Pruebas
Scripts para verificar que todo funciona correctamente.

- **`test_ollama_check.py`** - Prueba la verificación de modelos
  - ✅ Verifica instalación de Ollama
  - ✅ Verifica modelos necesarios
  - 📊 Muestra estado del sistema

## 🚀 Uso Rápido

### Iniciar Todo el Sistema
```bash
python scripts/automation/iniciar_resume_matcher.py
```

### Mantener Modelos Activos (opcional)
```bash
python scripts/maintenance/mantener_ollama_activo.py
```

### Detener y Limpiar Todo
```bash
python scripts/automation/parar_resume_matcher.py
```

## 📋 Requisitos

- Python 3.8+
- Windows 10/11
- Conexión a Internet (para descargas)
- Al menos 8GB RAM disponible (para modelos Ollama)
- 10GB espacio en disco

## 🔧 Configuración Automática

Los scripts manejan automáticamente:
- ✅ Instalación de Docker Desktop
- ✅ Instalación de Ollama
- ✅ Descarga de modelos LLM
- ✅ Configuración de red Docker
- ✅ Variables de entorno
- ✅ Verificación de puertos

## 🐛 Solución de Problemas

Si algo no funciona:
1. Ejecuta `test_ollama_check.py` para diagnóstico
2. Revisa logs con `docker logs resume-matcher-app`
3. Verifica modelos con `ollama list`
4. Reinicia todo con el script de parada + inicio

## 📞 Soporte

Los scripts incluyen verificación completa y mensajes de error detallados para facilitar la resolución de problemas.
