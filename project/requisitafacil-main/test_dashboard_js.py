#!/usr/bin/env python3
"""
Script para testar se o JavaScript do dashboard está sendo carregado
"""
import requests
from bs4 import BeautifulSoup

def test_dashboard_js():
    """Testa se o JavaScript do dashboard está sendo carregado"""
    try:
        # Faz login primeiro (simula um usuário logado)
        session = requests.Session()
        
        # Tenta acessar o dashboard
        response = session.get('http://localhost:8000/dashboard/')
        
        if response.status_code == 200:
            print("✅ Dashboard acessível")
            
            # Verifica se o JavaScript está sendo carregado
            soup = BeautifulSoup(response.text, 'html.parser')
            js_scripts = soup.find_all('script', src=True)
            
            dashboard_js_found = False
            for script in js_scripts:
                if 'dashboard-realtime.js' in script.get('src', ''):
                    dashboard_js_found = True
                    print(f"✅ JavaScript do dashboard encontrado: {script.get('src')}")
                    break
            
            if not dashboard_js_found:
                print("❌ JavaScript do dashboard não encontrado")
                print("Scripts encontrados:")
                for script in js_scripts:
                    print(f"  - {script.get('src')}")
            
            return dashboard_js_found
        else:
            print(f"❌ Erro ao acessar dashboard: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar ao Django")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("🧪 Testando carregamento do JavaScript do dashboard...")
    print("=" * 50)
    
    js_ok = test_dashboard_js()
    
    if js_ok:
        print("\n✅ JavaScript do dashboard está sendo carregado!")
        print("\n💡 Para testar a atualização automática:")
        print("   1. Abra o dashboard no navegador")
        print("   2. Abra o console do navegador (F12)")
        print("   3. Crie uma nova requisição")
        print("   4. Verifique se aparecem as mensagens de log")
    else:
        print("\n❌ JavaScript do dashboard não está sendo carregado")
        print("\n🔧 Verificações:")
        print("   - Certifique-se de que o servidor Django está rodando")
        print("   - Verifique se o arquivo dashboard-realtime.js existe")
        print("   - Execute: python manage.py collectstatic")

if __name__ == "__main__":
    main() 