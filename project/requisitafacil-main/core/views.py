from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q, ExpressionWrapper, F
from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from .forms import RequestForm, CustomUserCreationForm, RequestItemFormSet
from .models import Request, Role, RequestStatus, RequestItem

from django.views.decorators.http import require_POST

# --- Funções Auxiliares de Permissão ---
# Usamos essas funções para verificar o papel do usuário logado
def is_almoxarife(user):
    return user.is_authenticated and user.role == Role.Almoxarife

def is_gestor(user):
    return user.is_authenticated and user.role == Role.Gestor


# ----Views Principais----

@login_required
def home_view(request):
    if request.user.role == Role.Gestor:
        return redirect('core:gestor_dashboard')
    return redirect('core:dashboard')
    
@login_required
def criar_requisicao(request):
    data_today = timezone.localdate()
    # Obtém estatísticas de requisições
    user_requests = Request.objects.filter(requester=request.user)
    context = {
        'pending_requests': user_requests.filter(status=RequestStatus.PENDING).count(),
        'approved_requests': user_requests.filter(status=RequestStatus.APPROVED).count(),
        'total_requests': user_requests.count(),
        'data_today': data_today,
    }

    if request.method == 'POST':
        form = RequestForm(request.POST)
        formset = RequestItemFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                requisicao = form.save(commit=False)
                requisicao.requester = request.user

                if request.user.sector:
                    requisicao.sector = request.user.sector
                else:
                    form.add_error(None, 'Seu usuário não possui um setor cadastrado. Por favor, entre em contato com o gestor para que ele seja associado a um setor.')
                    context['form'] = form
                    context['formset'] = formset
                    return render(request, 'core/criar_requisicao.html', context)
                
                requisicao.save()
                formset.instance = requisicao
                formset.save()

            messages.success(request, 'Requisição criada com sucesso!')
            return redirect('core:listar_requisicoes')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário abaixo.')
    else:
        form = RequestForm()
        formset = RequestItemFormSet()

    context['form'] = form
    context['formset'] = formset
    return render(request, 'core/criar_requisicao.html', context)

@login_required
def listar_requisicoes(request):
    #Define o queryset base para as requisições
    if is_gestor(request.user):
        requisicoes_querysets = Request.objects.all()
    elif is_almoxarife(request.user):
        requisicoes_querysets = Request.objects.all()
    elif request.user.role == Role.Encarregado:
        requisicoes_querysets = Request.objects.filter(requester=request.user)
    else:
        requisicoes_querysets = Request.objects.filter(requester=request.user)

    
    status_filter = request.GET.get('status')
    if status_filter and status_filter in RequestStatus.values:
        requisicoes_querysets = requisicoes_querysets.filter(status=status_filter)

    # Filtro por data (opcional, se já existir no template)
    data_filter = request.GET.get('data')
    if data_filter:
        requisicoes_querysets = requisicoes_querysets.filter(created_at__date=data_filter)

    requisicoes = requisicoes_querysets.order_by('-created_at')

    context = {
        'requisicoes' : requisicoes,
        'RequestStatus': RequestStatus,
        'current_status': status_filter,
    }
    return render(request, 'core/listar_requisicoes.html', context)

@login_required
def detalhe_requisicao(request, pk):
    # Tenta pegar a requisição pelo UUID (pk) ou retorna erro 404 se não encontrar
    requisicao = get_object_or_404(Request, pk=pk)

    #Verifica permisão de acesso
    if not (is_almoxarife(request.user) or is_gestor(request.user) or requisicao.requester == request.user):
        messages.error(request, 'Você não tem permissão para acessar essa requisição')
        return redirect('core:listar_requisicoes')
    
    return render(request, 'core/detalhe_requisicao.html', {'requisicao': requisicao})

@login_required
def excluir_requisicao(request,pk):
    requisicao = get_object_or_404(Request, pk=pk)

    # Permite excluir APENAS se:
    # 1. O usuário logado é o mesmo que criou a requisição E
    # 2. O status da requisição ainda é PENDENTE
    if requisicao.requester == request.user and requisicao.status == RequestStatus.PENDING:
        if request.method == 'POST':
            requisicao.delete()
            messages.success(request, 'Requisição excluida com sucesso!')
            return redirect('core:listar_requisicoes')
         # Se for GET (primeira vez acessando a URL), mostra a página de confirmação
        return render(request, 'core/confirmar_exclusao.html', {'requisicao': requisicao})
    else:
        messages.error(request, 'Você não tem permissão para excluir esta requisição ou ela não está mais pendente.')
        return redirect('core:listar_requisicoes')

