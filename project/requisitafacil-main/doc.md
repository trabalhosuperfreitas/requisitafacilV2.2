# Documentação do Projeto Requisita Fácil

## Visão Geral
O **Requisita Fácil** é um sistema web completo para gestão de requisições internas de materiais, desenvolvido em Django. O sistema oferece controle de permissões por papel (Almoxarife, Gestor, Encarregado), dashboards personalizados, filtros avançados, notificações em tempo real e acompanhamento completo do ciclo de vida das requisições.

---

## 🏗️ Arquitetura do Sistema

### Tecnologias Utilizadas
- **Backend**: Django 4.2+
- **Frontend**: Bootstrap 5.3.3, CSS Customizado
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Autenticação**: Sistema nativo do Django
- **Interface**: Design responsivo com sidebar fixa
- **Tempo Real**: FastAPI WebSocket para notificações
- **JavaScript**: Interações dinâmicas e formset

### Estrutura de Pastas
```
requisitafacil-main/
├── core/                          # App principal
│   ├── models.py                  # Modelos de dados
│   ├── views.py                   # Lógica das views
│   ├── forms.py                   # Formulários Django
│   ├── urls.py                    # Rotas do app
│   ├── admin.py                   # Configuração do admin
│   ├── static/core/               # JavaScript customizado
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
├── realtime_server.py            # Servidor FastAPI para WebSocket
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
  - `status`: Status (Pendente/Em Atendimento/Atendida)
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
- **RequestStatus**: Pendente, Em Atendimento, Atendida

---

## 🎯 Funcionalidades por Papel

### 👤 Encarregado
- **Criar requisições** para seu setor
- **Visualizar** apenas suas requisições
- **Dashboard** com estatísticas pessoais
- **Excluir** requisições pendentes próprias
- **Receber notificações** em tempo real

### 🏢 Almoxarife
- **Visualizar** todas as requisições
- **Atender** requisições pendentes
- **Dashboard** específico para atendimento
- **Iniciar atendimento** de requisições
- **Finalizar** requisições com quantidades atendidas
- **Observações detalhadas** por item
- **Controle de concorrência** (evita conflitos)

### 👨‍💼 Gestor
- **Visualizar** todas as requisições
- **Dashboard avançado** com KPIs e gráficos
- **Gerenciar usuários** (CRUD completo)
- **Monitorar** tendências e departamentos ativos
- **Relatórios** de performance
- **Análise temporal** de requisições

---

## 🔄 Fluxo de Requisição

### 1. Criação da Requisição
```
Encarregado → /criar_requisicao/ → Preenche formulário → Salva no banco → Notificação em tempo real
```

**Processo**:
- Usuário acessa formulário
- Preenche urgência e observações
- Adiciona itens (nome, quantidade, categoria)
- Sistema gera código único automaticamente
- Requisição salva com status "Pendente"
- **Notificação WebSocket** enviada para todos os clientes

### 2. Atendimento da Requisição
```
Almoxarife → /almoxarife_dashboard/ → Seleciona requisição → Inicia atendimento → Atende → Finaliza
```

**Processo**:
- Almoxarife vê requisições pendentes
- **Inicia atendimento** (status → "Em Atendimento")
- **Controle de concorrência**: Apenas um almoxarife por requisição
- Preenche quantidades atendidas por item
- Adiciona observações específicas do item
- **Observações do atendimento** são anexadas
- Finaliza (status → "Atendida")
- **Notificação WebSocket** enviada

### 3. Acompanhamento
- **Encarregado**: Vê status das suas requisições
- **Gestor**: Monitora todas as requisições com KPIs
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
- **Gráficos** no dashboard do gestor

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
- `gestor_dashboard()`: Dashboard específico do gestor com KPIs
- `almoxarife_dashboard()`: Dashboard do almoxarife

### Views de Requisição
- `criar_requisicao()`: Cria nova requisição com formset
- `listar_requisicoes()`: Lista com filtros
- `detalhe_requisicao()`: Detalhes de uma requisição
- `excluir_requisicao()`: Exclui requisição pendente

### Views de Atendimento
- `iniciar_atendimento_requisicao()`: Inicia atendimento
- `almoxarife_atender_requisicao()`: Atende requisição com controle de concorrência

### Views de Usuário (Gestor)
- `usuarios_list()`: Lista todos os usuários
- `usuario_create()`: Cria novo usuário
- `usuario_edit()`: Edita usuário existente
- `usuario_delete()`: Remove usuário
- `criar_usuario()`: Formulário de criação

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

### Rotas de Gestão de Usuários (Gestor)
```
/configuracoes/usuarios/    → usuarios_list
/configuracoes/usuarios/novo/ → usuario_create
/configuracoes/usuarios/<uuid>/editar/ → usuario_edit
/configuracoes/usuarios/<uuid>/excluir/ → usuario_delete
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

