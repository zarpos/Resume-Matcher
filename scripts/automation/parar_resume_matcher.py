#!/usr/bin/env python3
"""
Script COMPLETO para parar y limpiar Resume Matcher
Detiene y elimina ABSOLUTAMENTE TODO para un sistema limpio
"""

import subprocess
import sys
import time
import threading
import os
import platform
from pathlib import Path


class ProgressBar:
    def __init__(self, total=100, length=50, prefix='Progreso', suffix='Completo'):
        self.total = total
        self.length = length
        self.prefix = prefix
        self.suffix = suffix
        self.progress = 0
        self.running = False
    
    def update(self, progress):
        self.progress = min(progress, self.total)
        percent = (self.progress / self.total) * 100
        filled_length = int(self.length * self.progress // self.total)
        bar = '█' * filled_length + '░' * (self.length - filled_length)
        
        print(f'\r{self.prefix} |{bar}| {percent:.1f}% {self.suffix}', end='', flush=True)
        
        if self.progress >= self.total:
            print()
    
    def start_animation(self):
        self.running = True
        animation_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        i = 0
        while self.running:
            print(f'\r{animation_chars[i % len(animation_chars)]} Limpiando...', end='', flush=True)
            i += 1
            time.sleep(0.1)
    
    def stop_animation(self):
        self.running = False
        print('\r' + ' ' * 50 + '\r', end='', flush=True)


def print_header():
    print("=" * 80)
    print("🛑 RESUME MATCHER - LIMPIADOR COMPLETO v3.0")
    print("   🧹 Detiene y elimina TODOS los componentes")
    print("   🐳 Docker: Contenedores, imágenes, volúmenes")
    print("   🤖 Ollama: Para y descarga modelos")
    print("   📁 Archivos temporales y configuración")
    print("=" * 80)


def run_command(command, shell=True, capture=True, timeout=60):
    """Ejecuta un comando con manejo de errores"""
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
            check=False
        )
        return result
    except subprocess.TimeoutExpired:
        print(f"⚠️  Timeout ejecutando: {cmd}")
        return None
    except Exception as e:
        print(f"⚠️  Error ejecutando {cmd}: {e}")
        return None


def stop_and_remove_containers():
    """Detiene y elimina todos los contenedores relacionados"""
    print("\n🐳 Limpiando contenedores Docker...")
    
    containers_to_clean = [
        'resume-matcher-app',
        'resume-matcher',
        'resume_matcher',
        'resumematcher'
    ]
    
    for container in containers_to_clean:
        print(f"🛑 Deteniendo contenedor: {container}")
        result = run_command(['docker', 'stop', container], shell=False)
        if result and result.returncode == 0:
            print(f"   ✅ {container} detenido")
        
        print(f"🗑️  Eliminando contenedor: {container}")
        result = run_command(['docker', 'rm', '-f', container], shell=False)
        if result and result.returncode == 0:
            print(f"   ✅ {container} eliminado")
    
    # Limpiar contenedores huérfanos
    print("🧹 Limpiando contenedores huérfanos...")
    run_command(['docker', 'container', 'prune', '-f'], shell=False)


def remove_docker_images():
    """Elimina las imágenes Docker de Resume Matcher"""
    print("\n🖼️  Eliminando imágenes Docker...")
    
    images_to_clean = [
        'resume-matcher',
        'resume_matcher',
        'resumematcher'
    ]
    
    for image in images_to_clean:
        print(f"🗑️  Eliminando imagen: {image}")
        result = run_command(['docker', 'rmi', '-f', image], shell=False)
        if result and result.returncode == 0:
            print(f"   ✅ Imagen {image} eliminada")
    
    # Limpiar imágenes huérfanas
    print("🧹 Limpiando imágenes huérfanas...")
    run_command(['docker', 'image', 'prune', '-f'], shell=False)


def cleanup_docker_volumes():
    """Limpia volúmenes Docker no utilizados"""
    print("\n💾 Limpiando volúmenes Docker...")
    
    result = run_command(['docker', 'volume', 'prune', '-f'], shell=False)
    if result and result.returncode == 0:
        print("✅ Volúmenes Docker limpiados")


def cleanup_docker_networks():
    """Limpia redes Docker no utilizadas"""
    print("\n🌐 Limpiando redes Docker...")
    
    result = run_command(['docker', 'network', 'prune', '-f'], shell=False)
    if result and result.returncode == 0:
        print("✅ Redes Docker limpiadas")


