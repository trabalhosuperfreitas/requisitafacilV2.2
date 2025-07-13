#!/usr/bin/env python3
"""
Script completo para testar o sistema de tempo real
"""
import requests
import json
import time
import websocket
import threading

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

def test_websocket_connection():
    """Testa se o WebSocket está funcionando"""
    try:
        ws = websocket.create_connection("ws://localhost:8001/ws/updates")
        print("✅ WebSocket conectado com sucesso")
        ws.close()
        return True
    except Exception as e:
        print(f"❌ Erro ao conectar WebSocket: {e}")
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

def test_websocket_receive():
    """Testa se o WebSocket recebe mensagens"""
    received_messages = []
    
    def on_message(ws, message):
        received_messages.append(message)
        print(f"📨 Mensagem recebida via WebSocket: {message}")
        ws.close()
    
    def on_error(ws, error):
        print(f"❌ Erro no WebSocket: {error}")
    
    def on_close(ws, close_status_code, close_msg):
        print("🔌 WebSocket fechado")
    
    def on_open(ws):
        print("🔌 WebSocket aberto, enviando notificação de teste...")
        # Envia uma notificação de teste
        try:
            requests.post('http://localhost:8001/notify', 
                        json={"action": "websocket_test", "message": "Teste WebSocket"})
        except Exception as e:
            print(f"❌ Erro ao enviar notificação de teste: {e}")
    
    try:
        ws = websocket.WebSocketApp("ws://localhost:8001/ws/updates",
                                  on_open=on_open,
                                  on_message=on_message,
                                  on_error=on_error,
                                  on_close=on_close)
        
        # Executa o WebSocket em uma thread separada
        wst = threading.Thread(target=ws.run_forever)
        wst.daemon = True
        wst.start()
        
        # Aguarda por 5 segundos para receber mensagens
        time.sleep(5)
        
        if received_messages:
            print("✅ WebSocket recebeu mensagens corretamente")
            return True
        else:
            print("❌ WebSocket não recebeu mensagens")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar WebSocket: {e}")
        return False

def main():
    print("🧪 Testando sistema de tempo real completo...")
    print("=" * 60)
    
    # Testar conexões básicas
    fastapi_ok = test_fastapi_connection()
    django_ok = test_django_connection()
    
    if not fastapi_ok or not django_ok:
        print("\n❌ Servidores não estão rodando corretamente")
        print("\n🔧 Para iniciar ambos os servidores, execute:")
        print("   python start_servers.py")
        return
    
    print("\n✅ Ambos os servidores estão rodando!")
    
    # Testar WebSocket
    websocket_ok = test_websocket_connection()
    if not websocket_ok:
        print("\n❌ WebSocket não está funcionando")
        return
    
    # Testar notificação
    notification_ok = test_notification()
    if not notification_ok:
        print("\n❌ Sistema de notificação não está funcionando")
        return
    
    # Testar recebimento de mensagens via WebSocket
    print("\n🔄 Testando recebimento de mensagens via WebSocket...")
    websocket_receive_ok = test_websocket_receive()
    
    if websocket_receive_ok:
        print("\n🎉 Sistema de tempo real funcionando corretamente!")
        print("\n💡 Agora quando você criar ou atualizar requisições,")
        print("   o painel deve atualizar automaticamente!")
        print("\n📋 Checklist:")
        print("   ✅ FastAPI rodando")
        print("   ✅ Django rodando")
        print("   ✅ WebSocket conectando")
        print("   ✅ Notificações sendo enviadas")
        print("   ✅ WebSocket recebendo mensagens")
    else:
        print("\n⚠️  Sistema parcialmente funcionando")
        print("   - Servidores OK")
        print("   - WebSocket conecta")
        print("   - Notificações são enviadas")
        print("   - ❌ WebSocket não recebe mensagens")

if __name__ == "__main__":
    main() 