### Gestão Completa de Usuários (Gestor)
- **Listagem**: `/configuracoes/usuarios/`
- **Criação**: `/configuracoes/usuarios/novo/`
- **Edição**: `/configuracoes/usuarios/<uuid>/editar/`
- **Exclusão**: `/configuracoes/usuarios/<uuid>/excluir/`

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

### Dashboard do Gestor (Avançado)
- **KPIs Principais**:
  - Requisições pendentes
  - Aprovadas hoje
  - Total do mês
  - Departamentos ativos
  - Requisições urgentes pendentes
- **Métricas de Performance**:
  - Tempo médio de atendimento
  - % atendidas no prazo (24h)
  - Setor com mais requisições
  - Usuário com mais requisições
- **Gráficos**:
  - Requisições por setor (30 dias)
  - Distribuição por status
  - Evolução diária
  - Top 5 usuários
  - Categorias mais requisitadas
- **Tabela**: Requisições recentes (20 últimas)

### Dashboard do Almoxarife
- **Foco**: Requisições pendentes para atendimento
- **Ações**: Iniciar atendimento
- **Controle**: Evita conflitos de atendimento

---

## 🔍 Filtros e Busca

### Filtros Disponíveis
- **Status**: Pendente, Em Atendimento, Atendida
- **Data**: Filtro por data de criação
- **Urgência**: Normal, Urgente
- **Setor**: Filtro por departamento

### Implementação
- **Query Parameters**: GET requests
- **Queryset Filtering**: Django ORM
- **Interface**: Formulários no template

---

## ⚡ Sistema de Notificações em Tempo Real

### Servidor FastAPI (`realtime_server.py`)
- **WebSocket**: `/ws/updates`
- **Notificações**: `/notify`
- **Funcionalidades**:
  - Conexões WebSocket persistentes
  - Broadcast de atualizações
  - CORS habilitado
  - Limpeza automática de conexões

### Integração com Django
- **Notificações enviadas**:
  - Nova requisição criada
  - Requisição finalizada
- **Método**: `requests.post('http://localhost:8001/notify')`
- **Dados**: JSON com ação específica

### JavaScript Client
- **Arquivo**: `static/core/admin_user_sector.js`
- **Funcionalidades**:
  - Conexão WebSocket automática
  - Recebimento de notificações
  - Atualização da interface
  - Reconexão automática

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

### Controle de Concorrência (Almoxarife)
- **Proteção**: Apenas um almoxarife por requisição
- **Verificação**: Status e atendido_por
- **Mensagens**: Feedback claro sobre conflitos

### Observações Detalhadas
- **Item**: Observação específica por item
- **Atendimento**: Observações gerais do atendimento
- **Histórico**: Preservação de observações originais

### Alertas Inteligentes
- **Requisições urgentes** pendentes
- **Threshold**: Mais de 3 urgentes
- **Ação direta**: Link para filtro

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

# 6. Execute o servidor Django
python manage.py runserver

