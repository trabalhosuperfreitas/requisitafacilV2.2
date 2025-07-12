# Documentação do Projeto Requisita Fácil

## Visão Geral
O **Requisita Fácil** é um sistema web completo para gestão de requisições internas de materiais, desenvolvido em Django. O sistema oferece controle de permissões por papel (Almoxarife, Gestor, Encarregado), dashboards personalizados, filtros avançados e acompanhamento completo do ciclo de vida das requisições.

---

## 🏗️ Arquitetura do Sistema

### Tecnologias Utilizadas
- **Backend**: Django 4.2+
- **Frontend**: Bootstrap 5.3.3, CSS Customizado
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Autenticação**: Sistema nativo do Django
- **Interface**: Design responsivo com sidebar fixa

### Estrutura de Pastas
```
requisitafacil-main/
├── core/                          # App principal
│   ├── models.py                  # Modelos de dados
│   ├── views.py                   # Lógica das views
│   ├── forms.py                   # Formulários Django
│   ├── urls.py                    # Rotas do app
│   ├── admin.py                   # Configuração do admin
│   └── migrations/                # Migrações do banco
├── requisita_facil/              # Configurações do projeto
│   ├── settings.py               # Configurações globais
│   └── urls.py                   # Rotas globais
├── templates/                     # Templates HTML
│   ├── base.html                 # Template base
│   ├── core/                     # Templates das views
│   └── registration/             # Templates de auth
├── static/                       # Arquivos estáticos
│   └── style.css                 # CSS customizado
├── db.sqlite3                    # Banco de dados
├── requirements.txt              # Dependências
└── manage.py                    # Script de gerenciamento
```

---

## 📊 Modelos de Dados (`core/models.py`)

### User (Usuário Personalizado)
- **Herda de**: `AbstractUser`
- **Campos principais**:
  - `id`: UUID (chave primária)
  - `email`: Email único
  - `role`: Papel do usuário (Gestor, Encarregado, Almoxarife)
  - `sector`: Relacionamento com Sector
  - `is_active`: Status ativo/inativo

### Sector (Setor)
- **Campos**:
  - `id`: UUID
  - `name`: Nome do setor (único)
  - `created_at`, `updated_at`: Timestamps

### Request (Requisição)
- **Campos principais**:
  - `id`: UUID
  - `requester`: Usuário que criou a requisição
  - `atendido_por`: Usuário que atendeu
  - `sector`: Setor da requisição
  - `request_code`: Código único (ex: F-1, FR-2)
  - `urgency`: Urgência (Normal/Urgente)
  - `observations`: Observações gerais
  - `status`: Status (Pendente/Em Atendimento/Aprovada)
  - `created_at`, `updated_at`: Timestamps

### RequestItem (Item da Requisição)
- **Campos**:
  - `request`: Relacionamento com Request
  - `item_requested`: Nome do item
  - `quantify`: Quantidade solicitada
  - `category`: Categoria (Insumo, Embalagens, Limpeza, etc.)
  - `quantidade_atendida`: Quantidade efetivamente atendida
  - `observacao_item`: Observações específicas do item

### Enums e Choices
- **Role**: Gestor, Encarregado, Almoxarife
- **ItemCategory**: Insumo(Produção), Embalagens, Limpeza, Area de venda, Administrativo
- **Urgency**: Normal, Urgente
- **RequestStatus**: Pendente, Em Atendimento, Aprovada

---

## 🎯 Funcionalidades por Papel

### 👤 Encarregado
- **Criar requisições** para seu setor
- **Visualizar** apenas suas requisições
- **Dashboard** com estatísticas pessoais
- **Excluir** requisições pendentes próprias

### 🏢 Almoxarife
- **Visualizar** todas as requisições
- **Atender** requisições pendentes
- **Dashboard** específico para atendimento
- **Iniciar atendimento** de requisições
- **Finalizar** requisições com quantidades atendidas

### 👨‍💼 Gestor
- **Visualizar** todas as requisições
- **Dashboard** com estatísticas gerais
- **Criar usuários** do sistema
- **Monitorar** tendências e departamentos ativos
- **Acesso**: `/usuarios/criar/` (apenas para Gestores)

---

## 🔄 Fluxo de Requisição

### 1. Criação da Requisição
```
Encarregado → /criar_requisicao/ → Preenche formulário → Salva no banco
```

**Processo**:
- Usuário acessa formulário
- Preenche urgência e observações
- Adiciona itens (nome, quantidade, categoria)
- Sistema gera código único automaticamente
- Requisição salva com status "Pendente"

### 2. Atendimento da Requisição
```
Almoxarife → /almoxarife_dashboard/ → Seleciona requisição → Atende
```

**Processo**:
- Almoxarife vê requisições pendentes
- Inicia atendimento (status → "Em Atendimento")
- Preenche quantidades atendidas por item
- Adiciona observações do atendimento
- Finaliza (status → "Aprovada")

### 3. Acompanhamento
- **Encarregado**: Vê status das suas requisições
- **Gestor**: Monitora todas as requisições
- **Almoxarife**: Gerencia atendimento

