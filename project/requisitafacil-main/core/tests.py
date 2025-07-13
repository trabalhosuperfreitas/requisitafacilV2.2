from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import uuid
import random
from decimal import Decimal

from .models import (
    User, Sector, Request, RequestItem, Role, 
    RequestStatus, Urgency, ItemCategory
)

class RequisicaoFacilTestCase(TestCase):
    def setUp(self):
        """Configuração inicial para todos os testes"""
        self.client = Client()
        
        # Criar setores
        self.setores = {}
        setores_nomes = ["FLV", "Frios", "Padaria", "Açougue", "ADM", "Deposito", "Limpeza", "Comercial", "Loja"]
        for nome in setores_nomes:
            setor = Sector.objects.create(name=nome)
            self.setores[nome] = setor
        
        # Criar usuários com diferentes roles
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
        
        # Encarregados para cada setor
        for i, (nome_setor, setor) in enumerate(self.setores.items()):
            encarregado = User.objects.create_user(
                username=f'encarregado_{nome_setor.lower()}',
                email=f'encarregado_{nome_setor.lower()}@test.com',
                password='testpass123',
                role=Role.Encarregado,
                first_name=f'Encarregado',
                last_name=nome_setor,
                sector=setor
            )
            self.users[f'encarregado_{nome_setor.lower()}'] = encarregado

    def login_user(self, user_key):
        """Helper para fazer login com um usuário específico"""
        user = self.users[user_key]
        self.client.login(username=user.username, password='testpass123')
        return user

    def criar_requisicao_fake(self, requester_key, setor_nome, status=RequestStatus.PENDING, 
                             urgency=Urgency.NORMAL, num_items=3, quantidade_atendida=0):
        """Cria uma requisição falsa para testes"""
        requester = self.users[requester_key]
        setor = self.setores[setor_nome]
        
        # Criar requisição
        requisicao = Request.objects.create(
            requester=requester,
            sector=setor,
            urgency=urgency,
            observations=f"Observação teste para {setor_nome}",
            status=status
        )
        
        # Criar itens da requisição
        categorias = list(ItemCategory.choices)
        itens_nomes = [
            "Papel A4", "Caneta", "Lápis", "Borracha", "Régua", "Tesoura",
            "Cola", "Fita adesiva", "Post-it", "Grampeador", "Clips",
            "Envelope", "Cartolina", "EVA", "Tinta", "Pincel", "Pano",
            "Detergente", "Desinfetante", "Papel higiênico"
        ]
        
        for i in range(num_items):
            categoria = random.choice(categorias)[0]
            item_nome = random.choice(itens_nomes)
            quantidade = random.randint(1, 10)
            
            RequestItem.objects.create(
                request=requisicao,
                item_requested=item_nome,
                quantify=quantidade,
                category=categoria,
                quantidade_atendida=quantidade_atendida,
                observacao_item=f"Observação do item {i+1}"
            )
        
        return requisicao

    def test_criar_requisicoes_fake_para_todos_setores(self):
        """Testa criação de requisições falsas para todos os setores"""
        print("\n=== Testando criação de requisições falsas ===")
        
        # Criar requisições para cada setor
        requisicoes_criadas = []
        
        for setor_nome in self.setores.keys():
            # Criar requisição normal
            req_normal = self.criar_requisicao_fake(
                f'encarregado_{setor_nome.lower()}', 
                setor_nome, 
                status=RequestStatus.PENDING,
                urgency=Urgency.NORMAL
            )
            requisicoes_criadas.append(req_normal)
            print(f"✓ Requisição normal criada para {setor_nome}: {req_normal.request_code}")
            
            # Criar requisição urgente
            req_urgente = self.criar_requisicao_fake(
                f'encarregado_{setor_nome.lower()}', 
                setor_nome, 
                status=RequestStatus.PENDING,
                urgency=Urgency.URGENTE
            )
            requisicoes_criadas.append(req_urgente)
            print(f"✓ Requisição urgente criada para {setor_nome}: {req_urgente.request_code}")
            
            # Criar requisição já aprovada
            req_aprovada = self.criar_requisicao_fake(
                f'encarregado_{setor_nome.lower()}', 
                setor_nome, 
                status=RequestStatus.APPROVED,
                urgency=Urgency.NORMAL,
                quantidade_atendida=5
            )
            requisicoes_criadas.append(req_aprovada)
            print(f"✓ Requisição aprovada criada para {setor_nome}: {req_aprovada.request_code}")
        
        # Verificar se todas foram criadas
        self.assertEqual(len(requisicoes_criadas), len(self.setores) * 3)
        print(f"✓ Total de {len(requisicoes_criadas)} requisições criadas com sucesso")

    def test_kpis_gestor_apos_criar_requisicoes(self):
        """Testa se os KPIs do gestor são atualizados corretamente após criar requisições"""
        print("\n=== Testando KPIs do gestor ===")
        
        # Fazer login como gestor
        gestor = self.login_user('gestor')
        
        # Criar várias requisições com diferentes status
        hoje = timezone.now().date()
        
        # Requisições pendentes
        for i in range(5):
            self.criar_requisicao_fake(
                'encarregado_flv', 'FLV', 
                status=RequestStatus.PENDING
            )
        
        # Requisições em atendimento
        for i in range(3):
            self.criar_requisicao_fake(
                'encarregado_frios', 'Frios', 
                status=RequestStatus.EM_ATENDIMENTO
            )
        
        # Requisições aprovadas hoje
        for i in range(4):
            req = self.criar_requisicao_fake(
                'encarregado_padaria', 'Padaria', 
                status=RequestStatus.APPROVED
            )
            # Forçar data de atualização para hoje
            req.updated_at = timezone.now()
            req.save()
        
        # Requisições aprovadas em dias anteriores
        for i in range(2):
            req = self.criar_requisicao_fake(
                'encarregado_acougue', 'Açougue', 
                status=RequestStatus.APPROVED
            )
            # Forçar data de atualização para ontem
            req.updated_at = timezone.now() - timedelta(days=1)
            req.save()
        
        # Acessar dashboard do gestor
        response = self.client.get(reverse('core:gestor_dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Verificar se os KPIs estão sendo calculados corretamente
        context = response.context
        
        # Verificar KPIs básicos
        self.assertEqual(context['pendentes'], 5)  # 5 pendentes
        self.assertEqual(context['aprovadas_hoje'], 4)  # 4 aprovadas hoje
        self.assertGreaterEqual(context['total_mes'], 14)  # Total do mês
        self.assertEqual(context['departamentos_ativos'], 4)  # 4 setores com requisições
        self.assertEqual(context['urgentes_pendentes'], 0)  # Nenhuma urgente pendente
        
        print(f"✓ KPIs calculados corretamente:")
        print(f"  - Pendentes: {context['pendentes']}")
        print(f"  - Aprovadas hoje: {context['aprovadas_hoje']}")
        print(f"  - Total do mês: {context['total_mes']}")
        print(f"  - Departamentos ativos: {context['departamentos_ativos']}")

    def test_fluxo_completo_requisicao(self):
        """Testa o fluxo completo de uma requisição: criar -> atender -> aprovar"""
        print("\n=== Testando fluxo completo de requisição ===")
        
        # 1. Encarregado cria requisição
        encarregado = self.login_user('encarregado_flv')
        
        # Simular criação de requisição via POST
        response = self.client.post(reverse('core:criar_requisicao'), {
            'urgency': 'NORMAL',
            'observations': 'Teste de fluxo completo',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '10',
            'form-0-item_requested': 'Papel A4',
            'form-0-quantify': '5',
            'form-0-category': 'ADIMINISTRATIVO',
            'form-1-item_requested': 'Caneta',
            'form-1-quantify': '10',
            'form-1-category': 'ADIMINISTRATIVO',
        })
        
        # Verificar se foi criada
        self.assertEqual(response.status_code, 302)  # Redirect após sucesso
        requisicao = Request.objects.filter(requester=encarregado).latest('created_at')
        print(f"✓ Requisição criada: {requisicao.request_code}")
        
        # 2. Almoxarife inicia atendimento
        almoxarife = self.login_user('almoxarife')
        response = self.client.get(reverse('core:almoxarife_atender_requisicao', args=[requisicao.pk]))
        self.assertEqual(response.status_code, 200)
        
        # Verificar se status mudou para EM_ATENDIMENTO
        requisicao.refresh_from_db()
        self.assertEqual(requisicao.status, RequestStatus.EM_ATENDIMENTO)
        self.assertEqual(requisicao.atendido_por, almoxarife)
        print(f"✓ Atendimento iniciado por {almoxarife.get_full_name()}")
        
        # 3. Almoxarife finaliza atendimento
        response = self.client.post(reverse('core:almoxarife_atender_requisicao', args=[requisicao.pk]), {
            'quantidade_atendida_0': '5',
            'observacao_item_0': 'Atendido completamente',
            'quantidade_atendida_1': '8',
            'observacao_item_1': 'Atendido parcialmente',
            'observacoes_atendimento': 'Atendimento finalizado com sucesso'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect após sucesso
        
        # Verificar se foi finalizada
        requisicao.refresh_from_db()
        self.assertEqual(requisicao.status, RequestStatus.APPROVED)
        print(f"✓ Requisição finalizada com sucesso")
        
        # Verificar itens atendidos
        for item in requisicao.items.all():
            self.assertGreater(item.quantidade_atendida, 0)
            print(f"  - Item: {item.item_requested} - Atendido: {item.quantidade_atendida}/{item.quantify}")

    def test_permissoes_usuarios(self):
        """Testa se as permissões estão funcionando corretamente"""
        print("\n=== Testando permissões de usuários ===")
        
        # Testar acesso do gestor
        gestor = self.login_user('gestor')
        response = self.client.get(reverse('core:gestor_dashboard'))
        self.assertEqual(response.status_code, 200)
        print("✓ Gestor pode acessar dashboard do gestor")
        
        # Testar acesso do almoxarife
        almoxarife = self.login_user('almoxarife')
        response = self.client.get(reverse('core:almoxarife_dashboard'))
        self.assertEqual(response.status_code, 200)
        print("✓ Almoxarife pode acessar dashboard do almoxarife")
        
        # Testar que encarregado não pode acessar dashboard do gestor
        encarregado = self.login_user('encarregado_flv')
        response = self.client.get(reverse('core:gestor_dashboard'))
        self.assertEqual(response.status_code, 403)  # Forbidden
        print("✓ Encarregado não pode acessar dashboard do gestor")
        
        # Testar que encarregado não pode acessar dashboard do almoxarife
        response = self.client.get(reverse('core:almoxarife_dashboard'))
        self.assertEqual(response.status_code, 403)  # Forbidden
        print("✓ Encarregado não pode acessar dashboard do almoxarife")

    def test_atualizacao_kpis_tempo_real(self):
        """Testa se os KPIs são atualizados em tempo real"""
        print("\n=== Testando atualização de KPIs em tempo real ===")
        
        gestor = self.login_user('gestor')
        
        # Verificar KPIs iniciais
        response = self.client.get(reverse('core:gestor_dashboard'))
        context_inicial = response.context
        pendentes_inicial = context_inicial['pendentes']
        print(f"✓ Pendentes iniciais: {pendentes_inicial}")
        
        # Criar nova requisição
        nova_requisicao = self.criar_requisicao_fake(
            'encarregado_comercial', 'Comercial', 
            status=RequestStatus.PENDING
        )
        print(f"✓ Nova requisição criada: {nova_requisicao.request_code}")
        
        # Verificar se KPIs foram atualizados
        response = self.client.get(reverse('core:gestor_dashboard'))
        context_final = response.context
        pendentes_final = context_final['pendentes']
        
        self.assertEqual(pendentes_final, pendentes_inicial + 1)
        print(f"✓ Pendentes após nova requisição: {pendentes_final}")

    def test_estatisticas_por_setor(self):
        """Testa se as estatísticas por setor estão funcionando"""
        print("\n=== Testando estatísticas por setor ===")
        
        # Criar requisições para diferentes setores
        setores_test = ['FLV', 'Frios', 'Padaria', 'Açougue']
        
        for setor in setores_test:
            # Criar 3 requisições para cada setor
            for i in range(3):
                self.criar_requisicao_fake(
                    f'encarregado_{setor.lower()}', 
                    setor, 
                    status=random.choice([RequestStatus.PENDING, RequestStatus.APPROVED])
                )
        
        gestor = self.login_user('gestor')
        response = self.client.get(reverse('core:gestor_dashboard'))
        context = response.context
        
        # Verificar se os dados dos gráficos estão sendo gerados
        self.assertIsNotNone(context.get('setores_labels'))
        self.assertIsNotNone(context.get('setores_data'))
        self.assertIsNotNone(context.get('status_labels'))
        self.assertIsNotNone(context.get('status_data'))
        
        print(f"✓ Gráficos gerados com sucesso:")
        print(f"  - Setores: {context['setores_labels']}")
        print(f"  - Dados setores: {context['setores_data']}")
        print(f"  - Status: {context['status_labels']}")
        print(f"  - Dados status: {context['status_data']}")

    def test_requisicoes_urgentes(self):
        """Testa o tratamento de requisições urgentes"""
        print("\n=== Testando requisições urgentes ===")
        
        # Criar requisições urgentes
        for i in range(5):
            self.criar_requisicao_fake(
                'encarregado_flv', 'FLV', 
                status=RequestStatus.PENDING,
                urgency=Urgency.URGENTE
            )
        
        gestor = self.login_user('gestor')
        response = self.client.get(reverse('core:gestor_dashboard'))
        context = response.context
        
        self.assertEqual(context['urgentes_pendentes'], 5)
        print(f"✓ Requisições urgentes pendentes: {context['urgentes_pendentes']}")

    def test_tempo_medio_atendimento(self):
        """Testa o cálculo do tempo médio de atendimento"""
        print("\n=== Testando tempo médio de atendimento ===")
        
        # Criar requisições aprovadas com diferentes tempos
        hoje = timezone.now()
        
        # Requisição aprovada rapidamente (1 hora)
        req_rapida = self.criar_requisicao_fake(
            'encarregado_flv', 'FLV', 
            status=RequestStatus.APPROVED
        )
        req_rapida.created_at = hoje - timedelta(hours=2)
        req_rapida.updated_at = hoje - timedelta(hours=1)
        req_rapida.save()
        
        # Requisição aprovada lentamente (24 horas)
        req_lenta = self.criar_requisicao_fake(
            'encarregado_frios', 'Frios', 
            status=RequestStatus.APPROVED
        )
        req_lenta.created_at = hoje - timedelta(hours=25)
        req_lenta.updated_at = hoje - timedelta(hours=1)
        req_lenta.save()
        
        gestor = self.login_user('gestor')
        response = self.client.get(reverse('core:gestor_dashboard'))
        context = response.context
        
        # Verificar se o tempo médio está sendo calculado
        self.assertIsNotNone(context.get('tempo_medio'))
        self.assertIsNotNone(context.get('tempo_medio_str'))
        
        print(f"✓ Tempo médio calculado: {context['tempo_medio_str']}")

    def test_percentual_atendidas_prazo(self):
        """Testa o cálculo do percentual de requisições atendidas no prazo"""
        print("\n=== Testando percentual atendidas no prazo ===")
        
        hoje = timezone.now()
        
        # Criar requisições aprovadas no prazo (menos de 24h)
        for i in range(3):
            req = self.criar_requisicao_fake(
                f'encarregado_flv', 'FLV', 
                status=RequestStatus.APPROVED
            )
            req.created_at = hoje - timedelta(hours=12)
            req.updated_at = hoje - timedelta(hours=1)
            req.save()
        
        # Criar requisições aprovadas fora do prazo (mais de 24h)
        for i in range(2):
            req = self.criar_requisicao_fake(
                f'encarregado_frios', 'Frios', 
                status=RequestStatus.APPROVED
            )
            req.created_at = hoje - timedelta(hours=25)
            req.updated_at = hoje - timedelta(hours=1)
            req.save()
        
        gestor = self.login_user('gestor')
        response = self.client.get(reverse('core:gestor_dashboard'))
        context = response.context
        
        # Verificar percentual (3 no prazo / 5 total = 60%)
        self.assertGreater(context['pct_no_prazo'], 0)
        print(f"✓ Percentual no prazo: {context['pct_no_prazo']}%")

    def test_criar_muitas_requisicoes_fake(self):
        """Testa criação de muitas requisições falsas para stress test"""
        print("\n=== Testando criação de muitas requisições ===")
        
        # Criar 50 requisições com diferentes características
        for i in range(50):
            setor = random.choice(list(self.setores.keys()))
            status = random.choice(list(RequestStatus.choices))[0]
            urgency = random.choice(list(Urgency.choices))[0]
            encarregado_key = f'encarregado_{setor.lower()}'
            
            req = self.criar_requisicao_fake(
                encarregado_key, setor, 
                status=status, urgency=urgency,
                num_items=random.randint(1, 5)
            )
            
            if i % 10 == 0:
                print(f"✓ Criadas {i+1} requisições...")
        
        # Verificar se todas foram criadas
        total_requisicoes = Request.objects.count()
        self.assertEqual(total_requisicoes, 50)
        print(f"✓ Total de requisições criadas: {total_requisicoes}")
        
        # Verificar se os KPIs ainda funcionam com muitos dados
        gestor = self.login_user('gestor')
        response = self.client.get(reverse('core:gestor_dashboard'))
        self.assertEqual(response.status_code, 200)
        print("✓ Dashboard do gestor funciona com muitos dados")

    def test_verificar_codigos_requisicao(self):
        """Testa se os códigos de requisição estão sendo gerados corretamente"""
        print("\n=== Testando códigos de requisição ===")
        
        # Criar requisições para diferentes setores
        setores_codigos = {
            'FLV': 'F',
            'Frios': 'FR', 
            'Padaria': 'PD',
            'Açougue': 'AC',
            'ADM': 'ADM',
            'Deposito': 'DP',
            'Limpeza': 'LP',
            'Comercial': 'CM',
            'Loja': 'LJ'
        }
        
        for setor_nome, codigo_esperado in setores_codigos.items():
            req = self.criar_requisicao_fake(
                f'encarregado_{setor_nome.lower()}', 
                setor_nome
            )
            
            # Verificar se o código foi gerado corretamente
            self.assertIsNotNone(req.request_code)
            self.assertTrue(req.request_code.startswith(codigo_esperado))
            print(f"✓ Código gerado para {setor_nome}: {req.request_code}")

    def test_estatisticas_por_categoria(self):
        """Testa as estatísticas por categoria de item"""
        print("\n=== Testando estatísticas por categoria ===")
        
        # Criar requisições com diferentes categorias
        categorias = list(ItemCategory.choices)
        
        for categoria in categorias:
            for i in range(2):  # 2 itens por categoria
                req = self.criar_requisicao_fake(
                    'encarregado_flv', 'FLV'
                )
                # Atualizar categoria do primeiro item
                if req.items.exists():
                    item = req.items.first()
                    item.category = categoria[0]
                    item.save()
        
        gestor = self.login_user('gestor')
        response = self.client.get(reverse('core:gestor_dashboard'))
        context = response.context
        
        # Verificar se os dados das categorias estão sendo gerados
        self.assertIsNotNone(context.get('categorias_labels'))
        self.assertIsNotNone(context.get('categorias_data'))
        
        print(f"✓ Estatísticas por categoria geradas:")
        print(f"  - Categorias: {context['categorias_labels']}")
        print(f"  - Dados: {context['categorias_data']}")

    def run_all_tests(self):
        """Executa todos os testes em sequência"""
        print("🚀 Iniciando testes completos do sistema Requisição Fácil")
        print("=" * 60)
        
        # Executar todos os testes
        test_methods = [
            'test_criar_requisicoes_fake_para_todos_setores',
            'test_kpis_gestor_apos_criar_requisicoes',
            'test_fluxo_completo_requisicao',
            'test_permissoes_usuarios',
            'test_atualizacao_kpis_tempo_real',
            'test_estatisticas_por_setor',
            'test_requisicoes_urgentes',
            'test_tempo_medio_atendimento',
            'test_percentual_atendidas_prazo',
            'test_criar_muitas_requisicoes_fake',
            'test_verificar_codigos_requisicao',
            'test_estatisticas_por_categoria'
        ]
        
        for test_method in test_methods:
            try:
                getattr(self, test_method)()
                print(f"✅ {test_method} - PASSOU")
            except Exception as e:
                print(f"❌ {test_method} - FALHOU: {str(e)}")
        
        print("\n" + "=" * 60)
        print("🎉 Testes completos finalizados!")
        print("=" * 60)
