#!/usr/bin/env python3
"""
Script para configurar o ambiente de desenvolvimento local
"""
import os
import subprocess
import sys
from pathlib import Path

def create_env_file():
    """Cria arquivo .env se não existir"""
    env_file = Path('.env')
    if not env_file.exists():
        print("📝 Criando arquivo .env...")
        env_content = """# Configurações de Desenvolvimento Local
DEBUG=True
SECRET_KEY=chave_insegura_para_desenvolvimento_local
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Arquivo .env criado!")
    else:
        print("✅ Arquivo .env já existe!")

def install_dependencies():
    """Instala dependências do projeto"""
    print("📦 Instalando dependências...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ Dependências instaladas!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False
    return True

def run_migrations():
    """Executa migrações do banco de dados"""
    print("🗄️ Executando migrações...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=True)
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("✅ Migrações executadas!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar migrações: {e}")
        return False
    return True

def create_superuser():
    """Cria superusuário se solicitado"""
    print("\n👤 Deseja criar um superusuário? (s/n): ", end="")
    response = input().lower()
    if response in ['s', 'sim', 'y', 'yes']:
        try:
            subprocess.run([sys.executable, 'manage.py', 'createsuperuser'], check=True)
            print("✅ Superusuário criado!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao criar superusuário: {e}")

def main():
    print("🚀 Configurando ambiente de desenvolvimento...")
    print("=" * 50)
    
    # 1. Criar arquivo .env
    create_env_file()
    
    # 2. Instalar dependências
    if not install_dependencies():
        return
    
    # 3. Executar migrações
    if not run_migrations():
        return
    
    # 4. Criar superusuário
    create_superuser()
    
    print("\n🎉 Configuração concluída!")
    print("\n📋 Para iniciar o projeto:")
    print("   python start_servers.py")
    print("\n📋 Ou inicie separadamente:")
    print("   Terminal 1: python manage.py runserver")
    print("   Terminal 2: python -m uvicorn realtime_server:app --reload --port 8001")

if __name__ == "__main__":
    main() 