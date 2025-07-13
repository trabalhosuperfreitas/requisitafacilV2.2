#!/usr/bin/env python3
"""
Script para testar a comunicação em tempo real entre Django e FastAPI
"""
import requests
import json
import time

def test_fastapi_connection():
    """Testa se o FastAPI está respondendo"""
    try:
        response = requests.get('http://localhost:8001/docs')
        if response.status_code == 200:
            print("✅ FastAPI está rodando na porta 8001")
            return True
        else:
            print(f"❌ FastAPI retornou status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar ao FastAPI na porta 8001")
        print("💡 Certifique-se de que o servidor FastAPI está rodando:")
        print("   python -m uvicorn realtime_server:app --host 0.0.0.0 --port 8001")
        return False

def test_django_connection():
    """Testa se o Django está respondendo"""
    try:
        response = requests.get('http://localhost:8000/')
        if response.status_code in [200, 302]:  # 302 é redirect para login
            print("✅ Django está rodando na porta 8000")
            return True
        else:
            print(f"❌ Django retornou status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar ao Django na porta 8000")
        print("💡 Certifique-se de que o servidor Django está rodando:")
        print("   python manage.py runserver 8000")
        return False

def test_notification():
    """Testa se a notificação está funcionando"""
    try:
        # Simula uma notificação do Django para o FastAPI
        response = requests.post('http://localhost:8001/notify', 
                               json={"action": "test", "message": "Teste de notificação"})
        if response.status_code == 200:
            print("✅ Notificação enviada com sucesso para o FastAPI")
            return True
        else:
            print(f"❌ Erro ao enviar notificação: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível enviar notificação para o FastAPI")
        return False

def main():
    print("🧪 Testando comunicação em tempo real...")
    print("=" * 50)
    
    # Testar conexões
    fastapi_ok = test_fastapi_connection()
    django_ok = test_django_connection()
    
    if fastapi_ok and django_ok:
        print("\n✅ Ambos os servidores estão rodando!")
        
        # Testar notificação
        if test_notification():
            print("\n🎉 Sistema de tempo real funcionando corretamente!")
            print("\n💡 Agora quando você criar ou atualizar requisições,")
            print("   o painel deve atualizar automaticamente!")
        else:
            print("\n⚠️  Sistema de notificação não está funcionando")
    else:
        print("\n❌ Um ou ambos os servidores não estão rodando")
        print("\n🔧 Para iniciar ambos os servidores, execute:")
        print("   python start_servers.py")

if __name__ == "__main__":
    main() 