@login_required
def criar_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('core:listar_requisicoes')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/criar_usuario.html', {'form': form})

@login_required
def dashboard(request):
    now = timezone.now()
    papel = request.user.role
    today = timezone.localdate()

    # Filtra as requisições do dia com base no papel do usuário
    if papel == Role.Encarregado:
        # Encarregado vê apenas as suas requisições do dia
        requisicoes_do_dia = Request.objects.filter(requester=request.user, created_at__date=today).order_by('-created_at')
    else:
        # Outros papéis (Gestor, Almoxarife) veem todas as requisições do dia
        requisicoes_do_dia = Request.objects.filter(created_at__date=today).order_by('-created_at')

    context = {
        'now': now,
        'user': request.user,
        'papel': papel,
        'requisicoes_do_dia': requisicoes_do_dia,
        'data_today': today,
    }

    # --- Estatísticas do Painel (cards) ---
    stats_qs = Request.objects.all()
    user_stats_qs = Request.objects.filter(requester=request.user)
    if papel == Role.Encarregado:
        pendentes = user_stats_qs.filter(status=RequestStatus.PENDING).count()
        aprovadas_hoje = user_stats_qs.filter(status=RequestStatus.APPROVED, updated_at__date=today).count()
        total_mes = user_stats_qs.filter(created_at__month=now.month, created_at__year=now.year).count()
        context.update({
            'pendentes': pendentes,
            'aprovadas_hoje': aprovadas_hoje,
            'total_mes': total_mes,
        })
    else: # Gestor e Almoxarife
        pendentes = stats_qs.filter(status=RequestStatus.PENDING).count()
        em_atendimento = stats_qs.filter(status=RequestStatus.EM_ATENDIMENTO).count()
        aprovadas_hoje = stats_qs.filter(status=RequestStatus.APPROVED, updated_at__date=today).count()
        context.update({
            'pendentes': pendentes,
            'em_atendimento': em_atendimento,
            'aprovadas_hoje': aprovadas_hoje,
        })

    # --- Alertas ---
    alertas = []
    urgentes_pendentes = Request.objects.filter(status=RequestStatus.PENDING, urgency='URGENTE').count()
    if urgentes_pendentes > 3:
        alertas.append({
            'tipo': 'danger',
            'titulo': 'Requisições urgentes pendentes!',
            'descricao': f'Há {urgentes_pendentes} requisições urgentes aguardando atendimento.',
            'acao_url': '/requisicoes/?status=PENDING&urgency=URGENTE',
        })
    context['alertas'] = alertas

    # --- Tabela de Requisições Recentes/Ativas ---
    base_recentes_qs = Request.objects.all()
    if papel == Role.Encarregado:
        base_recentes_qs = Request.objects.filter(requester=request.user)
    
    # Prioriza requisições ativas (Em Atendimento e Pendentes)
    recentes_qs = base_recentes_qs.filter(
        Q(status=RequestStatus.EM_ATENDIMENTO) | Q(status=RequestStatus.PENDING)
    ).order_by('-updated_at')[:5]

    recentes = []
    for req in recentes_qs:
        if req.status == RequestStatus.PENDING:
            status_cor = 'warning'
        elif req.status == RequestStatus.EM_ATENDIMENTO:
            status_cor = 'primary'
        elif req.status == RequestStatus.APPROVED:
            status_cor = 'success'
        else:
            status_cor = 'secondary'

        recentes.append({
            'status': dict(RequestStatus.choices).get(req.status, req.status),
            'status_cor': status_cor,
            'request_code': req.request_code,
            'first_item': req.items.first().item_requested if req.items.exists() else 'N/A',
            'solicitante': req.requester.get_full_name() or req.requester.username,
            'setor': req.sector.name if req.sector else '',
            'data': req.updated_at, # Usar updated_at para refletir atividade recente
            'id': req.id
        })
    context['recentes'] = recentes
    
    return render(request, 'core/dashboard.html', context)

