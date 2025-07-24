#!/usr/bin/env python3
"""
Script COMPLETO para iniciar Resume Matcher
Verifica e instala todo lo necesario automáticamente
"""

import subprocess
import sys
import time
import json
import requests
import os
import platform
from pathlib import Path


def print_header():
    print("=" * 80)
    print("🚀 RESUME MATCHER - CONFIGURADOR AUTOMÁTICO COMPLETO v3.0")
    print("   ✅ Verificación completa de dependencias")
    print("   🔧 Instalación automática de componentes faltantes")
    print("   🐳 Docker + Ollama + Frontend + Backend")
    print("=" * 80)


def run_command(command, shell=True, capture=True, timeout=300):
    """Ejecuta un comando con manejo de errores mejorado"""
    try:
        if isinstance(command, str):
            cmd = command
        else:
            cmd = ' '.join(command) if shell else command
            
        result = subprocess.run(
            cmd if shell else command,
            shell=shell,
            capture_output=capture,
            text=True,
            timeout=timeout,
            check=False,
            encoding='utf-8',
            errors='replace'
        )
        return result
    except subprocess.TimeoutExpired:
        print(f"❌ Timeout ejecutando: {cmd}")
        return None
    except Exception as e:
        print(f"❌ Error ejecutando {cmd}: {e}")
        return None


def check_and_install_docker():
    """Verifica e instala Docker si es necesario"""
    print("\n🐳 Verificando Docker...")
    
    # Verificar si Docker está instalado
    result = run_command(['docker', '--version'], shell=False)
    if result and result.returncode == 0:
        print("✅ Docker encontrado:", result.stdout.strip())
        
        # Verificar que Docker Desktop esté ejecutándose
        result = run_command(['docker', 'info'], shell=False)
        if result and result.returncode == 0:
            print("✅ Docker Desktop está ejecutándose")
            return True
        else:
            print("⚠️  Docker está instalado pero Docker Desktop no está ejecutándose")
            print("   Por favor inicia Docker Desktop y vuelve a ejecutar este script")
            return False
    else:
        print("❌ Docker no encontrado")
        print("📥 Descargando e instalando Docker Desktop...")
        
        system = platform.system().lower()
        if system == "windows":
            download_url = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
            print(f"   Descarga Docker Desktop desde: {download_url}")
        elif system == "darwin":  # macOS
            download_url = "https://desktop.docker.com/mac/main/amd64/Docker.dmg"
            print(f"   Descarga Docker Desktop desde: {download_url}")
        else:  # Linux
            print("   Para Linux, ejecuta: curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh")
        
        print("   Después de instalar Docker Desktop, reinicia este script")
        return False


def check_and_install_ollama():
    """Verifica e instala Ollama si es necesario"""
    print("\n🤖 Verificando Ollama...")
    
    # Verificar si Ollama está instalado
    result = run_command(['ollama', '--version'], shell=False)
    if result and result.returncode == 0:
        print("✅ Ollama encontrado:", result.stdout.strip())
        
        # Verificar si Ollama está ejecutándose
        result = run_command(['ollama', 'list'], shell=False)
        if result and result.returncode == 0:
            print("✅ Ollama está ejecutándose")
            
            # Verificar si ambos modelos están instalados
            models_output = result.stdout
            has_gemma = 'gemma3:4b' in models_output
            has_embeddings = 'nomic-embed-text' in models_output
            
            if has_gemma and has_embeddings:
                print("✅ Todos los modelos necesarios están instalados")
                print("   - gemma3:4b ✅")
                print("   - nomic-embed-text ✅")
                return True
            else:
                missing_models = []
                if not has_gemma:
                    missing_models.append("gemma3:4b")
                if not has_embeddings:
                    missing_models.append("nomic-embed-text")
                
                print(f"⚠️  Modelos faltantes: {', '.join(missing_models)}")
                print("   Descargando modelos necesarios...")
                return install_ollama_model()
        else:
            print("⚠️  Ollama instalado pero no está ejecutándose")
            print("   Iniciando Ollama...")
            return start_ollama()
    else:
        print("❌ Ollama no encontrado")
        return install_ollama()


