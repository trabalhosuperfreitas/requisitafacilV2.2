from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from .models import User, Request, ItemCategory, Urgency, Sector, RequestItem

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        # Os campos que os usuarios irão preencher no formulario
        fields = ['urgency', 'observations']
        widgets = {'observations': forms.Textarea(attrs={'rows': 4})}

        labels = {
            'urgency': 'Urgência',
            'observations': 'Observações',
        }

        help_texts = {
            'urgency': 'Prazo padrão de atendimento',
            'observations': 'Informações adicionais sobre a requisição (opcional)',
        }

    # o metodo __init__ é chamado quando o formulario é instanciado
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Loop para percorrer todos os campos do formulario e usar na estilização bootstrap
        for field_name, field in self.fields.items():
            # Configuração da classe CSS para estilização Bootstrap
            field.widget.attrs['class'] = 'form-control'

            if field_name == 'urgency':
                field.widget.attrs['class'] = 'form-select'

            # Adicionando os placeholders para guiar o usuario
            if field_name == 'observations':
                field.widget.attrs['placeholder'] = 'Detalhes adicionais'


class RequestItemForm(forms.ModelForm):
    class Meta:
        model = RequestItem
        fields = ['item_requested', 'quantify', 'category']
        labels = {
            'item_requested': 'Item Solicitado',
            'quantify': 'Quantidade',
            'category': 'Categoria',
        }
        help_texts = {
            'item_requested': 'Ex: Caneta Azul, Papel A4, Grampeador',
            'quantify': 'Ex: 10',
            'category': 'Selecione a categoria do item',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'category':
                field.widget.attrs['class'] = 'form-select form-select-sm'
            else:
                field.widget.attrs['class'] = 'form-control form-control-sm'
            
            if field_name == 'item_requested':
                field.widget.attrs['placeholder'] = 'Nome do item'
            elif field_name == 'quantify':
                field.widget.attrs['placeholder'] = 'Qtd.'


RequestItemFormSet = inlineformset_factory(
    Request, 
    RequestItem, 
    form=RequestItemForm, 
    extra=1, 
    can_delete=True
)


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'role', 'sector')
        labels = {
            'username': 'Usuário',
            'email': 'E-mail',
            'role': 'Função',
            'sector': 'Setor',
        }
        widgets = {
            'password': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        # Sempre exibe o campo setor, sem lógica dinâmica aqui

    def clean_sector(self):
        role = self.cleaned_data.get('role')
        sector = self.cleaned_data.get('sector')
        if role == 'Encarregado' and not sector:
            raise forms.ValidationError("O setor deve ser selecionado para o papel de Encarregado.")
        return sector