#!/usr/bin/env python3
"""
Script de acceso directo para parar Resume Matcher
Ejecuta el script de limpieza desde la carpeta de automatización
"""

import os
import sys
import subprocess

def main():
    # Obtener la ruta del script de parada
    script_dir = os.path.dirname(os.path.abspath(__file__))
    stop_script = os.path.join(script_dir, 'scripts', 'automation', 'parar_resume_matcher.py')
    
    if not os.path.exists(stop_script):
        print("❌ Error: No se encuentra el script de parada")
        print(f"   Buscando: {stop_script}")
        return 1
    
    # Ejecutar el script de parada
    try:
        subprocess.run([sys.executable, stop_script], check=True)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando el script: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n🛑 Limpieza cancelada por el usuario")
        return 0

if __name__ == "__main__":
    sys.exit(main())