def install_ollama():
    """Instala Ollama automáticamente"""
    print("📥 Instalando Ollama...")
    
    system = platform.system().lower()
    if system == "windows":
        # Para Windows, descargar el instalador
        download_url = "https://ollama.com/download/windows"
        print(f"   Descarga Ollama desde: {download_url}")
        print("   O ejecuta en PowerShell: winget install Ollama.Ollama")
        
        try:
            result = run_command("winget install Ollama.Ollama", timeout=600)
            if result and result.returncode == 0:
                print("✅ Ollama instalado correctamente")
                time.sleep(5)  # Esperar a que se inicie
                return install_ollama_model()
            else:
                print("⚠️  Instala Ollama manualmente desde https://ollama.com/download")
                return False
        except:
            print("⚠️  Por favor instala Ollama manualmente desde https://ollama.com/download")
            return False
    
    elif system == "darwin":  # macOS
        result = run_command("curl -fsSL https://ollama.com/install.sh | sh", timeout=600)
        if result and result.returncode == 0:
            print("✅ Ollama instalado correctamente")
            return install_ollama_model()
    
    else:  # Linux
        result = run_command("curl -fsSL https://ollama.com/install.sh | sh", timeout=600)
        if result and result.returncode == 0:
            print("✅ Ollama instalado correctamente")
            return install_ollama_model()
    
    print("⚠️  Por favor instala Ollama manualmente desde https://ollama.com/download")
    return False


def start_ollama():
    """Inicia el servicio de Ollama"""
    print("🔄 Iniciando Ollama...")
    
    system = platform.system().lower()
    if system == "windows":
        # En Windows, Ollama se inicia automáticamente
        time.sleep(5)
        result = run_command(['ollama', 'list'], shell=False)
        if result and result.returncode == 0:
            print("✅ Ollama iniciado correctamente")
            return install_ollama_model()
    
    return False


def install_ollama_model():
    """Instala los modelos necesarios: gemma3:4b y nomic-embed-text"""
    print("📦 Instalando modelos de Ollama...")
    print("   (Esto puede tomar varios minutos)")
    print()
    
    # Verificar modelos existentes
    result = run_command(['ollama', 'list'], shell=False)
    if not result or result.returncode != 0:
        print("❌ Error verificando modelos de Ollama")
        return False
    
    models_output = result.stdout
    has_gemma = 'gemma3:4b' in models_output
    has_embeddings = 'nomic-embed-text' in models_output
    
    # Instalar gemma3:4b si no existe
    if not has_gemma:
        print("📥 Descargando modelo gemma3:4b...")
        try:
            result = subprocess.run(
                ['ollama', 'pull', 'gemma3:4b'],
                check=False,
                encoding='utf-8',
                errors='ignore'
            )
            if result.returncode != 0:
                print("❌ Error descargando gemma3:4b")
                return False
            print("✅ Modelo gemma3:4b instalado")
        except Exception as e:
            print(f"❌ Error instalando gemma3:4b: {e}")
            return False
    else:
        print("✅ Modelo gemma3:4b ya está instalado")
    
    # Instalar modelo de embeddings si no existe
    if not has_embeddings:
        print("📥 Descargando modelo de embeddings...")
        try:
            result = subprocess.run(
                ['ollama', 'pull', 'nomic-embed-text:137m-v1.5-fp16'],
                check=False,
                encoding='utf-8',
                errors='ignore'
            )
            if result.returncode != 0:
                print("❌ Error descargando modelo de embeddings")
                return False
            print("✅ Modelo de embeddings instalado")
        except Exception as e:
            print(f"❌ Error instalando modelo de embeddings: {e}")
            return False
    else:
        print("✅ Modelo de embeddings ya está instalado")
    
    # Cargar modelo principal en memoria
    print("🔄 Cargando modelo en memoria...")
    try:
        result = subprocess.run(
            ['ollama', 'run', 'gemma3:4b', 'test'],
            capture_output=True,
            check=False,
            encoding='utf-8',
            errors='ignore'
        )
        if result.returncode == 0:
            print("✅ Modelo cargado en memoria")
        else:
            print("⚠️  Modelo instalado pero no se pudo cargar en memoria")
    except Exception as e:
        print(f"⚠️  Error cargando modelo: {e}")
    
    return True


def check_curl():
    """Verifica si curl está disponible"""
    result = run_command(['curl', '--version'], shell=False)
    if result and result.returncode == 0:
        print("✅ curl encontrado")
        return True
    else:
        print("❌ curl no encontrado - necesario para verificaciones")
        print("   Instala curl desde: https://curl.se/download.html")
        return False


