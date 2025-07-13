#!/usr/bin/env python
"""
Script para testar o sistema Requisição Fácil
Gera dados de teste e executa testes automatizados
"""

import os
import sys
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'requisita_facil.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.test.utils import get_runner
from django.conf import settings

def executar_comando_django(comando, args=None):
    """Executa um comando Django"""
    if args is None:
        args = []
    
    sys.argv = ['manage.py'] + comando.split() + args
    execute_from_command_line(sys.argv)

def gerar_dados_teste(num_requisicoes=50):
    """Gera dados de teste para o sistema"""
    print("🚀 Gerando dados de teste...")
    print(f"📝 Criando {num_requisicoes} requisições...")
    
    executar_comando_django('gerar_dados_teste', [
        '--num-requisicoes', str(num_requisicoes),
        '--dias-atras', '30'
    ])

def executar_testes():
    """Executa os testes automatizados"""
    print("🧪 Executando testes automatizados...")
    
    # Executar testes específicos
    executar_comando_django('test', [
        'core.tests.RequisicaoFacilTestCase',
        '--verbosity=2'
    ])

def executar_testes_rapidos():
    """Executa testes rápidos para verificar funcionalidades básicas"""
    print("⚡ Executando testes rápidos...")
    
    # Testes básicos
    executar_comando_django('test', [
        'core.tests.RequisicaoFacilTestCase.test_criar_requisicoes_fake_para_todos_setores',
        'core.tests.RequisicaoFacilTestCase.test_kpis_gestor_apos_criar_requisicoes',
        '--verbosity=2'
    ])

def mostrar_estatisticas():
    """Mostra estatísticas do sistema"""
    print("📊 Estatísticas do sistema:")
    
    from core.models import Request, User, Sector
    
    total_requisicoes = Request.objects.count()
    total_usuarios = User.objects.count()
    total_setores = Sector.objects.count()
    
    print(f"   - Total de requisições: {total_requisicoes}")
    print(f"   - Total de usuários: {total_usuarios}")
    print(f"   - Total de setores: {total_setores}")
    
    if total_requisicoes > 0:
        from core.models import RequestStatus, Urgency
        
        pendentes = Request.objects.filter(status=RequestStatus.PENDING).count()
        em_atendimento = Request.objects.filter(status=RequestStatus.EM_ATENDIMENTO).count()
        aprovadas = Request.objects.filter(status=RequestStatus.APPROVED).count()
        urgentes = Request.objects.filter(urgency=Urgency.URGENTE).count()
        
        print(f"   - Requisições pendentes: {pendentes}")
        print(f"   - Requisições em atendimento: {em_atendimento}")
        print(f"   - Requisições aprovadas: {aprovadas}")
        print(f"   - Requisições urgentes: {urgentes}")

def limpar_dados_teste():
    """Limpa dados de teste"""
    print("🧹 Limpando dados de teste...")
    
    from core.models import Request, RequestItem, User, Sector
    
    # Contar antes de limpar
    total_requisicoes = Request.objects.count()
    total_usuarios = User.objects.count()
    
    # Limpar requisições e itens
    RequestItem.objects.all().delete()
    Request.objects.all().delete()
    
    # Limpar usuários de teste (que contêm 'teste' no username)
    User.objects.filter(username__contains='teste').delete()
    
    print(f"✓ Removidas {total_requisicoes} requisições")
    print(f"✓ Removidos usuários de teste")

def mostrar_menu():
    """Mostra menu de opções"""
    print("\n" + "="*60)
    print("🧪 SISTEMA DE TESTES - REQUISIÇÃO FÁCIL")
    print("="*60)
    print("1. Gerar dados de teste (50 requisições)")
    print("2. Gerar dados de teste (100 requisições)")
    print("3. Gerar dados de teste (200 requisições)")
    print("4. Executar testes completos")
    print("5. Executar testes rápidos")
    print("6. Mostrar estatísticas")
    print("7. Limpar dados de teste")
    print("8. Executar tudo (gerar dados + testes)")
    print("0. Sair")
    print("="*60)

def main():
    """Função principal"""
    while True:
        mostrar_menu()
        
        try:
            opcao = input("\nEscolha uma opção (0-8): ").strip()
            
            if opcao == '0':
                print("👋 Saindo...")
                break
            elif opcao == '1':
                gerar_dados_teste(50)
            elif opcao == '2':
                gerar_dados_teste(100)
            elif opcao == '3':
                gerar_dados_teste(200)
            elif opcao == '4':
                executar_testes()
            elif opcao == '5':
                executar_testes_rapidos()
            elif opcao == '6':
                mostrar_estatisticas()
            elif opcao == '7':
                limpar_dados_teste()
            elif opcao == '8':
                print("🚀 Executando tudo...")
                gerar_dados_teste(100)
                print("\n" + "="*60)
                executar_testes()
            else:
                print("❌ Opção inválida!")
                
        except KeyboardInterrupt:
            print("\n👋 Saindo...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        input("\nPressione Enter para continuar...")

if __name__ == '__main__':
    main() 