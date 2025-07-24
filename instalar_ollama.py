#!/usr/bin/env python3
"""
Script para instalar y configurar Ollama para Resume Matcher
"""

import subprocess
import sys
import time
import threading

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
            print(f"\r✅ {self.description} - COMPLETADO" + " " * 30)
        else:
            print(f"\r❌ {self.description} - ERROR" + " " * 30)
    
    def _animate(self):
        chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        dots = ""
        char_index = 0
        
        while self.running:
            char = chars[char_index % len(chars)]
            char_index += 1
            dots = "." * ((len(dots) + 1) % 4)
            print(f"\r{char} {self.description}{dots}", end="", flush=True)
            time.sleep(0.15)

def run_command_with_progress(command, description):
    """Ejecuta un comando con barra de progreso"""
    progress = ProgressBar(description)
    progress.start()
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            progress.stop(True)
            return True, result.stdout
        else:
            progress.stop(False)
            print(f"\n❌ Error: {result.stderr}")
            return False, result.stderr
    except subprocess.TimeoutExpired:
        progress.stop(False)
        print(f"\n⏰ Timeout ejecutando comando")
        return False, "Timeout"
    except Exception as e:
        progress.stop(False)
        print(f"\n❌ Error: {e}")
        return False, str(e)

def check_ollama():
    """Verifica si Ollama está instalado"""
    try:
        result = subprocess.run("ollama --version", shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip()
    except:
        return False, ""

def install_ollama():
    """Instala Ollama en Windows"""
    print("🤖 INSTALANDO OLLAMA")
    print("="*50)
    
    # Verificar si ya está instalado
    is_installed, version = check_ollama()
    if is_installed:
        print(f"✅ Ollama ya está instalado: {version}")
        return True
    
    print("📥 Descargando Ollama para Windows...")
    print("💡 Se abrirá la página de descarga en tu navegador")
    print("📋 Sigue estos pasos:")
    print("   1. Descarga el instalador de Windows")
    print("   2. Ejecuta el archivo .exe descargado")
    print("   3. Sigue el asistente de instalación")
    print("   4. Reinicia esta aplicación después de la instalación")
    
    try:
        import webbrowser
        webbrowser.open("https://ollama.ai/download")
        print("🌐 Página de descarga abierta en el navegador")
    except:
        print("❌ No se pudo abrir el navegador automáticamente")
        print("🔗 Ve manualmente a: https://ollama.ai/download")
    
    input("\nPresiona Enter después de instalar Ollama...")
    
    # Verificar instalación
    is_installed, version = check_ollama()
    if is_installed:
        print(f"✅ Ollama instalado correctamente: {version}")
        return True
    else:
        print("❌ Ollama no se detectó. Asegúrate de que esté instalado y en PATH")
        return False

def start_ollama_service():
    """Inicia el servicio de Ollama"""
    print("\n🚀 INICIANDO SERVICIO OLLAMA")
    print("="*50)
    
    success, _ = run_command_with_progress("ollama serve", "Iniciando servicio Ollama (en background)")
    if success:
        print("✅ Servicio Ollama iniciado")
        return True
    else:
        print("⚠️ El servicio puede que ya esté ejecutándose")
        return True  # Continuamos aunque falle

def download_model():
    """Descarga el modelo necesario para Resume Matcher"""
    print("\n📦 DESCARGANDO MODELO DE IA")
    print("="*50)
    print("⚠️ Esta descarga puede tardar 10-30 minutos dependiendo de tu conexión")
    print("📦 Tamaño del modelo: ~2.4GB")
    
    # Usar el modelo específico requerido por Resume Matcher
    model = "gemma3:4b"  # Modelo específico usado en el código del proyecto
    
    success, output = run_command_with_progress(f"ollama pull {model}", f"Descargando modelo {model}")
    if success:
        print(f"✅ Modelo {model} descargado exitosamente")
        return True
    else:
        print(f"❌ Error descargando modelo {model}")
        print("💡 Puedes intentar más tarde con: ollama pull gemma3:4b")
        return False

def main():
    print("="*60)
    print("🤖 CONFIGURACIÓN DE OLLAMA PARA RESUME MATCHER")
    print("="*60)
    print("Ollama es necesario para las funciones de IA del proyecto")
    print("Este script te ayudará a instalarlo y configurarlo.\n")
    
    # Paso 1: Verificar/Instalar Ollama
    if not install_ollama():
        input("❌ Instalación fallida. Presiona Enter para salir...")
        sys.exit(1)
    
    # Paso 2: Iniciar servicio
    if not start_ollama_service():
        print("⚠️ Hubo problemas iniciando el servicio")
    
    # Paso 3: Descargar modelo
    print("\n¿Quieres descargar un modelo de IA ahora?")
    print("(Puedes hacer esto más tarde si prefieres)")
    choice = input("(s/n): ").lower()
    
    if choice in ['s', 'si', 'sí', 'y', 'yes']:
        download_model()
    
    print("\n" + "="*60)
    print("🎉 CONFIGURACIÓN DE OLLAMA COMPLETADA")
    print("="*60)
    print("✅ Ollama está listo para usar con Resume Matcher")
    print("\n📋 COMANDOS ÚTILES:")
    print("   • Ver modelos:     ollama list")
    print("   • Descargar modelo: ollama pull llama3.2:1b")
    print("   • Estado servicio: ollama ps")
    print("="*60)
    
    input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
