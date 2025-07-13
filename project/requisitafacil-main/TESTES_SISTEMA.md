# 🧪 Sistema de Testes - Requisição Fácil

Este documento explica como usar o sistema de testes para verificar se todas as funcionalidades estão funcionando corretamente, incluindo a atualização dos cards de KPI do gestor.

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Como Executar os Testes](#como-executar-os-testes)
3. [Gerando Dados de Teste](#gerando-dados-de-teste)
4. [Testes Disponíveis](#testes-disponíveis)
5. [Verificando KPIs do Gestor](#verificando-kpis-do-gestor)
6. [Limpeza do Banco de Dados](#limpeza-do-banco-de-dados)
7. [Troubleshooting](#troubleshooting)

## 🎯 Visão Geral

O sistema de testes foi criado para:

- ✅ Gerar requisições falsas automaticamente
- ✅ Verificar se todas as funcionalidades estão funcionando
- ✅ Testar a atualização dos cards de KPI do gestor
- ✅ Validar permissões de usuários
- ✅ Testar fluxos completos de requisições
- ✅ Verificar estatísticas e gráficos
- ✅ Permitir testes isolados de cada funcionalidade
- ✅ Limpar o banco de dados de testes facilmente

## 🚀 Como Executar os Testes

### Opção 1: Testes Integrados e de Stress

Use o script:
```bash
python testar_sistema.py
```
- Testes de stress, geração de muitos dados, KPIs, etc.
- Menu interativo para gerar dados, rodar todos os testes, ver estatísticas e limpar dados.

### Opção 2: Testes Isolados de Funcionalidades

Use o script:
```bash
python executar_testes_funcionalidades.py
```
- Testa cada funcionalidade separadamente (criação, permissões, KPIs, fluxo, etc.)
- Menu interativo para rodar cada teste individualmente, rodar todos, ou limpar o banco de dados de testes.
- **Opção 17**: Limpa todas as requisições, itens e usuários de teste do banco.

### Recomendações
- Use `executar_testes_funcionalidades.py` para validar funcionalidades específicas durante o desenvolvimento.
- Use `testar_sistema.py` para testes de stress, geração de massa de dados e validação geral do sistema.
- Sempre limpe o banco após rodar muitos testes para evitar poluição de dados.

## 📊 Gerando Dados de Teste

### Comando Básico
```bash
python manage.py gerar_dados_teste
```

### Opções Disponíveis
- `--num-requisicoes`: Número de requisições a criar (padrão: 100)
- `--setores`: Lista de setores (padrão: todos os setores)
- `--dias-atras`: Dias para trás para criar requisições (padrão: 30)

## 🧪 Testes Disponíveis

### Testes Isolados (executar_testes_funcionalidades.py)
- Criação de requisição básica
- Geração de código de requisição
- Permissões de usuários
- KPIs do gestor
- Requisições urgentes
- Fluxo de atendimento do almoxarife
- Tempo médio de atendimento
- Percentual atendidas no prazo
- Estatísticas por setor
- Estatísticas por categoria
- Verificação de códigos únicos
- Acesso não autenticado
- Requisição inexistente
- Permissões de requisição
- Estatísticas vazias
- **Limpeza do banco de dados**

### Testes Integrados (testar_sistema.py)
- Geração de massa de dados
- Testes de stress
- Testes de KPIs com muitos dados
- Testes de performance
- Limpeza de dados

## 📈 Verificando KPIs do Gestor

1. **Acesse o sistema**: http://localhost:8000
2. **Faça login como gestor**: `gestor_teste` / `testpass123`
3. **Acesse o dashboard do gestor**
4. **Verifique os cards de KPI**

## 🧹 Limpeza do Banco de Dados

Após rodar testes, use a opção de limpeza para evitar poluição de dados:

- No menu do `executar_testes_funcionalidades.py`, escolha:
  - `17. Limpar dados de teste do banco de dados`
- Ou, no `testar_sistema.py`, use a opção de limpeza do menu.
- Isso remove todas as requisições, itens e usuários de teste criados durante os testes.

## 🔧 Troubleshooting

- Se aparecer erro de banco travado, pare o servidor e tente novamente.
- Se os testes não rodarem, confira se está no diretório correto e se o ambiente virtual está ativado.
- Se precisar limpar manualmente:
```bash
python manage.py shell
>>> from core.models import Request, RequestItem, User
>>> RequestItem.objects.all().delete()
>>> Request.objects.all().delete()
>>> User.objects.filter(username__icontains='test').delete()
>>> exit()
```

## 📝 Logs de Teste

Os testes geram logs detalhados mostrando:
- ✅ Requisições criadas com sucesso
- ✅ KPIs calculados corretamente
- ✅ Fluxos completos funcionando
- ✅ Permissões validadas
- ✅ Estatísticas geradas

## 📄 Histórico de Atualizações

- **[NOVO]** Adicionado script `executar_testes_funcionalidades.py` para testes isolados.
- **[NOVO]** Opção de limpeza de banco de dados no menu dos scripts de teste.
- **[NOVO]** Testes separados por funcionalidade para facilitar depuração e validação.

---

**🎉 Sistema de testes atualizado! Agora você pode testar e limpar o banco facilmente.** 