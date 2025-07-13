#!/usr/bin/env python3
"""
Script para iniciar os servidores Django e FastAPI simultaneamente
"""
import subprocess
import sys
import time
import os
from pathlib import Path

def start_django():
    """Inicia o servidor Django"""
    print("🚀 Iniciando servidor Django na porta 8000...")
    return subprocess.Popen([
        sys.executable, "manage.py", "runserver", "8000"
    ])

def start_fastapi():
    """Inicia o servidor FastAPI"""
    print("🚀 Iniciando servidor FastAPI na porta 8001...")
    return subprocess.Popen([
        sys.executable, "-m", "uvicorn", "realtime_server:app", "--host", "0.0.0.0", "--port", "8001", "--reload"
    ])

def main():
    print("🔄 Iniciando servidores RequisitaFácil...")
    print("=" * 50)
    
    # Verificar se uvicorn está instalado
    try:
        import uvicorn
    except ImportError:
        print("❌ Erro: uvicorn não está instalado!")
        print("💡 Execute: pip install uvicorn")
        return
    
    # Iniciar servidores
    django_process = start_django()
    time.sleep(2)  # Aguardar Django inicializar
    fastapi_process = start_fastapi()
    
    print("\n✅ Servidores iniciados!")
    print("🌐 Django: http://localhost:8000")
    print("🔌 FastAPI: http://localhost:8001")
    print("📡 WebSocket: ws://localhost:8001/ws/updates")
    print("\n💡 Agora as atualizações em tempo real devem funcionar!")
    print("⏹️  Pressione Ctrl+C para parar os servidores")
    
    try:
        # Manter os processos rodando
        django_process.wait()
        fastapi_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Parando servidores...")
        django_process.terminate()
        fastapi_process.terminate()
        print("✅ Servidores parados!")

if __name__ == "__main__":
    main() 