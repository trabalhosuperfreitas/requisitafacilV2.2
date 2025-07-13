from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from core.models import (
    User, Sector, Request, RequestItem, Role, 
    RequestStatus, Urgency, ItemCategory
)

class Command(BaseCommand):
    help = 'Gera dados de teste para o sistema Requisição Fácil'

    def add_arguments(self, parser):
        parser.add_argument(
            '--num-requisicoes',
            type=int,
            default=100,
            help='Número de requisições a serem criadas (padrão: 100)'
        )
        parser.add_argument(
            '--setores',
            nargs='+',
            default=['FLV', 'Frios', 'Padaria', 'Açougue', 'ADM', 'Deposito', 'Limpeza', 'Comercial', 'Loja'],
            help='Lista de setores para criar requisições'
        )
        parser.add_argument(
            '--dias-atras',
            type=int,
            default=30,
            help='Número de dias para trás para criar requisições (padrão: 30)'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Iniciando geração de dados de teste...')
        )
        
        num_requisicoes = options['num_requisicoes']
        setores_nomes = options['setores']
        dias_atras = options['dias_atras']
        
        # Criar setores se não existirem
        setores = {}
        for nome in setores_nomes:
            setor, created = Sector.objects.get_or_create(name=nome)
            setores[nome] = setor
            if created:
                self.stdout.write(f"✓ Setor criado: {nome}")
        
        # Criar usuários se não existirem
        users = {}
        
        # Gestor
        gestor, created = User.objects.get_or_create(
            username='gestor_teste',
            defaults={
                'email': 'gestor@teste.com',
                'password': 'testpass123',
                'role': Role.Gestor,
                'first_name': 'João',
                'last_name': 'Gestor Teste'
            }
        )
        if created:
            gestor.set_password('testpass123')
            gestor.save()
            self.stdout.write("✓ Gestor criado")
        users['gestor'] = gestor
        
        # Almoxarife
        almoxarife, created = User.objects.get_or_create(
            username='almoxarife_teste',
            defaults={
                'email': 'almoxarife@teste.com',
                'password': 'testpass123',
                'role': Role.Almoxarife,
                'first_name': 'Maria',
                'last_name': 'Almoxarife Teste'
            }
        )
        if created:
            almoxarife.set_password('testpass123')
            almoxarife.save()
            self.stdout.write("✓ Almoxarife criado")
        users['almoxarife'] = almoxarife
        
        # Encarregados para cada setor
        for nome_setor in setores_nomes:
            username = f'encarregado_{nome_setor.lower()}_teste'
            encarregado, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@teste.com',
                    'password': 'testpass123',
                    'role': Role.Encarregado,
                    'first_name': f'Encarregado',
                    'last_name': nome_setor,
                    'sector': setores[nome_setor]
                }
            )
            if created:
                encarregado.set_password('testpass123')
                encarregado.save()
                self.stdout.write(f"✓ Encarregado criado para {nome_setor}")
            users[f'encarregado_{nome_setor.lower()}'] = encarregado
        
        # Itens disponíveis para requisições
        itens_disponiveis = [
            "Papel A4", "Caneta", "Lápis", "Borracha", "Régua", "Tesoura",
            "Cola", "Fita adesiva", "Post-it", "Grampeador", "Clips",
            "Envelope", "Cartolina", "EVA", "Tinta", "Pincel", "Pano",
            "Detergente", "Desinfetante", "Papel higiênico", "Sabão",
            "Luvas", "Máscaras", "Álcool", "Lixeira", "Vassoura",
            "Rodo", "Balde", "Esponja", "Saco de lixo", "Fita crepe"
        ]
        
        # Criar requisições
        self.stdout.write(f"📝 Criando {num_requisicoes} requisições...")
        
        hoje = timezone.now()
        requisicoes_criadas = 0
        
        for i in range(num_requisicoes):
            # Escolher setor aleatório
            setor_nome = random.choice(setores_nomes)
            setor = setores[setor_nome]
            encarregado = users[f'encarregado_{setor_nome.lower()}']
            
            # Escolher status com distribuição realista
            status_weights = {
                RequestStatus.PENDING: 0.3,      # 30% pendentes
                RequestStatus.EM_ATENDIMENTO: 0.2,  # 20% em atendimento
                RequestStatus.APPROVED: 0.5       # 50% aprovadas
            }
            status = random.choices(
                list(status_weights.keys()),
                weights=list(status_weights.values())
            )[0]
            
            # Escolher urgência
            urgency = random.choice(list(Urgency.choices))[0]
            
            # Data aleatória nos últimos dias
            dias_aleatorios = random.randint(0, dias_atras)
            data_criacao = hoje - timedelta(days=dias_aleatorios)
            
            # Criar requisição
            requisicao = Request.objects.create(
                requester=encarregado,
                sector=setor,
                urgency=urgency,
                observations=f"Observação teste {i+1} para {setor_nome}",
                status=status,
                created_at=data_criacao
            )
            
            # Definir data de atualização baseada no status
            if status == RequestStatus.APPROVED:
                # Se aprovada, definir data de atualização posterior
                horas_aleatorias = random.randint(1, 48)
                requisicao.updated_at = data_criacao + timedelta(hours=horas_aleatorias)
                requisicao.atendido_por = users['almoxarife']
            elif status == RequestStatus.EM_ATENDIMENTO:
                # Se em atendimento, definir almoxarife
                requisicao.atendido_por = users['almoxarife']
            
            requisicao.save()
            
            # Criar itens da requisição
            num_items = random.randint(1, 5)
            for j in range(num_items):
                categoria = random.choice(list(ItemCategory.choices))[0]
                item_nome = random.choice(itens_disponiveis)
                quantidade = random.randint(1, 20)
                quantidade_atendida = 0
                
                if status == RequestStatus.APPROVED:
                    # Se aprovada, definir quantidade atendida
                    quantidade_atendida = random.randint(0, quantidade)
                
                RequestItem.objects.create(
                    request=requisicao,
                    item_requested=item_nome,
                    quantify=quantidade,
                    category=categoria,
                    quantidade_atendida=quantidade_atendida,
                    observacao_item=f"Observação do item {j+1}"
                )
            
            requisicoes_criadas += 1
            
            if requisicoes_criadas % 10 == 0:
                self.stdout.write(f"✓ {requisicoes_criadas} requisições criadas...")
        
        # Estatísticas finais
        total_requisicoes = Request.objects.count()
        pendentes = Request.objects.filter(status=RequestStatus.PENDING).count()
        em_atendimento = Request.objects.filter(status=RequestStatus.EM_ATENDIMENTO).count()
        aprovadas = Request.objects.filter(status=RequestStatus.APPROVED).count()
        urgentes = Request.objects.filter(urgency=Urgency.URGENTE).count()
        
        self.stdout.write(
            self.style.SUCCESS(f"\n🎉 Dados de teste gerados com sucesso!")
        )
        self.stdout.write(f"📊 Estatísticas:")
        self.stdout.write(f"   - Total de requisições: {total_requisicoes}")
        self.stdout.write(f"   - Pendentes: {pendentes}")
        self.stdout.write(f"   - Em atendimento: {em_atendimento}")
        self.stdout.write(f"   - Aprovadas: {aprovadas}")
        self.stdout.write(f"   - Urgentes: {urgentes}")
        self.stdout.write(f"   - Setores ativos: {len(setores)}")
        self.stdout.write(f"   - Usuários criados: {len(users)}")
        
        self.stdout.write(
            self.style.SUCCESS(f"\n🔗 Para testar o sistema:")
        )
        self.stdout.write(f"   - Acesse: http://localhost:8000")
        self.stdout.write(f"   - Login como gestor: gestor_teste / testpass123")
        self.stdout.write(f"   - Login como almoxarife: almoxarife_teste / testpass123")
        self.stdout.write(f"   - Login como encarregado: encarregado_flv_teste / testpass123")
        
        self.stdout.write(
            self.style.SUCCESS(f"\n🧪 Para executar os testes:")
        )
        self.stdout.write(f"   - python manage.py test core.tests.RequisicaoFacilTestCase") 