@login_required
@user_passes_test(is_almoxarife)
@require_POST
def iniciar_atendimento_requisicao(request, pk):
    requisicao = get_object_or_404(Request, pk=pk)
    if requisicao.status == RequestStatus.PENDING:
        requisicao.status = RequestStatus.EM_ATENDIMENTO
        requisicao.atendido_por = request.user
        requisicao.save()
        messages.info(request, f'Você iniciou o atendimento da requisição {requisicao.request_code}.')
        return redirect('core:almoxarife_atender_requisicao', pk=requisicao.pk)
    else:
        messages.warning(request, 'Esta requisição não está pendente.')
        return redirect('core:listar_requisicoes')

@login_required
@user_passes_test(is_almoxarife)
def almoxarife_dashboard(request):
    requisicoes_pendentes = Request.objects.filter(status=RequestStatus.PENDING).order_by('-created_at')
    context = {
        'requisicoes_pendentes': requisicoes_pendentes,
    }
    return render(request, 'core/almoxarife_dashboard_requests.html', context)

@login_required
@user_passes_test(is_almoxarife)
def almoxarife_atender_requisicao(request, pk):
    requisicao = get_object_or_404(Request, pk=pk)

    if request.method == 'POST':
        try:
            with transaction.atomic():
                item_ids = request.POST.getlist('item_id')
                quantidades = request.POST.getlist('quantidade_atendida')
                observacoes = request.POST.getlist('observacao_item')

                # Verificação de consistência dos dados do formulário
                if not (len(item_ids) == len(quantidades) == len(observacoes)):
                    messages.error(request, 'Erro de inconsistência nos dados do formulário. Tente novamente.')
                    return redirect('core:almoxarife_atender_requisicao', pk=pk)

                for i, item_id in enumerate(item_ids):
                    try:
                        item = RequestItem.objects.get(id=item_id, request=requisicao)
                        quantidade_str = quantidades[i]
                        item.quantidade_atendida = int(quantidade_str) if quantidade_str.isdigit() else 0
                        item.observacao_item = observacoes[i]
                        item.save()
                    except RequestItem.DoesNotExist:
                        # Ignora se um item não pertencer a esta requisição por segurança
                        continue
                    except (ValueError, IndexError) as e:
                        raise Exception(f"Erro ao processar o item {item_id}: {e}")

                # Atualiza o status da requisição principal
                requisicao.status = RequestStatus.APPROVED
                # Adiciona as observações do atendimento ao campo já existente.
                obs_finais = request.POST.get('observacoes_atendimento', '')
                if obs_finais:
                    requisicao.observations = f"{requisicao.observations or ''}\n\n--- Observações do Atendimento ---\n{obs_finais}"
                requisicao.save()

            messages.success(request, f'Requisição {requisicao.request_code} finalizada com sucesso!')
            return redirect('core:listar_requisicoes')
        except Exception as e:
            messages.error(request, f'Ocorreu um erro ao finalizar a requisição: {e}')
            return redirect('core:almoxarife_atender_requisicao', pk=pk)

    # Lógica para GET
    if requisicao.status == RequestStatus.PENDING:
        requisicao.status = RequestStatus.EM_ATENDIMENTO
        requisicao.atendido_por = request.user
        requisicao.save()
    elif requisicao.status == RequestStatus.EM_ATENDIMENTO and requisicao.atendido_por != request.user:
        messages.error(request, f'Esta requisição já está sendo atendida por {requisicao.atendido_por.get_full_name()}.')
        return redirect('core:listar_requisicoes')
    elif requisicao.status not in [RequestStatus.PENDING, RequestStatus.EM_ATENDIMENTO]:
        messages.warning(request, 'Esta requisição não pode mais ser atendida.')
        return redirect('core:listar_requisicoes')

    context = {
        'requisicao': requisicao
    }
    return render(request, 'core/almoxarife_atender_requisicao.html', context)


@login_required
@user_passes_test(is_gestor)
def gestor_dashboard(request):
    today = timezone.localdate()


    requisicoes_do_dia = Request.objects.all().order_by('-created_at')

    pendentes = Request.objects.filter(status=RequestStatus.PENDING).order_by().count()
    aprovadas_hoje = Request.objects.filter(status=RequestStatus.APPROVED, updated_at__date=today).count()
    total_mes = Request.objects.filter(created_at__month=today.month, created_at__year=today.year).count()
    departamentos_ativos = Request.objects.values('sector').distinct().count()

    context ={
        'requisicoes_do_dia': requisicoes_do_dia,
        'pendentes': pendentes,
        'aprovadas_hoje': aprovadas_hoje,
        'total_mes': total_mes,
        'departamentos_ativos': departamentos_ativos
    }
    return render(request, 'core/dashboard_gestor.html',context)