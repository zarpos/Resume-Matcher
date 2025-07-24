#!/usr/bin/env python3
"""
Prueba rápida de la verificación de modelos de Ollama
"""

import subprocess
import sys
import os

# Agregar el directorio de scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'automation'))

from iniciar_resume_matcher import check_and_install_ollama

def test_ollama_check():
    """Prueba la función de verificación de Ollama"""
    print("🧪 Probando verificación de modelos de Ollama...")
    print("=" * 50)
    
    result = check_and_install_ollama()
    
    print("=" * 50)
    if result:
        print("✅ Prueba exitosa: Todos los modelos están disponibles")
        
        # Mostrar estado actual
        print("\n📊 Estado actual de los modelos:")
        try:
            result = subprocess.run(
                ['ollama', 'list'], 
                capture_output=True, 
                text=True, 
                check=False
            )
            if result.returncode == 0:
                print(result.stdout)
            else:
                print("❌ Error obteniendo lista de modelos")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("❌ Prueba fallida: Hay problemas con la configuración de Ollama")

if __name__ == "__main__":
    test_ollama_check()