def stop_existing_container():
    """Detiene y elimina el contenedor existente si existe"""
    print("\n🧹 Limpiando contenedores existentes...")
    
    # Detener contenedor
    result = run_command(['docker', 'stop', 'resume-matcher-app'], shell=False)
    if result and result.returncode == 0:
        print("🛑 Contenedor existente detenido")
    
    # Eliminar contenedor
    result = run_command(['docker', 'rm', 'resume-matcher-app'], shell=False)
    if result and result.returncode == 0:
        print("🗑️  Contenedor existente eliminado")


def verify_environment_files():
    """Verifica y crea archivos de configuración necesarios"""
    print("\n📋 Verificando archivos de configuración...")
    
    backend_env = Path("apps/backend/.env")
    frontend_env = Path("apps/frontend/.env")
    
    # Crear .env del backend si no existe
    if not backend_env.exists():
        print("📝 Creando apps/backend/.env...")
        backend_env_content = """# Base de datos SQLite para desarrollo local
SYNC_DATABASE_URL=sqlite:///./resume_matcher.db
ASYNC_DATABASE_URL=sqlite+aiosqlite:///./resume_matcher.db

# Clave secreta para sesiones
SESSION_SECRET_KEY=dev-secret-key-change-in-production-123456789

# Configuración de Ollama para Docker
OLLAMA_BASE_URL=http://host.docker.internal:11434

# Configuración de desarrollo
DB_ECHO=true
"""
        backend_env.write_text(backend_env_content)
        print("✅ apps/backend/.env creado")
    else:
        print("✅ apps/backend/.env existe")
    
    # Crear .env del frontend si no existe
    if not frontend_env.exists():
        print("📝 Creando apps/frontend/.env...")
        frontend_env_content = """# URL de la API del backend
NEXT_PUBLIC_API_URL=http://localhost:8000
"""
        frontend_env.write_text(frontend_env_content)
        print("✅ apps/frontend/.env creado")
    else:
        print("✅ apps/frontend/.env existe")


