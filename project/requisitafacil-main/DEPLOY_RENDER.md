# Guia de Deploy - Requisita Fácil no Render

Este guia explica como fazer o deploy da aplicação Requisita Fácil no Render usando o plano gratuito.

## 📋 Pré-requisitos

- Conta no Render (gratuita)
- Repositório Git com o código da aplicação
- Conhecimento básico de Django e FastAPI

## 🏗️ Estrutura do Projeto

A aplicação consiste em dois componentes principais:
1. **Django App** - Aplicação principal web
2. **FastAPI Server** - Servidor WebSocket para atualizações em tempo real

## 📁 Arquivos Necessários para Deploy

### 1. build.sh
Crie este arquivo na raiz do projeto:

```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
```

### 2. render.yaml
Crie este arquivo na raiz do projeto:

```yaml
services:
  - type: web
    name: requisita-facil-web
    env: python
    buildCommand: "./build.sh"
    startCommand: "gunicorn requisita_facil.wsgi:application"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DJANGO_SETTINGS_MODULE
        value: requisita_facil.settings
      - key: SECRET_KEY
        generateValue: true
      - key: WEB_CONCURRENCY
        value: 4
      - key: DATABASE_URL
        fromDatabase:
          name: requisita-facil-db
          property: connectionString

  - type: web
    name: requisita-facil-realtime
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn realtime_server:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: PORT
        value: 8001

databases:
  - name: requisita-facil-db
    databaseName: requisitafacil
    user: requisitafacil
```

### 3. requirements.txt (Atualizado)
Certifique-se de que o arquivo requirements.txt contenha:

```
Django>=4.2
psycopg2-binary>=2.9
python-dotenv>=1.0
fastapi>=0.104.0
uvicorn>=0.24.0
requests>=2.31.0
beautifulsoup4>=4.12.0
websocket-client>=1.6.0
gunicorn>=21.2.0
whitenoise>=6.6.0
```

## ⚙️ Configurações do Django para Produção

### 1. Criar settings_production.py
Crie o arquivo `requisita_facil/settings_production.py`:

```python
import os
from pathlib import Path
from .settings import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-j_2q$hjrx4^n=s84#v5m-^(1os+7pa4v!um88r^jou3entdi&)')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'requisita-facil-web.onrender.com',
    'requisita-facil-realtime.onrender.com',
    'localhost',
    '127.0.0.1',
]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles_collected'

# Add whitenoise middleware for static files
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this line
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

### 2. Atualizar requirements.txt
Adicione estas dependências:

```
dj-database-url>=2.1.0
```

## 🚀 Passos para Deploy

### 1. Preparar o Repositório
```bash
# Certifique-se de que todos os arquivos estão commitados
git add .
git commit -m "Preparar para deploy no Render"
git push origin main
```

### 2. Criar Conta no Render
1. Acesse [render.com](https://render.com)
2. Crie uma conta gratuita
3. Conecte seu repositório GitHub

### 3. Deploy da Aplicação Web (Django)

1. **Criar novo Web Service**
   - Clique em "New +" → "Web Service"
   - Conecte seu repositório GitHub
   - Selecione o repositório do projeto

2. **Configurações do Serviço**
   - **Name**: `requisita-facil-web`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn requisita_facil.wsgi:application`

3. **Variáveis de Ambiente**
   - `DJANGO_SETTINGS_MODULE`: `requisita_facil.settings_production`
   - `SECRET_KEY`: (será gerado automaticamente)
   - `DATABASE_URL`: (será configurado após criar o banco)

### 4. Criar Banco de Dados PostgreSQL

1. **Criar novo PostgreSQL**
   - Clique em "New +" → "PostgreSQL"
   - **Name**: `requisita-facil-db`
   - **Database**: `requisitafacil`
   - **User**: `requisitafacil`

2. **Conectar ao Web Service**
   - Vá para o serviço web criado
   - Em "Environment Variables", adicione:
   - `DATABASE_URL`: (copie a URL do banco criado)

### 5. Deploy do Servidor Realtime (FastAPI)

1. **Criar novo Web Service**
   - Clique em "New +" → "Web Service"
   - Conecte o mesmo repositório

2. **Configurações do Serviço**
   - **Name**: `requisita-facil-realtime`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn realtime_server:app --host 0.0.0.0 --port $PORT`

3. **Variáveis de Ambiente**
   - `PORT`: `8001`

## 🔧 Configurações Adicionais

### 1. Atualizar URLs do Frontend
No arquivo `static/core/global-websocket.js`, atualize a URL do WebSocket:

```javascript
// Substitua a URL local pela URL do Render
const wsUrl = 'wss://requisita-facil-realtime.onrender.com/ws/updates';
const notifyUrl = 'https://requisita-facil-realtime.onrender.com/notify';
```

### 2. Configurar CORS no FastAPI
Atualize o `realtime_server.py` para aceitar apenas o domínio de produção:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://requisita-facil-web.onrender.com",
        "http://localhost:8000",  # Para desenvolvimento local
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📊 Monitoramento e Logs

### 1. Logs do Render
- Acesse o dashboard do Render
- Clique no serviço
- Vá para a aba "Logs"

### 2. Health Checks
O Render fará health checks automáticos. Certifique-se de que:
- A aplicação responde em `/`
- Não há erros 500
- O banco de dados está conectado

## 🔒 Segurança

### 1. Variáveis Sensíveis
- Nunca commite `SECRET_KEY` no código
- Use variáveis de ambiente para todas as configurações sensíveis
- O Render gera automaticamente uma `SECRET_KEY` segura

### 2. HTTPS
- O Render fornece HTTPS automaticamente
- Todas as URLs devem usar `https://`

## 🚨 Troubleshooting

### Problemas Comuns

1. **Erro de Build**
   - Verifique se o `build.sh` tem permissão de execução
   - Certifique-se de que todas as dependências estão no `requirements.txt`

2. **Erro de Banco de Dados**
   - Verifique se a `DATABASE_URL` está correta
   - Certifique-se de que o banco está ativo

3. **Erro de Static Files**
   - Verifique se o `collectstatic` está sendo executado
   - Certifique-se de que o `whitenoise` está configurado

4. **WebSocket não conecta**
   - Verifique se o servidor realtime está rodando
   - Verifique as configurações de CORS
   - Teste a conectividade manualmente

### Comandos Úteis

```bash
# Verificar logs
render logs --service requisita-facil-web

# Executar comando no servidor
render exec --service requisita-facil-web python manage.py shell

# Verificar status dos serviços
render ps
```

## 📈 Escalabilidade

### Limitações do Plano Gratuito
- **Web Services**: 750 horas/mês
- **PostgreSQL**: 90 dias de trial
- **Bandwidth**: 100GB/mês

### Upgrade para Plano Pago
Quando necessário, você pode:
- Upgrade para plano pago ($7/mês por serviço)
- Aumentar recursos de CPU/memória
- Adicionar mais serviços

## 🎯 URLs Finais

Após o deploy, suas URLs serão:
- **Aplicação Web**: `https://requisita-facil-web.onrender.com`
- **Servidor Realtime**: `https://requisita-facil-realtime.onrender.com`

## 📞 Suporte

- **Render Docs**: [docs.render.com](https://docs.render.com)
- **Django Docs**: [docs.djangoproject.com](https://docs.djangoproject.com)
- **FastAPI Docs**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)

---

**Nota**: Este guia assume que você está usando o plano gratuito do Render. Para projetos em produção com alto tráfego, considere um plano pago. 