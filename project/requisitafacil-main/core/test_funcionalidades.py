from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import uuid
import random
from django.db.models import Avg, ExpressionWrapper, F, Count, DurationField

from .models import (
    User, Sector, Request, RequestItem, Role, 
    RequestStatus, Urgency, ItemCategory
)

class TesteFuncionalidadesIsoladas(TestCase):
    """
    Testes isolados para cada funcionalidade do sistema.
    Cada teste foca em uma funcionalidade específica e é independente dos outros.
    """
    
    def setUp(self):
        """Configuração básica para todos os testes"""
        self.client = Client()
        
        # Criar setores básicos
        self.setores = {}
        setores_nomes = ["FLV", "Frios", "Padaria", "Açougue", "ADM"]
        for nome in setores_nomes:
            setor = Sector.objects.create(name=nome)
            self.setores[nome] = setor
        
        # Criar usuários básicos
        self.users = {}
        
        # Gestor
        self.users['gestor'] = User.objects.create_user(
            username='gestor',
            email='gestor@test.com',
            password='testpass123',
            role=Role.Gestor,
            first_name='João',
            last_name='Gestor'
        )
        
        # Almoxarife
        self.users['almoxarife'] = User.objects.create_user(
            username='almoxarife',
            email='almoxarife@test.com',
            password='testpass123',
            role=Role.Almoxarife,
            first_name='Maria',
            last_name='Almoxarife'
        )
        
        # Encarregado para FLV
        self.users['encarregado_flv'] = User.objects.create_user(
            username='encarregado_flv',
            email='encarregado_flv@test.com',
            password='testpass123',
            role=Role.Encarregado,
            first_name='Encarregado',
            last_name='FLV',
            sector=self.setores['FLV']
        )

    def login_user(self, user_key):
        """Helper para fazer login com um usuário específico"""
        user = self.users[user_key]
        success = self.client.login(email=user.email, password='testpass123')
        print(f"🔍 Tentativa de login para {user.email}: {'Sucesso' if success else 'Falha'}")
        if not success:
            print(f"🔍 Verificando se usuário existe: {User.objects.filter(email=user.email).exists()}")
            print(f"🔍 Verificando se senha está correta...")
        return user

    def criar_requisicao_simples(self, requester_key, setor_nome, status=RequestStatus.PENDING):
        """Cria uma requisição simples para testes"""
        requester = self.users[requester_key]
        setor = self.setores[setor_nome]
        
        requisicao = Request.objects.create(
            requester=requester,
            sector=setor,
            urgency=Urgency.NORMAL,
            observations="Teste de funcionalidade",
            status=status
        )
        
        # Criar um item simples
        RequestItem.objects.create(
            request=requisicao,
            item_requested="Papel A4",
            quantify=5,
            category=ItemCategory.ADMINISTRATIVO
        )
        
        return requisicao

    def test_01_criacao_requisicao_basica(self):
        """Testa se uma requisição pode ser criada corretamente"""
        print("\n=== Teste 1: Criação de Requisição Básica ===")
        
        # Limpar dados existentes
        Request.objects.all().delete()
        
        # Criar requisição
        requisicao = self.criar_requisicao_simples('encarregado_flv', 'FLV')
        
        # Verificações básicas
        self.assertIsNotNone(requisicao.id)
        self.assertIsNotNone(requisicao.request_code)
        self.assertEqual(requisicao.status, RequestStatus.PENDING)
        self.assertEqual(requisicao.urgency, Urgency.NORMAL)
        self.assertEqual(requisicao.sector.name, 'FLV')
        
        # Verificar se o item foi criado
        self.assertEqual(requisicao.items.count(), 1)
        item = requisicao.items.first()
        self.assertEqual(item.item_requested, "Papel A4")
        self.assertEqual(item.quantify, 5)
        
        print(f"✓ Requisição criada: {requisicao.request_code}")
        print(f"✓ Item criado: {item.item_requested}")

    def test_02_geracao_codigo_requisicao(self):
        """Testa se os códigos de requisição são gerados corretamente"""
        print("\n=== Teste 2: Geração de Código de Requisição ===")
        
        # Limpar dados existentes
        Request.objects.all().delete()
        
        # Criar requisições para diferentes setores
        setores_codigos = {
            'FLV': 'F',
            'Frios': 'FR', 
            'Padaria': 'PD',
            'Açougue': 'AC',
            'ADM': 'ADM'
        }
        
        for setor_nome, codigo_esperado in setores_codigos.items():
            req = self.criar_requisicao_simples('encarregado_flv', setor_nome)
            
            # Verificar se o código foi gerado corretamente
            self.assertIsNotNone(req.request_code)
            self.assertTrue(req.request_code.startswith(codigo_esperado))
            print(f"✓ Código gerado para {setor_nome}: {req.request_code}")

    def test_03_permissoes_usuarios(self):
        """Testa se as permissões de usuários estão funcionando corretamente"""
        print("\n=== Teste 3: Permissões de Usuários ===")
        
        # Testar acesso do gestor ao dashboard do gestor
        gestor = self.login_user('gestor')
        response = self.client.get(reverse('core:gestor_dashboard'))
        self.assertEqual(response.status_code, 200)
        print("✓ Gestor pode acessar dashboard do gestor")
        
        # Testar acesso do almoxarife ao dashboard do almoxarife
        almoxarife = self.login_user('almoxarife')
        response = self.client.get(reverse('core:almoxarife_dashboard'))
        self.assertEqual(response.status_code, 200)
        print("✓ Almoxarife pode acessar dashboard do almoxarife")
        
        # Testar que encarregado NÃO pode acessar dashboard do gestor
        encarregado = self.login_user('encarregado_flv')
        response = self.client.get(reverse('core:gestor_dashboard'))
        self.assertEqual(response.status_code, 403)  # Forbidden
        print("✓ Encarregado NÃO pode acessar dashboard do gestor")
        
        # Testar que encarregado NÃO pode acessar dashboard do almoxarife
        response = self.client.get(reverse('core:almoxarife_dashboard'))
        self.assertEqual(response.status_code, 403)  # Forbidden
        print("✓ Encarregado NÃO pode acessar dashboard do almoxarife")

    def test_04_kpis_gestor(self):
        """Testa se os KPIs do gestor são calculados corretamente"""
        print("\n=== Teste 4: KPIs do Gestor ===")
        
        # Limpar dados existentes
        Request.objects.all().delete()
        
        gestor = self.login_user('gestor')
        hoje = timezone.now().date()
        
        # Criar requisições com diferentes status
        # 3 pendentes
        for i in range(3):
            self.criar_requisicao_simples('encarregado_flv', 'FLV', RequestStatus.PENDING)
        
        # 2 aprovadas hoje
        for i in range(2):
            req = self.criar_requisicao_simples('encarregado_flv', 'FLV', RequestStatus.APPROVED)
            req.updated_at = timezone.now()
            req.save()
        
        # Verificar KPIs diretamente no banco
        pendentes = Request.objects.filter(status=RequestStatus.PENDING).count()
        aprovadas_hoje = Request.objects.filter(status=RequestStatus.APPROVED, updated_at__date=hoje).count()
        total_mes = Request.objects.filter(created_at__month=hoje.month, created_at__year=hoje.year).count()
        
        self.assertEqual(pendentes, 3)
        self.assertEqual(aprovadas_hoje, 2)
        self.assertEqual(total_mes, 5)
        
        print(f"✓ KPIs calculados corretamente:")
        print(f"  - Pendentes: {pendentes}")
        print(f"  - Aprovadas hoje: {aprovadas_hoje}")
        print(f"  - Total do mês: {total_mes}")

    def test_05_requisicoes_urgentes(self):
        """Testa o tratamento de requisições urgentes"""
        print("\n=== Teste 5: Requisições Urgentes ===")
        
        # Limpar dados existentes
        Request.objects.all().delete()
        
        # Criar requisições urgentes
        for i in range(3):
            req = self.criar_requisicao_simples('encarregado_flv', 'FLV', RequestStatus.PENDING)
            req.urgency = Urgency.URGENTE
            req.save()
        
        # Verificar contagem de urgentes
        urgentes_pendentes = Request.objects.filter(status=RequestStatus.PENDING, urgency=Urgency.URGENTE).count()
        self.assertEqual(urgentes_pendentes, 3)
        
        print(f"✓ Requisições urgentes pendentes: {urgentes_pendentes}")

    def test_06_fluxo_atendimento_almoxarife(self):
        """Testa o fluxo de atendimento do almoxarife"""
        print("\n=== Teste 6: Fluxo de Atendimento do Almoxarife ===")
        
        # Limpar dados existentes
        Request.objects.all().delete()
        
        # 1. Criar requisição
        requisicao = self.criar_requisicao_simples('encarregado_flv', 'FLV', RequestStatus.PENDING)
        print(f"✓ Requisição criada: {requisicao.request_code}")
        
        # 2. Almoxarife inicia atendimento
        almoxarife = self.login_user('almoxarife')
        print(f"🔍 Usuário logado: {almoxarife.username} - Role: {almoxarife.role}")
        
        # Verificar se o login funcionou
        response = self.client.get(reverse('core:dashboard'))
        print(f"🔍 Teste de login - Status: {response.status_code}")
        
        # Verificar se o usuário está autenticado
        from django.contrib.auth import get_user
        user = get_user(self.client)
        print(f"🔍 Usuário autenticado: {user.username if user.is_authenticated else 'Não autenticado'}")
        
        response = self.client.get(reverse('core:almoxarife_atender_requisicao', args=[requisicao.pk]))
        
        print(f"🔍 Status da resposta: {response.status_code}")
        if response.status_code == 302:
            print(f"⚠️  View retornou redirect (302) - URL: {response.url}")
            # Se for redirect, seguir o redirect
            response = self.client.get(response.url, follow=True)
            print(f"🔍 Status após seguir redirect: {response.status_code}")
        
        self.assertEqual(response.status_code, 200)
        
        # Verificar se status mudou para EM_ATENDIMENTO
        requisicao.refresh_from_db()
        self.assertEqual(requisicao.status, RequestStatus.EM_ATENDIMENTO)
        self.assertEqual(requisicao.atendido_por, almoxarife)
        print(f"✓ Atendimento iniciado por {almoxarife.get_full_name()}")
        
        # 3. Almoxarife finaliza atendimento
        response = self.client.post(reverse('core:almoxarife_atender_requisicao', args=[requisicao.pk]), {
            'quantidade_atendida': ['5'],  # Lista para corresponder ao template
            'item_id': [str(requisicao.items.first().id)],  # ID do item
            'observacao_item': ['Atendido completamente'],  # Lista para corresponder ao template
            'observacoes_atendimento': 'Atendimento finalizado com sucesso'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect após sucesso
        
        # Verificar se foi finalizada
        requisicao.refresh_from_db()
        self.assertEqual(requisicao.status, RequestStatus.APPROVED)
        print(f"✓ Requisição finalizada com sucesso")

    def test_07_tempo_medio_atendimento(self):
        """Testa o cálculo do tempo médio de atendimento"""
        print("\n=== Teste 7: Tempo Médio de Atendimento ===")
        
        # Limpar dados existentes
        Request.objects.all().delete()
        
        hoje = timezone.now()
        
        # Criar requisições aprovadas com diferentes tempos
        # Requisição aprovada rapidamente (1 hora)
        req_rapida = self.criar_requisicao_simples('encarregado_flv', 'FLV', RequestStatus.APPROVED)
        req_rapida.created_at = hoje - timedelta(hours=2)
        req_rapida.updated_at = hoje - timedelta(hours=1)
        req_rapida.save()
        
        # Requisição aprovada lentamente (24 horas)
        req_lenta = self.criar_requisicao_simples('encarregado_flv', 'FLV', RequestStatus.APPROVED)
        req_lenta.created_at = hoje - timedelta(hours=25)
        req_lenta.updated_at = hoje - timedelta(hours=1)
        req_lenta.save()
        
        # Calcular tempo médio manualmente
        tempo_medio = Request.objects.filter(status=RequestStatus.APPROVED).aggregate(
            media=Avg(ExpressionWrapper(F('updated_at') - F('created_at'), output_field=DurationField()))
        )['media']
        
        self.assertIsNotNone(tempo_medio)
        print(f"✓ Tempo médio calculado: {tempo_medio}")

    def test_08_percentual_atendidas_prazo(self):
        """Testa o cálculo do percentual de requisições atendidas no prazo"""
        print("\n=== Teste 8: Percentual Atendidas no Prazo ===")
        
        # Limpar dados existentes
        Request.objects.all().delete()
        
        hoje = timezone.now()
        
        # Criar requisições aprovadas no prazo (menos de 24h)
        for i in range(3):
            req = self.criar_requisicao_simples('encarregado_flv', 'FLV', RequestStatus.APPROVED)
            req.created_at = hoje - timedelta(hours=12)
            req.updated_at = hoje - timedelta(hours=1)
            req.save()
        
        # Criar requisições aprovadas fora do prazo (mais de 24h)
        for i in range(2):
            req = self.criar_requisicao_simples('encarregado_flv', 'FLV', RequestStatus.APPROVED)
            req.created_at = hoje - timedelta(hours=25)
            req.updated_at = hoje - timedelta(hours=1)
            req.save()
        
        # Calcular percentual manualmente
        total_aprovadas = Request.objects.filter(status=RequestStatus.APPROVED).count()
        atendidas_no_prazo = Request.objects.filter(
            status=RequestStatus.APPROVED,
            created_at__isnull=False,
            updated_at__isnull=False
        ).annotate(
            tempo_espera=ExpressionWrapper(F('updated_at') - F('created_at'), output_field=DurationField())
        ).filter(tempo_espera__lte=timedelta(hours=24)).count()
        
        pct_no_prazo = (atendidas_no_prazo / total_aprovadas * 100) if total_aprovadas else 0
        
        self.assertEqual(total_aprovadas, 5)
        self.assertEqual(atendidas_no_prazo, 3)
        self.assertEqual(pct_no_prazo, 60.0)
        
        print(f"✓ Percentual no prazo: {pct_no_prazo}%")

    def test_09_estatisticas_por_setor(self):
        """Testa as estatísticas por setor"""
        print("\n=== Teste 9: Estatísticas por Setor ===")
        
        # Limpar dados existentes
        Request.objects.all().delete()
        
        # Criar requisições para diferentes setores
        setores_test = ['FLV', 'Frios', 'Padaria']
        
        for setor in setores_test:
            # Criar 2 requisições para cada setor
            for i in range(2):
                self.criar_requisicao_simples('encarregado_flv', setor)
        
        # Verificar estatísticas por setor
        setores_stats = Request.objects.values('sector__name').annotate(total=Count('id')).order_by('-total')
        
        self.assertEqual(len(setores_stats), 3)
        
        for stat in setores_stats:
            print(f"✓ Setor {stat['sector__name']}: {stat['total']} requisições")

    def test_10_estatisticas_por_categoria(self):
        """Testa as estatísticas por categoria de item"""
        print("\n=== Teste 10: Estatísticas por Categoria ===")
        
        # Limpar dados existentes
        Request.objects.all().delete()
        
        # Criar requisições com diferentes categorias
        categorias = list(ItemCategory.choices)
        
        for categoria in categorias:
            req = self.criar_requisicao_simples('encarregado_flv', 'FLV')
            # Atualizar categoria do item
            if req.items.exists():
                item = req.items.first()
                item.category = categoria[0]
                item.save()
        
        # Verificar estatísticas por categoria
        categorias_stats = RequestItem.objects.values('category').annotate(total=Count('id')).order_by('-total')
        
        self.assertEqual(len(categorias_stats), len(categorias))
        
        for stat in categorias_stats:
            categoria_nome = dict(ItemCategory.choices).get(stat['category'], stat['category'])
            print(f"✓ Categoria {categoria_nome}: {stat['total']} itens")

    def test_11_verificacao_codigos_unicos(self):
        """Testa se os códigos de requisição são únicos"""
        print("\n=== Teste 11: Verificação de Códigos Únicos ===")
        
        # Limpar dados existentes
        Request.objects.all().delete()
        
        # Criar várias requisições rapidamente
        codigos_criados = set()
        
        for i in range(10):
            req = self.criar_requisicao_simples('encarregado_flv', 'FLV')
            codigo = req.request_code
            
            # Verificar se o código é único
            self.assertNotIn(codigo, codigos_criados)
            codigos_criados.add(codigo)
            
            print(f"✓ Código único criado: {codigo}")
        
        print(f"✓ Total de códigos únicos: {len(codigos_criados)}")

    def test_12_acesso_nao_autenticado(self):
        """Testa se usuários não autenticados são redirecionados"""
        print("\n=== Teste 12: Acesso Não Autenticado ===")
        
        # Tentar acessar dashboard sem estar logado
        response = self.client.get(reverse('core:gestor_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect para login
        print("✓ Usuário não autenticado é redirecionado")

    def test_13_requisicao_inexistente(self):
        """Testa o comportamento quando uma requisição não existe"""
        print("\n=== Teste 13: Requisição Inexistente ===")
        
        # Tentar acessar uma requisição que não existe
        fake_uuid = uuid.uuid4()
        response = self.client.get(reverse('core:detalhe_requisicao', args=[fake_uuid]))
        self.assertEqual(response.status_code, 404)  # Not Found
        print("✓ Requisição inexistente retorna 404")

    def test_14_permissoes_requisicao(self):
        """Testa as permissões de acesso a requisições"""
        print("\n=== Teste 14: Permissões de Requisição ===")
        
        # Criar uma requisição
        requisicao = self.criar_requisicao_simples('encarregado_flv', 'FLV')
        
        # 1. Encarregado deve poder ver sua própria requisição
        self.login_user('encarregado_flv')
        response = self.client.get(reverse('core:detalhe_requisicao', args=[requisicao.pk]))
        self.assertEqual(response.status_code, 200)
        print("✓ Encarregado pode ver sua própria requisição")
        
        # 2. Gestor deve poder ver qualquer requisição
        self.login_user('gestor')
        response = self.client.get(reverse('core:detalhe_requisicao', args=[requisicao.pk]))
        self.assertEqual(response.status_code, 200)
        print("✓ Gestor pode ver qualquer requisição")
        
        # 3. Almoxarife deve poder ver qualquer requisição
        self.login_user('almoxarife')
        response = self.client.get(reverse('core:detalhe_requisicao', args=[requisicao.pk]))
        self.assertEqual(response.status_code, 200)
        print("✓ Almoxarife pode ver qualquer requisição")

    def test_15_estatisticas_vazias(self):
        """Testa o comportamento quando não há requisições"""
        print("\n=== Teste 15: Estatísticas Vazias ===")
        
        # Limpar dados existentes
        Request.objects.all().delete()
        
        gestor = self.login_user('gestor')
        
        # Verificar KPIs quando não há requisições
        pendentes = Request.objects.filter(status=RequestStatus.PENDING).count()
        aprovadas_hoje = Request.objects.filter(status=RequestStatus.APPROVED).count()
        total_mes = Request.objects.filter(created_at__month=timezone.now().month).count()
        
        self.assertEqual(pendentes, 0)
        self.assertEqual(aprovadas_hoje, 0)
        self.assertEqual(total_mes, 0)
        
        print("✓ KPIs zerados quando não há requisições")

    def run_todos_testes(self):
        """Executa todos os testes em sequência"""
        print("🚀 Iniciando testes de funcionalidades isoladas")
        print("=" * 60)
        
        # Lista de todos os testes
        test_methods = [
            'test_01_criacao_requisicao_basica',
            'test_02_geracao_codigo_requisicao',
            'test_03_permissoes_usuarios',
            'test_04_kpis_gestor',
            'test_05_requisicoes_urgentes',
            'test_06_fluxo_atendimento_almoxarife',
            'test_07_tempo_medio_atendimento',
            'test_08_percentual_atendidas_prazo',
            'test_09_estatisticas_por_setor',
            'test_10_estatisticas_por_categoria',
            'test_11_verificacao_codigos_unicos',
            'test_12_acesso_nao_autenticado',
            'test_13_requisicao_inexistente',
            'test_14_permissoes_requisicao',
            'test_15_estatisticas_vazias'
        ]
        
        resultados = []
        
        for test_method in test_methods:
            try:
                print(f"\n🧪 Executando: {test_method}")
                getattr(self, test_method)()
                print(f"✅ {test_method} - PASSOU")
                resultados.append((test_method, True, None))
            except Exception as e:
                print(f"❌ {test_method} - FALHOU: {str(e)}")
                resultados.append((test_method, False, str(e)))
        
        # Resumo final
        print("\n" + "=" * 60)
        print("📊 RESUMO DOS TESTES")
        print("=" * 60)
        
        passaram = sum(1 for _, success, _ in resultados if success)
        total = len(resultados)
        
        for test_name, success, error in resultados:
            status = "✅ PASSOU" if success else "❌ FALHOU"
            print(f"{status}: {test_name}")
            if not success and error:
                print(f"    Erro: {error}")
        
        print(f"\n🎯 Resultado Final: {passaram}/{total} testes passaram")
        
        if passaram == total:
            print("🎉 Todos os testes passaram!")
        else:
            print(f"⚠️ {total - passaram} teste(s) falharam")
        
        print("=" * 60) 