---

## 🎨 Interface e Design

### Layout Principal
- **Sidebar fixa** com navegação
- **Design responsivo** (Bootstrap 5)
- **Tema escuro** personalizado
- **Ícones SVG** para melhor UX

### Componentes Principais
- **Cards de estatísticas** no dashboard
- **Tabelas responsivas** para listagens
- **Formulários dinâmicos** com formset
- **Alertas** para feedback do usuário
- **Badges** para status e urgência

### CSS Customizado (`static/style.css`)
- **Sidebar**: 260px de largura, tema escuro
- **Cards**: Design moderno com hover effects
- **Tabelas**: Responsivas com tema escuro
- **Formulários**: Estilização Bootstrap customizada

### Templates de Autenticação
- **Login** (`templates/registration/login.html`): Formulário de login responsivo
- **Criar Usuário** (`templates/core/criar_usuario.html`): Formulário de cadastro (apenas Gestores)
- **Base** (`templates/base.html`): Template base com sidebar e navegação

---

## 🔧 Views Principais (`core/views.py`)

### Views de Navegação
- `home_view()`: Redireciona baseado no papel
- `dashboard()`: Dashboard geral
- `gestor_dashboard()`: Dashboard específico do gestor
- `almoxarife_dashboard()`: Dashboard do almoxarife

### Views de Requisição
- `criar_requisicao()`: Cria nova requisição com formset
- `listar_requisicoes()`: Lista com filtros
- `detalhe_requisicao()`: Detalhes de uma requisição
- `excluir_requisicao()`: Exclui requisição pendente

### Views de Atendimento
- `iniciar_atendimento_requisicao()`: Inicia atendimento
- `almoxarife_atender_requisicao()`: Atende requisição

### Views de Usuário
- `criar_usuario()`: Cadastro de novos usuários

---

## 📝 Formulários (`core/forms.py`)

### RequestForm
- **Campos**: urgency, observations
- **Widgets**: Bootstrap classes
- **Validação**: Campos obrigatórios

### RequestItemForm
- **Campos**: item_requested, quantify, category
- **Formset**: Permite múltiplos itens
- **Validação**: Quantidade positiva

### CustomUserCreationForm
- **Campos**: username, email, role, sector
- **Validação**: Setor obrigatório para Encarregado
- **Estilização**: Bootstrap classes
- **Acesso**: Apenas para usuários com papel de Gestor

---

## 🔗 URLs e Rotas (`core/urls.py`)

### Rotas Principais
```
/                           → home_view
/requisicoes/criar/         → criar_requisicao
/requisicoes/               → listar_requisicoes
/requisicoes/<uuid>/        → detalhe_requisicao
/requisicoes/<uuid>/excluir/ → excluir_requisicao
/dashboard/                 → dashboard
```

### Rotas Específicas
```
/almoxarife/dashboard/      → almoxarife_dashboard
/almoxarife/atender_requisicao/<uuid>/ → almoxarife_atender_requisicao
/gestor/dashboard/          → gestor_dashboard
/usuarios/criar/            → criar_usuario (apenas Gestores)
```

### Rotas de Autenticação
```
/accounts/login/            → Login do sistema
/accounts/logout/           → Logout do sistema
/accounts/password_reset/   → Recuperação de senha
```

---

## 🔐 Sistema de Autenticação e Criação de Contas

### Login do Sistema
- **URL**: `/accounts/login/`
- **Template**: `templates/registration/login.html`
- **Funcionalidades**:
  - Formulário de login responsivo
  - Validação de credenciais
  - Link para recuperação de senha
  - Redirecionamento automático após login

### Criação de Usuários
- **URL**: `/usuarios/criar/` (apenas para Gestores)
- **Template**: `templates/core/criar_usuario.html`
- **Campos obrigatórios**:
  - Usuário (username)
  - E-mail
  - Senha e confirmação
  - Função (Gestor, Encarregado, Almoxarife)
  - Setor (obrigatório para Encarregado)
- **Validações**:
  - Usuário único
  - E-mail único
  - Senha com confirmação
  - Setor obrigatório para Encarregado

### Recuperação de Senha
- **URL**: `/accounts/password_reset/`
- **Funcionalidade**: Sistema nativo do Django

---

## 🛡️ Sistema de Permissões

### Funções de Verificação
- `is_almoxarife(user)`: Verifica se é almoxarife
- `is_gestor(user)`: Verifica se é gestor

### Decoradores Utilizados
- `@login_required`: Autenticação obrigatória
- `@user_passes_test`: Verificação de papel específico
- `@require_POST`: Apenas requisições POST

### Regras de Acesso
- **Encarregado**: Apenas suas requisições
- **Almoxarife**: Todas as requisições + atendimento
- **Gestor**: Todas as requisições + criação de usuários + acesso total ao sistema

---

## 📊 Dashboards e Estatísticas

### Dashboard Geral
- **Cards**: Pendentes, Aprovadas hoje, Total do mês
- **Alertas**: Requisições urgentes pendentes
- **Tabela**: Requisições recentes/ativas

