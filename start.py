#!/usr/bin/env python3
"""
Script de acceso directo para iniciar Resume Matcher
Ejecuta el script principal desde la carpeta de automatización
"""

import os
import sys
import subprocess

def main():
    # Obtener la ruta del script principal
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(script_dir, 'scripts', 'automation', 'iniciar_resume_matcher.py')
    
    if not os.path.exists(main_script):
        print("❌ Error: No se encuentra el script principal")
        print(f"   Buscando: {main_script}")
        return 1
    
    # Ejecutar el script principal
    try:
        subprocess.run([sys.executable, main_script], check=True)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando el script: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n🛑 Instalación cancelada por el usuario")
        return 0

if __name__ == "__main__":
    sys.exit(main())
