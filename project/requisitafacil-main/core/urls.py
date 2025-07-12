from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # URL para a página inicial. A 'home_view' será definida no views.py.
    # Por enquanto, ela vai apenas redirecionar o usuário logado.
    path('', views.home_view, name='home'),
    path('requisicoes/criar/',views.criar_requisicao,name='criar_requisicao'),
    path('requisicoes/',views.listar_requisicoes,name='listar_requisicoes'),
    path('requisicoes/<uuid:pk>/',views.detalhe_requisicao,name='detalhe_requisicao'),
    path('requisicoes/<uuid:pk>/excluir/',views.excluir_requisicao,name='excluir_requisicao'),
    path('requisicao/<uuid:pk>/iniciar-atendimento/', views.iniciar_atendimento_requisicao, name='iniciar_atendimento_requisicao'),
    path('usuarios/criar/', views.criar_usuario, name='criar_usuario'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('almoxarife/dashboard/', views.almoxarife_dashboard, name='almoxarife_dashboard'),
    path('almoxarife/atender_requisicao/<uuid:pk>/', views.almoxarife_atender_requisicao, name='almoxarife_atender_requisicao'),
    path('gestor/dashboard/', views.gestor_dashboard, name='gestor_dashboard'),
]