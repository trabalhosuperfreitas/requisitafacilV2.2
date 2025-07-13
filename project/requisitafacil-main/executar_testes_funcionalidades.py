#!/usr/bin/env python
"""
Script para executar testes de funcionalidades isoladas
Cada teste foca em uma funcionalidade específica do sistema
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'requisita_facil.settings')
django.setup()

from django.core.management import execute_from_command_line

def executar_teste_especifico(nome_teste):
    """Executa um teste específico"""
    print(f"🧪 Executando teste: {nome_teste}")
    sys.argv = ['manage.py', 'test', f'core.test_funcionalidades.TesteFuncionalidadesIsoladas.{nome_teste}', '--verbosity=2']
    execute_from_command_line(sys.argv)

def executar_todos_testes():
    """Executa todos os testes de funcionalidades"""
    print("🚀 Executando todos os testes de funcionalidades")
    sys.argv = ['manage.py', 'test', 'core.test_funcionalidades.TesteFuncionalidadesIsoladas', '--verbosity=2']
    execute_from_command_line(sys.argv)

def limpar_dados_teste():
    """Remove todas as requisições, itens e usuários de teste do banco de dados."""
    print("🧹 Limpando dados de teste...")
    from core.models import Request, RequestItem, User
    # Apagar itens e requisições
    total_itens = RequestItem.objects.count()
    total_requisicoes = Request.objects.count()
    RequestItem.objects.all().delete()
    Request.objects.all().delete()
    # Apagar usuários de teste (username ou email contendo 'test')
    usuarios_teste = User.objects.filter(username__icontains='test') | User.objects.filter(email__icontains='test')
    total_usuarios = usuarios_teste.count()
    usuarios_teste.delete()
    print(f"✓ Removidas {total_requisicoes} requisições e {total_itens} itens.")
    print(f"✓ Removidos {total_usuarios} usuários de teste.")
    print("✓ Banco de dados limpo!")

def mostrar_menu():
    """Mostra menu de opções"""
    print("\n" + "="*60)
    print("🧪 TESTES DE FUNCIONALIDADES ISOLADAS")
    print("="*60)
    print("1. Teste 1: Criação de Requisição Básica")
    print("2. Teste 2: Geração de Código de Requisição")
    print("3. Teste 3: Permissões de Usuários")
    print("4. Teste 4: KPIs do Gestor")
    print("5. Teste 5: Requisições Urgentes")
    print("6. Teste 6: Fluxo de Atendimento do Almoxarife")
    print("7. Teste 7: Tempo Médio de Atendimento")
    print("8. Teste 8: Percentual Atendidas no Prazo")
    print("9. Teste 9: Estatísticas por Setor")
    print("10. Teste 10: Estatísticas por Categoria")
    print("11. Teste 11: Verificação de Códigos Únicos")
    print("12. Teste 12: Acesso Não Autenticado")
    print("13. Teste 13: Requisição Inexistente")
    print("14. Teste 14: Permissões de Requisição")
    print("15. Teste 15: Estatísticas Vazias")
    print("16. Executar TODOS os testes")
    print("17. Limpar dados de teste do banco de dados")
    print("0. Sair")
    print("="*60)

def main():
    """Função principal"""
    while True:
        mostrar_menu()
        
        try:
            opcao = input("\nEscolha uma opção (0-17): ").strip()
            
            if opcao == '0':
                print("👋 Saindo...")
                break
            elif opcao == '1':
                executar_teste_especifico('test_01_criacao_requisicao_basica')
            elif opcao == '2':
                executar_teste_especifico('test_02_geracao_codigo_requisicao')
            elif opcao == '3':
                executar_teste_especifico('test_03_permissoes_usuarios')
            elif opcao == '4':
                executar_teste_especifico('test_04_kpis_gestor')
            elif opcao == '5':
                executar_teste_especifico('test_05_requisicoes_urgentes')
            elif opcao == '6':
                executar_teste_especifico('test_06_fluxo_atendimento_almoxarife')
            elif opcao == '7':
                executar_teste_especifico('test_07_tempo_medio_atendimento')
            elif opcao == '8':
                executar_teste_especifico('test_08_percentual_atendidas_prazo')
            elif opcao == '9':
                executar_teste_especifico('test_09_estatisticas_por_setor')
            elif opcao == '10':
                executar_teste_especifico('test_10_estatisticas_por_categoria')
            elif opcao == '11':
                executar_teste_especifico('test_11_verificacao_codigos_unicos')
            elif opcao == '12':
                executar_teste_especifico('test_12_acesso_nao_autenticado')
            elif opcao == '13':
                executar_teste_especifico('test_13_requisicao_inexistente')
            elif opcao == '14':
                executar_teste_especifico('test_14_permissoes_requisicao')
            elif opcao == '15':
                executar_teste_especifico('test_15_estatisticas_vazias')
            elif opcao == '16':
                executar_todos_testes()
            elif opcao == '17':
                limpar_dados_teste()
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