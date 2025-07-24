#!/usr/bin/env python3
"""
Script de ayuda para Resume Matcher con interfaz mejorada
Proporciona información del estado y comandos útiles
"""

import subprocess
import sys
import threading
import time

class ProgressBar:
    """Clase para mostrar una barra de progreso animada"""
    def __init__(self, description):
        self.description = description
        self.running = False
        self.thread = None
        
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True
        self.thread.start()
        
    def stop(self, success=True):
        self.running = False
        if self.thread:
            self.thread.join()
        
        if success:
            print(f"\r✅ {self.description} - COMPLETADO" + " " * 20)
        else:
            print(f"\r❌ {self.description} - ERROR" + " " * 20)
    
    def _animate(self):
        chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        dots = ""
        while self.running:
            for char in chars:
                if not self.running:
                    break
                dots = "." * ((len(dots) + 1) % 4)
                print(f"\r{char} {self.description}{dots}", end="", flush=True)
                time.sleep(0.1)

def run_command_silent(command):
    """Ejecuta un comando sin mostrar salida"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except:
        return False, "", ""

def check_status_with_progress():
    """Verifica el estado actual del sistema con progreso visual"""
    print("="*60)
    print("📊 VERIFICANDO ESTADO DE RESUME MATCHER")
    print("="*60)
    
    # Verificar Docker
    progress = ProgressBar("Verificando Docker")
    progress.start()
    time.sleep(1)
    success, output, _ = run_command_silent("docker --version")
    if success:
        progress.stop(True)
        print(f"🐳 Docker: ✅ Instalado - {output.strip()}")
    else:
        progress.stop(False)
        print("🐳 Docker: ❌ No disponible")
        return
    
    # Verificar contenedores
    progress = ProgressBar("Verificando contenedores")
    progress.start()
    time.sleep(1)
    success, output, _ = run_command_silent("docker ps --filter name=resume-matcher --format '{{.Names}}\\t{{.Status}}'")
    progress.stop(True)
    
    if output.strip():
        print("📦 Contenedores activos:")
        for line in output.strip().split('\n'):
            if line.strip():
                print(f"   • {line}")
        
        # Verificar puertos
        print("\n🌐 Servicios disponibles:")
        print("   • Frontend: http://localhost:3000")
        print("   • Backend:  http://localhost:8000")
        print("   • API Docs: http://localhost:8000/docs")
    else:
        print("📦 Contenedores: ❌ No hay contenedores ejecutándose")
    
    # Verificar imagen
    progress = ProgressBar("Verificando imagen Docker")
    progress.start()
    time.sleep(0.5)
    success, output, _ = run_command_silent("docker images resume-matcher --format '{{.Repository}}\\t{{.Tag}}\\t{{.Size}}'")
    progress.stop(True)
    
    if output.strip():
        print(f"\n💿 Imagen Docker: ✅ Disponible")
        print(f"   {output.strip()}")
    else:
        print("\n💿 Imagen Docker: ❌ No construida")

def show_help():
    """Muestra ayuda y comandos disponibles"""
    print("\n" + "=" * 60)
    print("📚 AYUDA - RESUME MATCHER")
    print("=" * 60)
    print("\n🚀 SCRIPTS DISPONIBLES:")
    print("   • python iniciar_resume_matcher.py  - Iniciar el proyecto")
    print("   • python parar_resume_matcher.py    - Parar el proyecto")
    print("   • python ayuda_resume_matcher.py    - Mostrar esta ayuda")
    
    print("\n🐳 COMANDOS DOCKER ÚTILES:")
    print("   • docker ps                         - Ver contenedores activos")
    print("   • docker logs resume-matcher-app    - Ver logs del contenedor")
    print("   • docker stop resume-matcher-app    - Parar contenedor")
    print("   • docker start resume-matcher-app   - Reiniciar contenedor")
    print("   • docker images                     - Ver imágenes disponibles")
    
    print("\n🌐 URLS DE ACCESO:")
    print("   • Frontend (Usuario): http://localhost:3000")
    print("   • Backend (API):      http://localhost:8000")
    print("   • API Docs:          http://localhost:8000/docs")
    
    print("\n🔧 SOLUCIÓN DE PROBLEMAS:")
    print("   • Si el puerto está ocupado:")
    print("     - Para el proceso: netstat -ano | findstr :3000")
    print("     - Mata el proceso: taskkill /PID <PID> /F")
    print("   • Si Docker no responde:")
    print("     - Reinicia Docker Desktop")
    print("   • Si hay errores de construcción:")
    print("     - Limpia Docker: docker system prune")

def main():
    check_status_with_progress()
    show_help()
    
    print("\n" + "=" * 60)
    print("¿Qué quieres hacer?")
    print("1. Iniciar Resume Matcher")
    print("2. Parar Resume Matcher") 
    print("3. Ver logs del contenedor")
    print("4. Limpiar Docker (liberar espacio)")
    print("5. Salir")
    
    try:
        choice = input("\nElige una opción (1-5): ").strip()
        
        if choice == "1":
            print("\n🚀 Iniciando Resume Matcher...")
            subprocess.run("python iniciar_resume_matcher.py", shell=True)
        elif choice == "2":
            print("\n🛑 Parando Resume Matcher...")
            subprocess.run("python parar_resume_matcher.py", shell=True)
        elif choice == "3":
            print("\n📄 Mostrando logs...")
            subprocess.run("docker logs resume-matcher-app", shell=True)
            input("\nPresiona Enter para continuar...")
        elif choice == "4":
            response = input("\n⚠️ ¿Estás seguro de limpiar Docker? (s/n): ")
            if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
                print("🧹 Limpiando Docker...")
                subprocess.run("docker system prune -f", shell=True)
                print("✅ Limpieza completada")
            input("\nPresiona Enter para continuar...")
        elif choice == "5":
            print("\n👋 ¡Hasta luego!")
            sys.exit(0)
        else:
            print("❌ Opción no válida")
            
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
        sys.exit(0)

if __name__ == "__main__":
    main()
