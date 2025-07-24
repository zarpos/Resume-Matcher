#!/usr/bin/env python3
"""
Script para mantener los modelos de Ollama activos en memoria
Previene timeouts durante el uso de Resume Matcher
"""

import subprocess
import time
import sys

def keep_models_active():
    """Mantiene los modelos activos enviando requests periódicos"""
    print("🤖 Manteniendo modelos de Ollama activos...")
    print("   Presiona Ctrl+C para detener")
    
    try:
        while True:
            # Hacer ping al modelo principal cada 3 minutos
            try:
                subprocess.run(
                    ['ollama', 'run', 'gemma3:4b', 'ping'],
                    capture_output=True,
                    timeout=30,
                    check=False
                )
                print(f"✅ {time.strftime('%H:%M:%S')} - Modelo activo")
            except Exception as e:
                print(f"⚠️  {time.strftime('%H:%M:%S')} - Error: {e}")
            
            # Esperar 3 minutos antes del siguiente ping
            time.sleep(180)
            
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo mantenimiento de modelos...")
        sys.exit(0)

if __name__ == "__main__":
    keep_models_active()