# 7. Execute o servidor FastAPI (em outro terminal)
python realtime_server.py
```

### Configuração Inicial
1. **Acesse** `http://localhost:8000/admin/`
2. **Faça login** com o superusuário
3. **Crie setores** no admin Django
4. **Crie usuários** com diferentes papéis
5. **Acesse** `http://localhost:8000/`

### Como Criar Novos Usuários
1. **Faça login** como Gestor
2. **Acesse** `http://localhost:8000/configuracoes/usuarios/`
3. **Clique** em "Novo Usuário"
4. **Preencha** o formulário com:
   - Usuário (username)
   - E-mail
   - Senha e confirmação
   - Função (Gestor, Encarregado, Almoxarife)
   - Setor (obrigatório para Encarregado)
5. **Clique** em "Salvar"

**Observação**: Apenas usuários com papel de **Gestor** podem gerenciar usuários no sistema.

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
fastapi>=0.104.0     # Servidor WebSocket
uvicorn>=0.24.0      # ASGI server
requests>=2.31.0     # HTTP client
```

---

## 🔄 Migrações

### Migrações Existentes
- `0001_initial.py`: Criação inicial dos modelos
- `0002_alter_user_sector.py`: Alteração no campo sector
- `0003_requestitem_ean_requestitem_observations_and_more.py`: Adição de campos
- `0004_remove_requestitem_ean_and_more.py`: Remoção de campos
- `0005_requestitem_observacao_item_and_more.py`: Novos campos (quantidade_atendida, observacao_item)
- `0006_alter_request_status.py`: Alteração nos status (Pendente/Em Atendimento/Atendida)

---

## 🔒 Segurança

### Medidas Implementadas
- **CSRF Protection**: Tokens em formulários
- **Login Required**: Autenticação obrigatória
- **User Passes Test**: Verificação de papéis
- **UUID**: IDs únicos para recursos
- **SQL Injection**: Proteção via ORM
- **Controle de Concorrência**: Evita conflitos de atendimento

### Boas Práticas
- **Validação**: Formulários e modelos
- **Sanitização**: Dados de entrada
- **Permissões**: Controle granular
- **Logs**: Rastreamento de ações
- **Transações**: Atomic operations

---

## 📈 Melhorias Futuras

### Funcionalidades Sugeridas
- **Notificações**: Email/SMS para status
- **Relatórios**: PDF/Excel export
- **API REST**: Para integração
- **Auditoria**: Log de mudanças
- **Backup**: Automático do banco
- **Mobile App**: Aplicativo nativo

### Otimizações Técnicas
- **Cache**: Redis para performance
- **CDN**: Para arquivos estáticos
- **Docker**: Containerização
- **CI/CD**: Pipeline automatizado
- **Testes**: Unitários e integração
- **Monitoramento**: Métricas de performance

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

*Documentação atualizada em: Dezembro 2024*
*Versão do sistema: 2.0*

### 🆕 Novidades da Versão 2.0

#### ✨ Funcionalidades Adicionadas
- **Sistema de Notificações em Tempo Real** com WebSocket
- **Gestão Completa de Usuários** para Gestores
- **Dashboard Avançado** com KPIs e gráficos
- **Controle de Concorrência** para almoxarifes
- **Observações Detalhadas** por item e atendimento
- **Métricas de Performance** e análise temporal
- **Interface Melhorada** com JavaScript dinâmico

#### 🔧 Melhorias Técnicas
- **Servidor FastAPI** para notificações
- **Transações Atômicas** para integridade
- **Validações Aprimoradas** nos formulários
- **Código Mais Robusto** com tratamento de erros
- **Documentação Completa** atualizada

#### 📊 Novos Dashboards
- **Gestor**: KPIs, gráficos, métricas de performance
- **Almoxarife**: Foco em atendimento com controle de concorrência
- **Encarregado**: Estatísticas pessoais melhoradas