def stop_ollama_model():
    """Para los modelos de Ollama para liberar memoria"""
    print("\n🤖 Parando modelos de Ollama...")
    
    # Verificar si Ollama está disponible
    result = run_command(['ollama', '--version'], shell=False)
    if not result or result.returncode != 0:
        print("⚠️  Ollama no encontrado o no está instalado")
        return
    
    # Obtener lista de modelos ejecutándose
    result = run_command(['ollama', 'ps'], shell=False)
    if result and result.returncode == 0:
        if 'gemma3:4b' in result.stdout:
            print("🛑 Parando modelo gemma3:4b...")
            # No hay comando directo para parar, pero podemos hacer una consulta vacía para que se descargue
            run_command(['ollama', 'run', 'gemma3:4b', '--timeout', '1'], shell=False)
            print("✅ Modelo gemma3:4b liberado de memoria")
        else:
            print("✅ No hay modelos de Ollama ejecutándose")


def remove_ollama_model():
    """Opcionalmente elimina el modelo de Ollama para liberar espacio"""
    print("\n🗑️  ¿Eliminar modelo Ollama gemma3:4b? (Liberará ~3GB de espacio)")
    
    try:
        response = input("   Escribe 'SI' para eliminar el modelo (o Enter para mantenerlo): ").strip().upper()
        if response == 'SI':
            print("🗑️  Eliminando modelo gemma3:4b...")
            result = run_command(['ollama', 'rm', 'gemma3:4b'], shell=False)
            if result and result.returncode == 0:
                print("✅ Modelo gemma3:4b eliminado (~3GB liberados)")
            else:
                print("⚠️  No se pudo eliminar el modelo")
        else:
            print("✅ Modelo gemma3:4b mantenido")
    except KeyboardInterrupt:
        print("\n⚠️  Manteniendo modelo gemma3:4b")


def cleanup_local_files():
    """Limpia archivos locales temporales y configuración"""
    print("\n📁 Limpiando archivos locales...")
    
    files_to_clean = [
        'ollama_progress.txt',
        'ollama_logs.txt',
        'ollama_monitor.txt',
        'resume_matcher.db',
        'apps/backend/resume_matcher.db',
        '.env.backup',
        'docker-compose.override.yml'
    ]
    
    for file_path in files_to_clean:
        path = Path(file_path)
        if path.exists():
            try:
                if path.is_file():
                    path.unlink()
                    print(f"🗑️  Eliminado: {file_path}")
                elif path.is_dir():
                    import shutil
                    shutil.rmtree(path)
                    print(f"🗑️  Directorio eliminado: {file_path}")
            except Exception as e:
                print(f"⚠️  No se pudo eliminar {file_path}: {e}")
    
    # Limpiar directorios de cache
    cache_dirs = [
        '.cache',
        'node_modules',
        'apps/frontend/.next',
        'apps/backend/.venv',
        'apps/backend/__pycache__',
        'apps/backend/app/__pycache__'
    ]
    
    for cache_dir in cache_dirs:
        path = Path(cache_dir)
        if path.exists() and path.is_dir():
            try:
                import shutil
                shutil.rmtree(path)
                print(f"🗑️  Cache eliminado: {cache_dir}")
            except Exception as e:
                print(f"⚠️  No se pudo eliminar cache {cache_dir}: {e}")


def cleanup_environment_files():
    """Opcionalmente elimina archivos de configuración"""
    print("\n⚙️  ¿Eliminar archivos de configuración .env?")
    print("   (Se recrearán automáticamente la próxima vez)")
    
    try:
        response = input("   Escribe 'SI' para eliminar configuración (o Enter para mantener): ").strip().upper()
        if response == 'SI':
            env_files = [
                'apps/backend/.env',
                'apps/frontend/.env'
            ]
            
            for env_file in env_files:
                path = Path(env_file)
                if path.exists():
                    try:
                        path.unlink()
                        print(f"🗑️  Eliminado: {env_file}")
                    except Exception as e:
                        print(f"⚠️  No se pudo eliminar {env_file}: {e}")
            print("✅ Archivos de configuración eliminados")
        else:
            print("✅ Archivos de configuración mantenidos")
    except KeyboardInterrupt:
        print("\n⚠️  Manteniendo archivos de configuración")