### Dashboard do Gestor
- **Estatísticas**: Departamentos ativos, tendências
- **Visão geral**: Todas as requisições do dia
- **Funcionalidades**: Acesso para criar novos usuários

### Dashboard do Almoxarife
- **Foco**: Requisições pendentes para atendimento
- **Ações**: Iniciar atendimento

---

## 🔍 Filtros e Busca

### Filtros Disponíveis
- **Status**: Pendente, Em Atendimento, Aprovada
- **Data**: Filtro por data de criação
- **Urgência**: Normal, Urgente
- **Setor**: Filtro por departamento

### Implementação
- **Query Parameters**: GET requests
- **Queryset Filtering**: Django ORM
- **Interface**: Formulários no template

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes)

### Instalação
```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd requisitafacil-main

# 2. Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure o banco de dados
python manage.py makemigrations
python manage.py migrate

# 5. Crie um superusuário
python manage.py createsuperuser

# 6. Execute o servidor
python manage.py runserver
```

### Configuração Inicial
1. **Acesse** `http://localhost:8000/admin/`
2. **Faça login** com o superusuário
3. **Crie setores** no admin Django
4. **Crie usuários** com diferentes papéis
5. **Acesse** `http://localhost:8000/`

### Como Criar Novos Usuários
1. **Faça login** como Gestor
2. **Acesse** `http://localhost:8000/usuarios/criar/`
3. **Preencha** o formulário com:
   - Usuário (username)
   - E-mail
   - Senha e confirmação
   - Função (Gestor, Encarregado, Almoxarife)
   - Setor (obrigatório para Encarregado)
4. **Clique** em "Criar Usuário"

**Observação**: Apenas usuários com papel de **Gestor** podem criar novos usuários no sistema.

---

## 🔧 Configurações (`requisita_facil/settings.py`)

### Configurações Principais
- **DEBUG**: True (desenvolvimento)
- **SECRET_KEY**: Configurada para desenvolvimento
- **DATABASES**: SQLite (padrão)
- **AUTH_USER_MODEL**: 'core.User'
- **STATIC_URL**: 'static/'
- **TEMPLATES**: Configurado para pasta templates/

### Configurações de Autenticação
- **LOGIN_REDIRECT_URL**: '/'
- **LOGOUT_REDIRECT_URL**: '/accounts/login/'

---

## 📦 Dependências (`requirements.txt`)

```
Django>=4.2          # Framework web
psycopg2-binary>=2.9 # Driver PostgreSQL
python-dotenv>=1.0   # Variáveis de ambiente
```

---

## 🔄 Migrações

### Migrações Existentes
- `0001_initial.py`: Criação inicial dos modelos
- `0002_alter_user_sector.py`: Alteração no campo sector
- `0003_requestitem_ean_requestitem_observations_and_more.py`: Adição de campos
- `0004_remove_requestitem_ean_and_more.py`: Remoção de campos
- `0005_requestitem_observacao_item_and_more.py`: Novos campos
- `0006_alter_request_status.py`: Alteração nos status

---

## 🎯 Funcionalidades Avançadas

### Geração Automática de Códigos
- **Formato**: SETOR-NÚMERO (ex: F-1, FR-2)
- **Mapeamento**: Setores para abreviações
- **Sequencial**: Número automático por setor

### Formset Dinâmico
- **Adicionar/Remover** itens dinamicamente
- **Validação** em tempo real
- **JavaScript** para interação

### Alertas Inteligentes
- **Requisições urgentes** pendentes
- **Threshold**: Mais de 3 urgentes
- **Ação direta**: Link para filtro

---

## 🔒 Segurança

### Medidas Implementadas
- **CSRF Protection**: Tokens em formulários
- **Login Required**: Autenticação obrigatória
- **User Passes Test**: Verificação de papéis
- **UUID**: IDs únicos para recursos
- **SQL Injection**: Proteção via ORM

### Boas Práticas
- **Validação**: Formulários e modelos
- **Sanitização**: Dados de entrada
- **Permissões**: Controle granular
- **Logs**: Rastreamento de ações

---

## 📈 Melhorias Futuras

### Funcionalidades Sugeridas
- **Notificações**: Email/SMS para status
- **Relatórios**: PDF/Excel export
- **API REST**: Para integração
- **Auditoria**: Log de mudanças
- **Backup**: Automático do banco

### Otimizações Técnicas
- **Cache**: Redis para performance
- **CDN**: Para arquivos estáticos
- **Docker**: Containerização
- **CI/CD**: Pipeline automatizado
- **Testes**: Unitários e integração

---

## 📞 Suporte e Contato

Para dúvidas, sugestões ou problemas:
- **Desenvolvedor**: [Nome do Desenvolvedor]
- **Email**: [email@exemplo.com]
- **Repositório**: [URL do repositório]

---

## 📄 Licença

Este projeto está sob a licença [TIPO_DE_LICENÇA]. Veja o arquivo LICENSE para mais detalhes.

---

*Documentação atualizada em: [DATA]*
*Versão do sistema: 1.0*
