from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Sector, Request, RequestItem
from .forms import CustomUserCreationForm # Importa o formulário personalizado

# Register your models here.

#Classe para personalizar o admin do user customizado
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Usa o formulário personalizado para adicionar novos usuários
    add_form = CustomUserCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        ('Informações pessoais', {'fields': ('first_name', 'last_name')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Função e Setor', {'fields': ('role', 'sector')}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    # Define os fieldsets para adicionar novos usuários, incluindo o email
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role', 'sector'),
        }),
    )
    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'sector', 'is_staff')
    list_filter = BaseUserAdmin.list_filter + ('role', 'sector', 'is_active')
    search_fields = BaseUserAdmin.search_fields + ('sector__name',)
    ordering = ('email',)

admin.site.register(Sector)

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'requester', 'sector', 'request_code', 'urgency', 'created_at', 'status',
    )
    list_filter = ('status', 'urgency', 'sector')
    search_fields = (
        'request_code',
        'observations',
        'requester__username', 'requester__email',
        'sector__name',
    )
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('requester','sector','urgency','observations')
        }),
        ('status da Requisição', {
            'fields': ('status',)
        }),
        ('Datas de Controle',{
            'fields':('created_at','updated_at')
        }),
    )

admin.site.register(RequestItem)