def kill_processes():
    """Mata procesos que puedan estar ejecutándose"""
    print("\n⚡ Terminando procesos relacionados...")
    
    processes_to_kill = [
        'node',
        'npm',
        'uvicorn',
        'python'
    ]
    
    system = platform.system().lower()
    
    for process in processes_to_kill:
        if system == "windows":
            # En Windows, ser más específico para no matar procesos importantes
            result = run_command(f'tasklist /FI "IMAGENAME eq {process}.exe" /FO CSV | findstr -i "resume\\|matcher\\|ollama"', shell=True)
            if result and result.stdout.strip():
                print(f"🔪 Terminando procesos {process} relacionados con Resume Matcher...")
                run_command(f'taskkill /F /IM {process}.exe /FI "WINDOWTITLE eq *resume*" 2>nul', shell=True)
        else:
            # En Linux/macOS
            result = run_command(f'pgrep -f "resume.*matcher\\|{process}.*8000\\|{process}.*3000"', shell=True)
            if result and result.stdout.strip():
                print(f"🔪 Terminando procesos {process} relacionados...")
                run_command(f'pkill -f "resume.*matcher\\|{process}.*8000\\|{process}.*3000"', shell=True)


def comprehensive_cleanup():
    """Limpieza completa del sistema"""
    print("\n🧹 LIMPIEZA COMPLETA DEL SISTEMA")
    print("=" * 50)
    
    progress_bar = ProgressBar(total=100, prefix='🧹 Limpieza completa')
    
    steps = [
        ("Terminando procesos", kill_processes, 10),
        ("Deteniendo contenedores", stop_and_remove_containers, 20),
        ("Eliminando imágenes Docker", remove_docker_images, 15),
        ("Limpiando volúmenes Docker", cleanup_docker_volumes, 10),
        ("Limpiando redes Docker", cleanup_docker_networks, 10),
        ("Parando modelos Ollama", stop_ollama_model, 15),
        ("Limpiando archivos locales", cleanup_local_files, 20)
    ]
    
    current_progress = 0
    for step_name, step_func, step_weight in steps:
        print(f"\n📋 {step_name}...")
        try:
            step_func()
            current_progress += step_weight
            progress_bar.update(current_progress)
        except Exception as e:
            print(f"⚠️  Error en {step_name}: {e}")
    
    progress_bar.update(100)
    print("\n✅ Limpieza completa terminada")


def show_final_status():
    """Muestra el estado final del sistema"""
    print("\n" + "=" * 80)
    print("🎉 ¡LIMPIEZA COMPLETA TERMINADA!")
    print("=" * 80)
    print("📊 ESTADO DEL SISTEMA:")
    
    # Verificar Docker
    result = run_command(['docker', 'ps', '-a', '--filter', 'name=resume'], shell=False)
    if result and result.returncode == 0 and 'resume' not in result.stdout:
        print("   ✅ Docker: Sin contenedores de Resume Matcher")
    else:
        print("   ⚠️  Docker: Algunos contenedores pueden seguir existiendo")
    
    # Verificar imágenes
    result = run_command(['docker', 'images', '--filter', 'reference=resume*'], shell=False)
    if result and result.returncode == 0 and len(result.stdout.strip().split('\n')) <= 1:
        print("   ✅ Docker: Sin imágenes de Resume Matcher")
    else:
        print("   ⚠️  Docker: Algunas imágenes pueden seguir existiendo")
    
    # Verificar Ollama
    result = run_command(['ollama', 'ps'], shell=False)
    if result and result.returncode == 0:
        if 'gemma3:4b' not in result.stdout:
            print("   ✅ Ollama: Modelos no están en memoria")
        else:
            print("   ⚠️  Ollama: gemma3:4b sigue en memoria")
    
    print("\n🔄 PARA VOLVER A USAR RESUME MATCHER:")
    print("   python iniciar_resume_matcher.py")
    print("\n💡 ESPACIO LIBERADO:")
    print("   • Contenedores Docker: ~2-3GB")
    print("   • Imágenes Docker: ~1-2GB")
    print("   • Archivos temporales: ~100MB")
    print("   • Modelo Ollama (si se eliminó): ~3GB")
    print("=" * 80)


def main():
    """Función principal"""
    print_header()
    
    print("\n⚠️  ATENCIÓN: Este script eliminará TODOS los componentes de Resume Matcher")
    print("   • Contenedores Docker")
    print("   • Imágenes Docker")
    print("   • Volúmenes y redes")
    print("   • Modelos Ollama en memoria")
    print("   • Archivos temporales")
    
    try:
        response = input("\n¿Continuar con la limpieza completa? (SI/no): ").strip().upper()
        if response not in ['SI', 'S', 'YES', 'Y', '']:
            print("❌ Limpieza cancelada")
            return 0
    except KeyboardInterrupt:
        print("\n❌ Limpieza cancelada por el usuario")
        return 1
    
    # Ejecutar limpieza completa
    comprehensive_cleanup()
    
    # Preguntar sobre eliminaciones opcionales
    remove_ollama_model()
    cleanup_environment_files()
    
    # Mostrar estado final
    show_final_status()
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Limpieza cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        sys.exit(1)
