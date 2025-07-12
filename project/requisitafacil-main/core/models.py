from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class Role(models.TextChoices):
    Gestor = 'Gestor', 'Gestor'
    Encarregado = 'Encarregado', 'Encarregado'
    Almoxarife = 'Almoxarife', 'Almoxarife'

class Sector(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome do Setor")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'
        ordering = ['name'] #Ordernar por nome Padrão

    def __str__(self):
        return self.name
    
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.Almoxarife,
        verbose_name='Função',
    )
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, blank=True, null=True)
    
    is_active = models.BooleanField(default=True, verbose_name="Ativo")

    # Se quiser usar o email como login principal:
    USERNAME_FIELD = 'email'  # Ou 'email' se quiser autenticar por email
    REQUIRED_FIELDS = ['username']  # Garante que o email é obrigatório no admin

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        
    def __str__(self):
        return self.get_full_name() or self.email

class ItemCategory(models.TextChoices):
    INSUMO_PRODUCAO = 'INSUMO_PRODUCAO', 'Insumo(Produção)'
    EMBALAGENS = 'EMBALAGENS', 'Embalagens'
    LIMPEZA = 'LIMPEZA', 'Limpeza'
    AREA_DE_VENDA = 'AREA_DE_VENDA', 'Area de venda'
    ADMINISTRATIVO = 'ADIMINISTRATIVO', 'Administrativo'

class Urgency(models.TextChoices):
    NORMAL = 'NORMAL', 'Normal'
    URGENTE = 'URGENTE', 'Urgente'

class RequestStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pendente'
    EM_ATENDIMENTO = 'EM_ATENDIMENTO', 'Em Atendimento'
    APPROVED = 'APPROVED', 'Atendida'
    
class Request(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable=False)
    
    #Quem fez a requisição
    requester = models.ForeignKey(User,
        on_delete=models.PROTECT,
        related_name='requests_made',
        verbose_name="Requisitante",
    )

    atendido_por = models.ForeignKey(User,
        on_delete=models.SET_NULL,
        related_name='requests_attended',
        verbose_name="Atendido por",
        null=True, blank=True
    )

    sector = models.ForeignKey(Sector,
        on_delete=models.PROTECT,
        related_name='requests_from_sector',
        verbose_name="Setor",
    )

    request_code = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="Código da Requisição")

    urgency = models.CharField(
        max_length=10,
        choices=Urgency.choices,
        default=Urgency.NORMAL,
        verbose_name="Urgência",
    )
    observations = models.TextField(max_length=255, verbose_name="Observações")

    #Status da Requisição
    status = models.CharField(
        max_length=15,
        choices=RequestStatus.choices,
        default=RequestStatus.PENDING,
        verbose_name="Status",
    )

    #Campos de controle de data e Horario
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data da Requisição")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ultima Atualização")

    class Meta:
        verbose_name = 'Requisição'
        verbose_name_plural = 'Requisições'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.request_code or self.id} - {self.requester.get_full_name() or self.requester.username}'

    def save(self, *args, **kwargs):
        if not self.request_code and self.sector:
            # Mapeamento de setores para abreviações
            setor_abreviacoes = {
                "FLV": "F",
                "Frios": "FR",
                "Padaria": "PD",
                "Açougue": "AC",
                "ADM": "ADM",
                "Deposito": "DP",
                "Limpeza": "LP",
                "Comercial": "CM",
                "Loja": "LJ",
            }
            abreviacao = setor_abreviacoes.get(self.sector.name, "GEN") # GEN para genérico se não mapeado
            
            # Encontra o próximo número sequencial para o setor
            last_request = Request.objects.filter(request_code__startswith=abreviacao).order_by('-created_at').first()
            if last_request and last_request.request_code:
                try:
                    last_number = int(last_request.request_code.split('-')[-1])
                    next_number = last_number + 1
                except (ValueError, IndexError):
                    next_number = 1
            else:
                next_number = 1
            
            self.request_code = f'{abreviacao}-{next_number}'

        super().save(*args, **kwargs)

class RequestItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='items', verbose_name="Requisição")
    item_requested = models.CharField(max_length=255, verbose_name="Item Solicitado")
    quantify = models.PositiveIntegerField(verbose_name="Quantidade")
    category = models.CharField(
        max_length=50,
        choices=ItemCategory.choices,
        verbose_name="Categoria",
    )
    quantidade_atendida = models.PositiveIntegerField(default=0, verbose_name="Quantidade Atendida")
    observacao_item = models.CharField(max_length=255, blank=True, null=True, verbose_name="Observação do Item")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Item da Requisição'
        verbose_name_plural = 'Itens da Requisição'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.item_requested} ({self.quantify}) - Req: {self.request.request_code or self.request.id}"