def run_docker_build_with_progress():
    """Ejecuta docker build mostrando el progreso real de Docker"""
    print("\n🔨 Construyendo imagen Docker...")
    print("   (Esto puede tomar varios minutos)")
    print()
    
    try:
        start_time = time.time()
        result = subprocess.run(
            ['docker', 'build', '-t', 'resume-matcher', '.'],
            check=False,
            encoding='utf-8',
            errors='ignore'
        )
        
        elapsed_time = time.time() - start_time
        
        if result.returncode == 0:
            print(f"\n✅ Imagen Docker construida correctamente en {elapsed_time:.1f}s")
            return True
        else:
            print(f"\n❌ Error construyendo imagen Docker (código: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"\n❌ Error construyendo imagen: {e}")
        return False


def start_container():
    """Inicia el contenedor de Resume Matcher"""
    print("\n🚀 Iniciando contenedor...")
    
    try:
        result = subprocess.run([
            'docker', 'run', '-d',
            '-p', '3000:3000',
            '-p', '8000:8000',
            '--add-host=host.docker.internal:host-gateway',
            '--name', 'resume-matcher-app',
            'resume-matcher'
        ], capture_output=True, text=True, check=True)
        
        container_id = result.stdout.strip()
        print(f"✅ Contenedor iniciado: {container_id[:12]}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error iniciando contenedor: {e}")
        return False


def comprehensive_service_check():
    """Verificación completa de todos los servicios"""
    print("\n🔍 VERIFICACIÓN COMPLETA DE SERVICIOS")
    print("=" * 50)
    
    max_attempts = 60  # 3 minutos máximo
    backend_ready = False
    frontend_ready = False
    ollama_connected = False
    
    for attempt in range(max_attempts):
        print(f"\n🔄 Verificación {attempt + 1}/{max_attempts}")
        
        # 1. Verificar Backend
        if not backend_ready:
            try:
                response = requests.get('http://localhost:8000/ping', timeout=5)
                if response.status_code == 200 and 'pong' in response.text:
                    print("✅ Backend API respondiendo correctamente")
                    backend_ready = True
                else:
                    print(f"⏳ Backend API: Status {response.status_code}")
            except:
                print("⏳ Backend API: No responde aún")
        
        # 2. Verificar Frontend
        if not frontend_ready:
            try:
                response = requests.get('http://localhost:3000', timeout=5)
                if response.status_code == 200:
                    print("✅ Frontend cargando correctamente")
                    frontend_ready = True
                else:
                    print(f"⏳ Frontend: Status {response.status_code}")
            except:
                print("⏳ Frontend: No responde aún")
        
        # 3. Verificar conexión Backend-Ollama
        if backend_ready and not ollama_connected:
            try:
                # Verificar que el backend puede acceder a Ollama
                result = run_command(['docker', 'exec', 'resume-matcher-app', 'curl', '-s', 'http://host.docker.internal:11434/api/tags'], shell=False)
                if result and result.returncode == 0 and 'gemma3:4b' in result.stdout:
                    print("✅ Backend conectado a Ollama correctamente")
                    ollama_connected = True
                else:
                    print("⏳ Backend-Ollama: Verificando conexión...")
            except:
                print("⏳ Backend-Ollama: Verificando conexión...")
        
        # Si todo está listo, salir
        if backend_ready and frontend_ready and ollama_connected:
            print("\n🎉 ¡TODOS LOS SERVICIOS ESTÁN FUNCIONANDO!")
            return True
        
        time.sleep(3)
    
    # Mostrar estado final si no todo está listo
    print("\n⚠️  ESTADO FINAL DE SERVICIOS:")
    print(f"   Backend API: {'✅ Listo' if backend_ready else '❌ No listo'}")
    print(f"   Frontend: {'✅ Listo' if frontend_ready else '❌ No listo'}")
    print(f"   Backend-Ollama: {'✅ Conectado' if ollama_connected else '❌ No conectado'}")
    
    return backend_ready and frontend_ready


def show_final_info():
    """Muestra información final y comandos útiles"""
    print("\n" + "=" * 80)
    print("🎉 ¡RESUME MATCHER CONFIGURADO Y EJECUTÁNDOSE!")
    print("=" * 80)
    print("🌐 ACCESOS:")
    print("   📱 Frontend: http://localhost:3000")
    print("   🔧 Backend API: http://localhost:8000")
    print("   📚 Documentación API: http://localhost:8000/api/docs")
    print("   🔍 Health Check: http://localhost:8000/ping")
    print("\n💾 ARCHIVOS DE CONFIGURACIÓN:")
    print("   📋 Backend: apps/backend/.env")
    print("   📋 Frontend: apps/frontend/.env")
    print("\n🛠️  COMANDOS ÚTILES:")
    print("   📊 Ver logs: docker logs -f resume-matcher-app")
    print("   🔄 Reiniciar: docker restart resume-matcher-app")
    print("   🛑 Detener: python parar_resume_matcher.py")
    print("   🤖 Estado Ollama: ollama ps")
    print("=" * 80)
    print("💡 TIP: Si algo no funciona, ejecuta 'python parar_resume_matcher.py' y luego este script otra vez")
    print("=" * 80)


def main():
    """Función principal"""
    print_header()
    
    # 1. Verificar e instalar Docker
    if not check_and_install_docker():
        print("\n❌ No se puede continuar sin Docker")
        return 1
    
    # 2. Verificar curl
    if not check_curl():
        print("\n⚠️  curl no encontrado - algunas verificaciones pueden fallar")
    
    # 3. Verificar e instalar Ollama
    if not check_and_install_ollama():
        print("\n❌ No se puede continuar sin Ollama")
        return 1
    
    # 4. Verificar archivos de configuración
    verify_environment_files()
    
    # 5. Limpiar contenedores existentes
    stop_existing_container()
    
    # 6. Construir imagen Docker
    if not run_docker_build_with_progress():
        print("\n❌ Error construyendo imagen Docker")
        return 1
    
    # 7. Iniciar contenedor
    if not start_container():
        print("\n❌ Error iniciando contenedor")
        return 1
    
    # 8. Verificación completa de servicios
    if not comprehensive_service_check():
        print("\n⚠️  Algunos servicios pueden no estar completamente listos")
        print("   Pero el sistema debería funcionar. Verifica manualmente las URLs.")
    
    # 9. Mostrar información final
    show_final_info()
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Instalación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        sys.exit(1)
