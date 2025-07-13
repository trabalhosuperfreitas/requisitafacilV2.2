#!/usr/bin/env python3
"""
Script para testar o cenário real: dashboard aberto + criação de requisição
"""
import requests
import time
import json

def test_real_scenario():
    """Testa o cenário real de uso"""
    print("🧪 Testando cenário real: Dashboard + Criação de Requisição")
    print("=" * 60)
    
    # 1. Simula um dashboard aberto (conecta ao WebSocket)
    print("1️⃣  Simulando dashboard aberto...")
    try:
        # Conecta ao WebSocket (simula dashboard aberto)
        import websocket
        
        ws = websocket.create_connection("ws://localhost:8001/ws/updates")
        print("✅ WebSocket conectado (dashboard simulado)")
        
        # Envia ping para manter conexão ativa
        ws.send('ping')
        time.sleep(1)
        
        # Recebe o pong
        pong = ws.recv()
        print(f"✅ Ping/Pong funcionando: {pong}")
        
        # 2. Cria uma requisição
        print("\n2️⃣  Criando uma requisição...")
        
        # Simula criação de requisição
        response = requests.post('http://localhost:8001/notify', 
                               json={"action": "created", "message": "Teste de requisição criada"})
        
        if response.status_code == 200:
            print("✅ Notificação de requisição criada enviada")
            print(f"📤 Resposta do servidor: {response.json()}")
            
            # 3. Verifica se o WebSocket recebeu a mensagem
            print("\n3️⃣  Verificando se o dashboard recebeu a atualização...")
            
            # Aguarda um pouco para receber a mensagem
            time.sleep(2)
            
            # Tenta receber mensagem do WebSocket
            try:
                ws.settimeout(5)
                message = ws.recv()
                print(f"📨 Mensagem recebida no dashboard: {message}")
                
                if message == 'created':
                    print("🎉 SUCESSO! Dashboard recebeu a atualização automaticamente!")
                    return True
                else:
                    print(f"⚠️  Mensagem inesperada recebida: {message}")
                    print("💡 Isso pode indicar que a notificação não está sendo enviada corretamente")
                    return False
                    
            except websocket.WebSocketTimeoutException:
                print("❌ Timeout: Dashboard não recebeu a atualização")
                print("💡 Verifique se o servidor FastAPI está enviando as notificações")
                return False
            except Exception as e:
                print(f"❌ Erro ao receber mensagem: {e}")
                return False
        else:
            print(f"❌ Erro ao enviar notificação: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False
    finally:
        try:
            ws.close()
        except:
            pass

def test_notification_directly():
    """Testa se a notificação está sendo enviada diretamente"""
    print("\n🔍 Testando notificação diretamente...")
    
    try:
        response = requests.post('http://localhost:8001/notify', 
                               json={"action": "test_direct", "message": "Teste direto"})
        
        if response.status_code == 200:
            print("✅ Notificação enviada com sucesso")
            print(f"📤 Resposta: {response.json()}")
            return True
        else:
            print(f"❌ Erro ao enviar notificação: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("🔄 Iniciando teste do cenário real...")
    
    # Testa notificação diretamente primeiro
    test_notification_directly()
    
    # Testa o cenário completo
    success = test_real_scenario()
    
    if success:
        print("\n🎉 Teste passou! O sistema está funcionando corretamente.")
        print("\n💡 Agora teste manualmente:")
        print("   1. Abra o dashboard em um navegador")
        print("   2. Abra o console (F12) para ver os logs")
        print("   3. Em outro navegador, crie uma requisição")
        print("   4. Veja se o primeiro navegador atualiza automaticamente")
    else:
        print("\n❌ Teste falhou. Verificando possíveis problemas...")
        print("\n🔧 Verificações:")
        print("   - Servidores estão rodando?")
        print("   - WebSocket está conectando?")
        print("   - Notificações estão sendo enviadas?")
        print("\n💡 Verifique o log do servidor FastAPI para mais detalhes")

if __name__ == "__main__":
    main() 